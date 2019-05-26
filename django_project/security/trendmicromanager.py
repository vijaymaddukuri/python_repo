from saltmanager.salt_utils import SaltNetAPI
from common.functions import get_config, log_func_calls
from common.constants import (
    KEY_TRENDMICRO_CLIENT,
    KEY_TRENDMICRO_SERVER,
)
from security.constants import (SECURITY_ERRORS,
                                DSM_COMPUTER_LIST_URL,
                                DSM_COMPUTER_URL,
                                DSM_API_VERSION)
from common.exceptions import (TASException,
                               APIException)
from security.responseparser import ResponseParser
from common.constants import SECURITY_LOG_ID, KEY_SALT_RETRY_CONFIG_VALUES
from common.utils import RestClient
import time

import logging

logger = logging.getLogger(__name__)

class TrendMicroAPI:
    """
    This class  will call the security related functions and
    add jobs to execute on minions.
    """
    def __init__(self):
        self.response_parser = ResponseParser()

    @log_func_calls(SECURITY_LOG_ID)
    def check_minion_status(self, vm_ip):
        """
        :param vm_ip: IP address of client vm
        :return: True / False
        """
        logger.debug("{} check_minion_status: parameters : {}  ".format(SECURITY_LOG_ID, vm_ip))
        salt_ping_no_of_retries = get_config(KEY_SALT_RETRY_CONFIG_VALUES, "SALT_PING_NO_OF_RETRIES")
        salt_ping_retries_timeout = get_config(KEY_SALT_RETRY_CONFIG_VALUES, "SALT_PING_RETRIES_TIMEOUT")
        salt_api = SaltNetAPI()
        status = False
        for limit in range(salt_ping_no_of_retries):
            resp = salt_api.get_vm_minion_status(vm_ip, 'ipcidr')
            logger.debug("{} minion status : {}".format(SECURITY_LOG_ID, resp))
            if resp["status"]:
                logger.info("{} minion successfully found for ip: {}".format(SECURITY_LOG_ID, vm_ip))
                status = True
                break
            logger.info("{} Retrying for minion status: Attempt {}/{}.".format(SECURITY_LOG_ID, limit + 1,
                                                                               salt_ping_no_of_retries))
            time.sleep(salt_ping_retries_timeout)

        return status

    @log_func_calls(SECURITY_LOG_ID)
    def get_fqdn_from_vm_ip(self, vm_ip):
        """
        :param vm_ip: IP address of client vm
        :return: Response Object
        """
        logger.debug("{} get_fqdn_from_vm_ip: parameters : {} ".format(SECURITY_LOG_ID, vm_ip))
        salt_api = SaltNetAPI()
        vm_minion_id = salt_api.get_minion_name(vm_ip, 'ipcidr')
        if not vm_minion_id['status']:
            logger.error("{} Unable to fetch Minion id from VM. Errors: {} "
                         .format(SECURITY_LOG_ID, vm_minion_id['comment']))
            return vm_minion_id

        vm_fqdn_resp = salt_api.get_fqdn_from_minion_id(vm_minion_id['minion_name'])
        return vm_fqdn_resp

    @log_func_calls(SECURITY_LOG_ID)
    def delete_computer(self, computer_id):
        ip = get_config(KEY_TRENDMICRO_SERVER, "DSM_IP")
        port = get_config(KEY_TRENDMICRO_SERVER, "DSM_PORT")
        secret_key = get_config(KEY_TRENDMICRO_SERVER, "DSM_API_SECRET_KEY")
        delete_url = DSM_COMPUTER_URL + "/{}".format(computer_id)
        dsm_url = RestClient.get_https_url(ip, port, delete_url)

        # Header creation.
        headers = {"Content-Type": "application/json"}
        headers['api-version'] = DSM_API_VERSION
        headers['api-secret-key'] = secret_key
        headers['Cache-Control'] = 'no-cache'
        return RestClient.make_delete_request(dsm_url, headers=headers)
       

    @log_func_calls(SECURITY_LOG_ID)
    def get_dsm_response(self, vm_ip):
        vm_fqdn_resp = self.get_fqdn_from_vm_ip(vm_ip)
        if not vm_fqdn_resp['status']:
            logger.error("{} Unable to fetch FQDN from VM. Errors: {} "
                         .format(SECURITY_LOG_ID, vm_fqdn_resp['comment']))
            err_code = "SEC001_SALT_CONNECTION_ERROR"
            err_message = SECURITY_ERRORS[err_code]
            err_trace = vm_fqdn_resp['comment']
            raise TASException(err_code, err_message, err_trace)

        vm_fqdn = vm_fqdn_resp['fqdn']
        ip = get_config(KEY_TRENDMICRO_SERVER, "DSM_IP")
        port = get_config(KEY_TRENDMICRO_SERVER, "DSM_PORT")
        secret_key = get_config(KEY_TRENDMICRO_SERVER, "DSM_API_SECRET_KEY")

        dsm_url = RestClient.get_https_url(ip, port, DSM_COMPUTER_LIST_URL)

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        headers['api-version'] = DSM_API_VERSION
        headers['api-secret-key'] = secret_key
        headers['Cache-Control'] = 'no-cache'

        search_params = {"fieldName": "hostName", "stringTest": "equal"}
        search_params['stringValue'] = vm_fqdn
        search_list = [search_params]
        input_data = {"searchCriteria": search_list}
        logger.debug("{} DSM json_dict : {}".format(SECURITY_LOG_ID, input_data))
        return vm_fqdn, RestClient.post_JSON(dsm_url, headers=headers, payload=input_data)

    @log_func_calls(SECURITY_LOG_ID)
    def is_security_enabled_for_vm(self, vm_ip):
        """
        :param vm_ip: IP address of client vm
        :return: True / False
        """
        enable_status = False
        vm_fqdn, resp = self.get_dsm_response(vm_ip)
        dsm_computers_resp = resp.json()
        dsm_computers = dsm_computers_resp['computers']

        if len(dsm_computers) < 1:
            return enable_status

        for computer in dsm_computers:
            if computer['hostName'] == vm_fqdn:
                logger.info("{} VM - {} exist in DSM server computers list."
                            .format(SECURITY_LOG_ID, vm_fqdn))
                enable_status = True
                break

        return enable_status

    @log_func_calls(SECURITY_LOG_ID)
    def enable_security(self, vm_hostname, vm_ip, LinuxPolicyID, WindowsPolicyID):
        """
        Install trend-micro and enable security scan on the Minion from Master VM
        :param vm_hostname: Minion VM Hostname
        :param unix_policy_id: Policy id for unix VM
        :param win_policy_id: Policy id for windows VM
        :return: extracted response in dictionary with keys as success and failure
        :except: Exception when could not install agent on minion
        """
        logger.debug("{} enable_security: parameters - {} {} {} ".format(SECURITY_LOG_ID, vm_hostname,
                                                                         LinuxPolicyID, WindowsPolicyID))
        enable_security_response = {}
        try:
            security_enabled = self.is_security_enabled_for_vm(vm_ip)

            if security_enabled:
                enable_security_response['status'] = True
                msg = "Security service is already enabled on this {} VM."\
                      .format(vm_hostname)
                enable_security_response['comment'] = msg
                logger.info('{} {}'.format(SECURITY_LOG_ID, msg))
                return enable_security_response

            installer_agent_script_path = get_config(KEY_TRENDMICRO_CLIENT, "INSTALLER_AGENT_SCRIPT_PATH")
            dsm_ip = get_config(KEY_TRENDMICRO_SERVER, "DSM_IP")
            dsm_tenant_id = get_config(KEY_TRENDMICRO_SERVER, "DSM_TENANT_ID")
            dsm_tenant_pwd = get_config(KEY_TRENDMICRO_SERVER, "DSM_TENANT_PWD")
            salt_api = SaltNetAPI()
            pillar_details = {"pillar": {'unix_policy_id': LinuxPolicyID, 'win_policy_id': WindowsPolicyID,
                                         'dsm_ip': dsm_ip, 'tenant_id': dsm_tenant_id,
                                         'tenant_pwd': dsm_tenant_pwd}
                              }

            security_script_response = salt_api.execute_command_with_minion_ip(
                vm_ip, installer_agent_script_path, pillar_details)

            enable_security_response['status'] = False
            if not security_script_response:
                enable_security_response['err_code'] = "SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE"
                enable_security_response['comment'] = SECURITY_ERRORS[enable_security_response['err_code']]
                logger.error('{} {}'.format(SECURITY_LOG_ID, enable_security_response))
                return enable_security_response

            if 'status' not in security_script_response or \
                    'comment' not in security_script_response:
                enable_security_response['err_code'] = "SEC005_UNKNOWN_SALT_API_RESPONSE"
                enable_security_response['comment'] = SECURITY_ERRORS[enable_security_response['err_code']]
                logger.error('{} {}'.format(SECURITY_LOG_ID, enable_security_response))
                return enable_security_response

            if not security_script_response['status']:
                enable_security_response['err_code'] = "SEC001_SALT_CONNECTION_ERROR"
                enable_security_response['comment'] = security_script_response['comment']
                logger.error('{} {}'.format(SECURITY_LOG_ID, enable_security_response))
                return enable_security_response

            logger.info("{} Response received after executing Trend Micro agent installation and "
                        "enable security script".format(SECURITY_LOG_ID))
            logger.debug("{} Response of enable security script {} ".format(SECURITY_LOG_ID, str(
                security_script_response['comment'])))
            enable_security_response = self.response_parser.parse_security_salt_script_response(
                security_script_response['comment'])
            return enable_security_response

        except APIException as e:
            enable_security_response['status'] = False
            enable_security_response['err_code'] = "SEC009_DSM_API"
            enable_security_response['comment'] = SECURITY_ERRORS[enable_security_response['err_code']]
            enable_security_response['err_trace'] = e.received_message
            logger.error('{} {} '.format(SECURITY_LOG_ID, enable_security_response))
            return enable_security_response
        except TASException as e:
            enable_security_response['status'] = False
            enable_security_response['err_code'] = e.err_code
            enable_security_response['comment'] = e.err_message
            enable_security_response['err_trace'] = e.err_trace
            logger.error('{} {} '.format(SECURITY_LOG_ID, enable_security_response))
            return enable_security_response

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.error('{} {}'.format(SECURITY_LOG_ID, message))
            raise Exception(message)
