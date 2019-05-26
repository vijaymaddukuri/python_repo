from saltmanager.salt_utils import SaltNetAPI
from monitoring.constants import (KEY_NIMSOFT_CLIENT,
                                  KEY_NIMSOFT_SERVER)
from common.functions import get_config, log_func_calls
from monitoring.constants import MONITORING_ERRORS
from monitoring.responseparser import ResponseParser
from common.exceptions import TASException
from common.constants import MONITORING_LOG_ID, KEY_SALT_RETRY_CONFIG_VALUES
import logging
import time

logger = logging.getLogger(__name__)


class NimsoftAPI:
    def __init__(self):
        self.response_parser = ResponseParser()

    @log_func_calls(MONITORING_LOG_ID)
    def install_nimsoft_agent(self, vm_hostname, vm_ip):
        """Run nimsoft installer command into the Minion from Master VM
            :param vm_hostname: Minion VM Hostname
            :param vm_ip: Minion VM ip address
            :return: extracted response in dictionary with keys as success and failure
            :except: Exception when could not install or configuration agent on minion
            """
        installer_agent_script_path = get_config(KEY_NIMSOFT_CLIENT, "INSTALLER_AGENT_SCRIPT_PATH")
        hub_ip = get_config(KEY_NIMSOFT_SERVER, "NIMSOFT_HUB_IP")
        hub_name = get_config(KEY_NIMSOFT_SERVER, "NIMSOFT_HUB_NAME")
        domain = get_config(KEY_NIMSOFT_SERVER, "NIMSOFT_DOMAIN")
        hub_robot_name = get_config(KEY_NIMSOFT_SERVER, "NIMSOFT_HUB_ROBOT_NAME")
        hub_username = get_config(KEY_NIMSOFT_SERVER, "NIMSOFT_HUB_USERNAME")
        hub_password = get_config(KEY_NIMSOFT_SERVER, "NIMSOFT_HUB_PASSWORD")
        nimsoft_agent_response = {}
        salt_api = SaltNetAPI()
        error_message = ''
        robot_details = {"pillar": {"robotip": vm_ip, "hub_ip": hub_ip,
                                    "hub_name": hub_name, "domain": domain,
                                    "hub_robot_name": hub_robot_name, "hub_username": hub_username,
                                    "hub_password": hub_password}}

        # Check if client vm is up and running
        vm_minion_status_resp = salt_api.check_minion_status(vm_ip)
        if not vm_minion_status_resp:
            err_code = "MON013_CHECK_VM_STATUS"
            err_message = MONITORING_ERRORS[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        minion_name = salt_api.get_minion_name_from_ip(vm_ip)
        nim_api_response = salt_api.execute_command(minion_name['minion_name'], args=installer_agent_script_path,
                                                    pillar_details=robot_details)
        if not nim_api_response:
            err_code = "MON009_UNABLE_INSTALL"
            err_message = MONITORING_ERRORS[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        if 'status' not in nim_api_response or \
                'comment' not in nim_api_response:
            err_code = "MON008_UNKNOWN_SALT_API_RESPONSE"
            err_message = MONITORING_ERRORS[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        if not nim_api_response['status']:
            err_code = "MON000_SALT_SERVER_ERROR"
            err_message = MONITORING_ERRORS[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        logger.info("{} Response received after executing "
                    "the installation of Monitoring robot script".format(MONITORING_LOG_ID))
        logger.debug("{} Response for installation of Monitoring robot {}"
                     .format(MONITORING_LOG_ID, str(nim_api_response['comment'])))

        os_kernel = salt_api.get_os_kernel_from_minion_id(minion_name['minion_name'])
        os_kernel_fold = os_kernel.casefold()
        self.response_parser.parse_salt_script_response(nim_api_response['comment'], os_kernel_fold)
        return True

    @log_func_calls(MONITORING_LOG_ID)
    def uninstall_nimsoft_agent(self, vm_hostname, vm_ip):
        """Run nimsoft uninstaller command into the Minion from Master VM
            :param vm_hostname: Minion VM Hostname
            :param vm_ip: Minion VM ip address
            :return: extracted response in dictionary with keys as success and failure
            :except: Exception when could not uninstall or cleanup agent on minion
        """
        uninstaller_agent_script_path = get_config(KEY_NIMSOFT_CLIENT, "UNINSTALLER_AGENT_SCRIPT_PATH")
        cleanup_script_path = get_config(KEY_NIMSOFT_CLIENT, "CLEANUP_SCRIPT_PATH")
        salt_api = SaltNetAPI()

        # Check if client vm is up and running
        vm_minion_status_resp = salt_api.check_minion_status(vm_ip)
        if not vm_minion_status_resp:
            err_code = "MON013_CHECK_VM_STATUS"
            err_message = MONITORING_ERRORS[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        minion_name = salt_api.get_minion_name_from_ip(vm_ip)
        nim_api_response = salt_api.execute_command(minion_name['minion_name'], args=uninstaller_agent_script_path)

        if not nim_api_response:
            err_code = "MON0014_UNABLE_UNINSTALL"
            err_message = MONITORING_ERRORS[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        if 'status' not in nim_api_response or \
                'comment' not in nim_api_response:
            err_code = "MON008_UNKNOWN_SALT_API_RESPONSE"
            err_message = MONITORING_ERRORS[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        if not nim_api_response['status']:
            err_code = "MON000_SALT_SERVER_ERROR"
            err_message = MONITORING_ERRORS[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        logger.info("{} Response received after executing "
                    "the uninstallation of Monitoring robot script".format(MONITORING_LOG_ID))
        logger.debug("{} Response for uninstallation of Monitoring robot {}"
                     .format(MONITORING_LOG_ID, str(nim_api_response['comment'])))

        os_kernel = salt_api.get_os_kernel_from_minion_id(minion_name['minion_name'])
        os_kernel_fold = os_kernel.casefold()
        if os_kernel_fold == "windows":
            self.response_parser.parse_uninstall_windows_salt_response(nim_api_response, vm_hostname)
            return True
        else:
            self.response_parser.parse_uninstall_linux_salt_response(nim_api_response, vm_hostname)

            cleanup_api_response = salt_api.execute_command(minion_name['minion_name'], args=cleanup_script_path)

            if not cleanup_api_response:
                err_code = "MON0014_UNABLE_UNINSTALL"
                err_message = MONITORING_ERRORS[err_code]
                err_trace = ""
                logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                             .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

            if 'status' not in nim_api_response or \
                    'comment' not in nim_api_response:
                err_code = "MON008_UNKNOWN_SALT_API_RESPONSE"
                err_message = MONITORING_ERRORS[err_code]
                err_trace = ""
                logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                             .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

            if not nim_api_response['status']:
                err_code = "MON000_SALT_SERVER_ERROR"
                err_message = MONITORING_ERRORS[err_code]
                err_trace = ""
                logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                             .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

            logger.info("{} Response received after executing "
                        "the uninstallation of Monitoring robot script".format(MONITORING_LOG_ID))
            logger.debug("{} Response for uninstallation of Monitoring robot {}"
                         .format(MONITORING_LOG_ID, str(nim_api_response['comment'])))
            self.response_parser.parse_cleanup_linux_salt_response(cleanup_api_response, vm_hostname)
            return True


