import time

from common.constants import (KEY_NETWORKER_CLIENT,
                              KEY_NETWORKER_SERVER,
                              BACKUP_LOG_ID,
                              KEY_SALT_RETRY_CONFIG_VALUES)
from common.functions import get_config, log_func_calls
from common.exceptions import TASException
from saltmanager.salt_utils import SaltNetAPI
from backup.responseparser import ResponseParser
from backup.constants import BACKUP_ERRORS
from backup.Networker import Networker
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class NetworkerAPI:
    """
            This class  will call the networker related functions and
            add jobs to execute on minions.
        """

    def __init__(self):
        self.response_parser = ResponseParser()

    @log_func_calls(BACKUP_LOG_ID)
    def pick_networker(self, hostname):
        """
        :param hostname:
        :return: string url of the networker to use, if None there are not any avialble Networker(s)
        """
        networker_list = get_config(KEY_NETWORKER_SERVER, "NETWORKER_SERVERS")
        logger.debug('{} pick_networker: networker list - {}'.format(BACKUP_LOG_ID,
                                                                     [i['url'] for i in networker_list]))
        networker_max_clients = int(get_config(KEY_NETWORKER_SERVER, "NETWORKER_MAX_CLIENTS"))
        networker_max_jobs = int(get_config(KEY_NETWORKER_SERVER, "NETWORKER_MAX_JOBS"))
        selected_networker = None
        for networker in networker_list:
            networker_api = Networker(networker['username'], networker['password'], networker['url'])
            client = networker_api.get_client(hostname)
            if "error_code" not in client and 'aliases' in client and hostname in client['aliases']:
                return networker
            if not selected_networker and not networker_api.is_full(networker_max_clients,
                                                                    networker_max_jobs):
                selected_networker = networker
        if selected_networker:
            return selected_networker
        else:
            logger.info('{} None of the Networker is picked. Either max client or max'
                        ' job limit is exceeded.'.format(BACKUP_LOG_ID))
        return None

    @log_func_calls(BACKUP_LOG_ID)
    def get_networker_for_client(self, hostname):
        """
        :param hostname:
        :return: Finds the networker which contains a client with hostname
        """
        networker_list = get_config(KEY_NETWORKER_SERVER, "NETWORKER_SERVERS")
        logger.debug('{} get_networker_for_client: networker list - {}'
                     .format(BACKUP_LOG_ID, [i['url'] for i in networker_list]))
        for networker in networker_list:
            networker_api = Networker(networker['username'], networker['password'], networker['url'])
            client = networker_api.get_client(hostname)
            if client:
                return dict(networker=networker, client=client)
        return None

    @log_func_calls(BACKUP_LOG_ID)
    def get_minion_name(self, vm_ip):
        """
        :param vm_ip: VM ipaddress
        :return: return dictionary containing VM minion name
        """
        logger.debug("{} get_minion_name: parameters : {} ".format(BACKUP_LOG_ID, vm_ip))
        salt_api = SaltNetAPI()
        vm_minion_id_resp = salt_api.get_minion_name(vm_ip, 'ipcidr')
        return vm_minion_id_resp

    @log_func_calls(BACKUP_LOG_ID)
    def get_fqdn_from_minion_id(self, vm_minion_id):
        logger.debug("{} get_fqdn_from_minion_id: parameters : {} ".format(BACKUP_LOG_ID, vm_minion_id))
        salt_api = SaltNetAPI()
        vm_fqdn_resp = salt_api.get_fqdn_from_minion_id(vm_minion_id)
        return vm_fqdn_resp

    @log_func_calls(BACKUP_LOG_ID)
    def add_host_entry_on_minion(self, vm_minion_id):
        """
        Add DNS entry in etc host file on Minion VM
        :param vm_minion_id: Minion VM id
        :return: extracted response in dictionary with keys as success and failure
        :except: Exception when not able to add dns entry
        """
        logger.debug("{} add_host_entry_on_minion: parameters : {} ".format(BACKUP_LOG_ID, vm_minion_id))
        host_entry_response = {}
        host_entry_script_path = get_config(KEY_NETWORKER_CLIENT, "HOST_ENTRY_SCRIPT_PATH")
        salt_api = SaltNetAPI()
        networker_list = get_config(KEY_NETWORKER_SERVER, "NETWORKER_SERVERS")
        datadomain_list = get_config(KEY_NETWORKER_SERVER, "DATADOMAIN_SERVERS")
        domain_name = get_config(KEY_NETWORKER_SERVER, "DOMAIN_NAME")
        pillar_nw_dd_host_entry = "nw_dd_host_entry"
        pillar_details = {"pillar": {"nw_dd_fqdn_entry": domain_name,
                                     pillar_nw_dd_host_entry: {}}}

        # Adding pillar details in 'ip' as a key and 'host' as a value.
        for networker in networker_list:
            url_obj = urlparse(networker["url"])
            pillar_details["pillar"][pillar_nw_dd_host_entry][url_obj.hostname] = networker["hostname"]
        for datadomain in datadomain_list:
            pillar_details["pillar"][pillar_nw_dd_host_entry][datadomain["ip"]] = datadomain["hostname"]

        try:
            host_entry_api_response = salt_api.execute_command(vm_minion_id,
                                                               args=host_entry_script_path,
                                                               pillar_details=pillar_details)
            host_entry_response['status'] = False
            if host_entry_api_response is None:
                host_entry_response['comment'] = 'Unable to add host entry on VM'
                return host_entry_response

            if 'status' not in host_entry_api_response or \
                    'comment' not in host_entry_api_response:
                host_entry_response['comment'] = 'Response received after executing the salt ' \
                                                 'add host entry api command is not proper'
                return host_entry_response
            if not host_entry_api_response['status']:
                host_entry_response['comment'] = host_entry_api_response['comment']
                return host_entry_response
            logger.info("{} Response received after executing "
                        "adding host entry on minion".format(BACKUP_LOG_ID))
            logger.debug("{} Response for Adding host entry on minion {}"
                         .format(BACKUP_LOG_ID, str(host_entry_api_response['comment'])))
            host_entry_response = self.response_parser.parse_add_host_entry_script_response(
                host_entry_api_response['comment'])
            return host_entry_response

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} Exception :{}".format(BACKUP_LOG_ID, message))
            raise Exception(message)

    @log_func_calls(BACKUP_LOG_ID)
    def install_networker_agent(self, vm_hostname, vm_minion_id):
        """
        Run networker agent installer command into the Minion from Master VM
        :param vm_hostname: Minion VM Hostname
        :return: extracted response in dictionary with keys as success and failure
        :except: Exception when could not install agent on minion
        """
        logger.debug("{} install_networker_agent: parameters : {} ".format(BACKUP_LOG_ID, vm_hostname))
        networker_agent_response = {}
        installer_agent_script_path = get_config(KEY_NETWORKER_CLIENT, "INSTALLER_AGENT_SCRIPT_PATH")
        salt_api = SaltNetAPI()
        try:
            logger.info("installer_agent_script_path: {}".format(installer_agent_script_path))
            net_api_response = salt_api.execute_command(vm_minion_id, installer_agent_script_path)

            networker_agent_response['status'] = False
            if net_api_response is None:
                networker_agent_response['comment'] = 'Unable to install networker agent on VM'
                return networker_agent_response
            if 'status' not in net_api_response or \
                    'comment' not in net_api_response:
                networker_agent_response['comment'] = 'Response received after executing the ' \
                                                      'salt net api command is not proper'
                return networker_agent_response
            if not net_api_response['status']:
                networker_agent_response['comment'] = net_api_response['comment']
                return networker_agent_response
            logger.info("{} Response received after executing "
                        "the Installation of networker agent script".format(BACKUP_LOG_ID))
            logger.debug("{} Response for Installation of networker agent {}"
                         .format(BACKUP_LOG_ID, str(net_api_response['comment'])))
            networker_agent_response = self.response_parser\
                .parse_networker_agent_install_script_response(net_api_response['comment'])
            return networker_agent_response

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} Exception :{}".format(BACKUP_LOG_ID, message))
            raise Exception(message)

    @log_func_calls(BACKUP_LOG_ID)
    def add_entry_to_host_file(self, vm_hostname, vm_ipaddress, vm_fqdn, minion_id):
        """Add DNS entry in etc host file on the Minion
        :param vm_hostname: VM Hostname to be added to hostfile
        :param vm_ipaddress: VM ipaddress
        :param vm_fqdn: VM FQDN
        :param minion_id: Minion ID where the host entry needs to be done
        :return: extracted response in dictionary with keys as success and failure
        :except: Exception when not able to add dns entry
        """
        logger.debug("{} add_entry_to_host_file: parameters - {}, {}, {}, {}"
                     .format(BACKUP_LOG_ID, vm_hostname, vm_ipaddress, vm_fqdn, minion_id))
        installer_agent_script_path = get_config(KEY_NETWORKER_SERVER, "ADD_HOSTNAME_SCRIPT_PATH")
        salt_api = SaltNetAPI()
        add_response = {}
        try:
            pillar_details = {
                "pillar": {'minion_ip': vm_ipaddress, 'minion_hostname': vm_hostname, 'minion_fqdn': vm_fqdn}}
            net_api_response = salt_api.execute_command(minion_id, args=installer_agent_script_path,
                                                        pillar_details=pillar_details)

            if not net_api_response:
                raise TASException("BACKUP014_DNS_ENTRY_FAILURE",
                                   BACKUP_ERRORS["BACKUP014_DNS_ENTRY_FAILURE"], None)

            if 'status' not in net_api_response or 'comment' not in net_api_response:
                raise TASException("BACKUP015_SALT_EXECUTION_ERROR",
                                   BACKUP_ERRORS["BACKUP015_SALT_EXECUTION_ERROR"], None)

            if not net_api_response['status']:
                raise TASException("SALT ERROR", net_api_response['comment'], None)

            logger.info("{} Response received after executing "
                        "the script to add Client VM DNS entry".format(BACKUP_LOG_ID))
            logger.debug("{} Response for adding Client VM DNS entry {}"
                         .format(BACKUP_LOG_ID, str(net_api_response['comment'])))
            add_response = self.response_parser\
                .parse_add_host_entry_script_response(net_api_response['comment'])
            return add_response

        except TASException as e:
            add_response['status'] = False
            add_response['err_code'] = e.err_code
            add_response['comment'] = e.err_message
            add_response['err_trace'] = e.err_trace
            logger.error('{} {} '.format(BACKUP_LOG_ID, add_response))
            return add_response

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug('{}{}'.format(BACKUP_LOG_ID, message))
            raise Exception(message)

    @log_func_calls(BACKUP_LOG_ID)
    def enable_backup_on_client(self, vm_hostname, directories, protection_group, networker):
        """
        Run networker enable backup request
        :param vm_hostname: Minion VM Hostname
        :param directories: List of Directories that need to be backed up. Default
                           is ["All"] which means the entire filesystem
        :param protection_group: Name of the protection group, that the VM will be assigned to
        :return: extracted response in dictionary with keys as success and failure
        :except: Exception when could not enable backup on minion
        """
        logger.debug("{} enable_backup_on_client: parameters :{} {} {} "
                     .format(BACKUP_LOG_ID, vm_hostname, directories, protection_group))

        networker_api = Networker(networker['username'], networker['password'], networker['url'])
        try:
            net_api_response = networker_api.enable_backup(vm_hostname, directories, protection_group)
            enable_backup_response = self.response_parser.parse_networker_response(net_api_response,
                                                                                   vm_hostname)
            if not enable_backup_response['status']:
                logger.error("{} Error :{}".format(BACKUP_LOG_ID, str(enable_backup_response)))
                return enable_backup_response

            logger.info("{} Response received after executing "
                        "the Enable networker backup".format(BACKUP_LOG_ID))
            logger.debug("{} Response for Enabling networker backup on client :{} {}"
                         .format(BACKUP_LOG_ID, str(net_api_response[0]['result']),
                                 str(net_api_response[1]['result'])))
            return enable_backup_response

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {}".format(BACKUP_LOG_ID, message))
            raise Exception(message)

    @log_func_calls(BACKUP_LOG_ID)
    def check_minion_status(self, vm_ip):
        """
        Check status of minion VM if reachable or not
        :param vm_ip: Minion VM IP address
        :return: return status True as success and False as failure
        """
        logger.debug("{} check_minion_status: parameters : {}  ".format(BACKUP_LOG_ID, vm_ip))
        salt_ping_no_of_retries = get_config(KEY_SALT_RETRY_CONFIG_VALUES, "SALT_PING_NO_OF_RETRIES")
        salt_ping_retries_timeout = get_config(KEY_SALT_RETRY_CONFIG_VALUES, "SALT_PING_RETRIES_TIMEOUT")

        salt_api = SaltNetAPI()
        status = False
        for limit in range(salt_ping_no_of_retries):
            resp = salt_api.get_vm_minion_status(vm_ip, 'ipcidr')
            logger.debug("{} minion status : {}".format(BACKUP_LOG_ID, resp))
            if resp["status"]:
                logger.info("{} minion successfully found for VM with IP :{}".format(BACKUP_LOG_ID, vm_ip))
                status = True
                break
            logger.info("{} Retrying for minion status: Attempt {}/{}.".format(BACKUP_LOG_ID, limit + 1,
                                                                               salt_ping_no_of_retries))
            time.sleep(salt_ping_retries_timeout)
        return status

    @log_func_calls(BACKUP_LOG_ID)
    def action_on_vm_at_networker(self, method, hostname, **kwargs):
        """
        :param method: Method name for which we are using this function
        :param hostname: virtual machine hostname
        :param kwargs: extra parameters
        :return:
        """
        logger.debug("{} action_on_vm_at_networker parameters: {}, {}, {}"
                     .format(BACKUP_LOG_ID, method, hostname, kwargs))
        resp = None
        try:
            networker_list = get_config(KEY_NETWORKER_SERVER, "NETWORKER_SERVERS")
            logger.debug('{} get_client_details_from_networker: networker list - {}'
                         .format(BACKUP_LOG_ID, [i['url'] for i in networker_list]))
            for networker in networker_list:
                networker_api = Networker(networker['username'], networker['password'], networker['url'])
                client = networker_api.get_client(hostname)
                if client is None or 'hostname' not in client or client['hostname'] is None or \
                        'aliases' not in client or client['aliases'] is None \
                        or hostname not in client['aliases']:
                    continue
                if method in {'PauseVM', 'ResumeVM'}:
                    resp = networker_api.change_backup_state(client, kwargs['task_id'],
                                                             kwargs['state'])
                    break
            if resp is None:
                err_code = "BACKUP011_CLIENT_NOT_CONFIGURED"
                err_message = BACKUP_ERRORS[err_code]
                err_trace = ""
                raise TASException(err_code, err_message, err_trace)
        except TASException as e:
            raise
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {}".format(BACKUP_LOG_ID, message))
            raise Exception(message)
        return resp

    @log_func_calls(BACKUP_LOG_ID)
    def pause_vm_backup_service(self, hostname, task_id):
        """
        :param hostname: VM hostanme.
        :param task_id: Task Id for service request.
        :return: return response for backup service pause.
        """
        logger.info("{} pause_vm_backup_service: parameters- {}, {}"
                    .format(BACKUP_LOG_ID, hostname, task_id))

        pause_vm_backup_response = {'status': False}
        try:
            data = {}
            data['task_id'] = task_id
            data['state'] = False
            resp = self.action_on_vm_at_networker('PauseVM', hostname, **data)
            if isinstance(resp, dict):
                pause_vm_backup_response['comment'] = resp['error_message']
                pause_vm_backup_response['err_code'] = resp['error_code']
                logger.debug('{} Backup service pause on VM failed..'.format(BACKUP_LOG_ID))
            elif resp.ok:
                logger.debug('{} Backup service is paused on VM.'.format(BACKUP_LOG_ID))
                pause_vm_backup_response['status'] = True
            else:
                err_code = "BACKUP500_INTERNAL_SERVER_ERROR"
                err_message = BACKUP_ERRORS[err_code]
                err_trace = ""
                raise TASException(err_code, err_message, err_trace)
        except TASException as e:
            pause_vm_backup_response['err_code'] = e.err_code
            pause_vm_backup_response['comment'] = e.err_message
            pause_vm_backup_response['err_trace'] = e.err_trace
            logger.error('{} {}'.format(BACKUP_LOG_ID, pause_vm_backup_response))
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {}".format(BACKUP_LOG_ID, message))
            raise Exception(message)
        return pause_vm_backup_response

    @log_func_calls(BACKUP_LOG_ID)
    def disable_vm_backup_service(self, hostname, vm_ip, task_id):
        """
        :param hostname: VM hostname.
        :param vm_ip: VM ip address
        :param task_id: Task Id for service request.
        :return: return response for backup service disable.
        """
        logger.info("{} disable_vm_backup_service: parameters- {}, {}, {}"
                    .format(BACKUP_LOG_ID, hostname, vm_ip, task_id))
        disable_response = dict(status=True)
        salt_api = SaltNetAPI()

        cleanup_script_path = get_config(KEY_NETWORKER_CLIENT, "CLEANUP_BACKUP_SCRIPT_PATH")
        comment_script_path = get_config(KEY_NETWORKER_CLIENT, "COMMENT_BACKUP_SCRIPT_PATH")
        networker_list = get_config(KEY_NETWORKER_SERVER, "NETWORKER_SERVERS")
        datadomain_list = get_config(KEY_NETWORKER_SERVER, "DATADOMAIN_SERVERS")

        try:

            # Step 1: Pause Backup Service on VM - We do not delete client in NVE,
            # instead just put the VM in maintenance mode
            pause_vm_backup_response = self.pause_vm_backup_service(hostname, task_id)
            if 'err_code' in pause_vm_backup_response.keys():
                return pause_vm_backup_response

            # Step 2: Check Minion Status
            vm_minion_status_resp = self.check_minion_status(hostname)
            if not vm_minion_status_resp:
                raise TASException("BACKUP010_CHECK_HOSTNAME",
                                   BACKUP_ERRORS["BACKUP010_CHECK_HOSTNAME"],
                                   "")

            # Step 3: Fetch minion id of client VM
            vm_minion_id_resp = self.get_minion_name(vm_ip, 'ipcidr')
            if vm_minion_id_resp['status'] is False:
                raise TASException("MINION_ID_ERROR", vm_minion_id_resp['comment'], "")

            vm_minion_id = vm_minion_id_resp['minion_name']

            # Step 4: Perform Clean-up operation on Minion
            cleanup_ip_list = []
            for nw in networker_list:
                cleanup_ip_list.append(urlparse(nw["url"]).hostname)
            for dd in datadomain_list:
                cleanup_ip_list.append(dd["ip"])

            logger.debug("{} Cleanup pillars : {}".format(BACKUP_LOG_ID, cleanup_ip_list))
            cleanup_response = salt_api.execute_command(vm_minion_id,
                                                        args=cleanup_script_path,
                                                        pillar_details={
                                                            'pillar': {'ip_entries': cleanup_ip_list}})
            logger.debug("{} Cleanup Response : {}".format(BACKUP_LOG_ID, cleanup_response))

            disable_response = self.response_parser.\
                parse_minion_backup_cleanup_salt_response(cleanup_response, hostname)

            # Step 5: Fetch Correct Networker
            networker = self.get_networker_for_client(hostname)['networker']
            if not networker:
                raise TASException("BACKUP011_CLIENT_NOT_CONFIGURED",
                                   BACKUP_ERRORS["BACKUP011_CLIENT_NOT_CONFIGURED"], "")

            # Step 6: Perform Comment Operation on Networker
            comment_response = salt_api.execute_command(networker['minionid'],
                                                        args=comment_script_path,
                                                        pillar_details={
                                                            'pillar': {'minion_hostname': hostname}})
            logger.debug("{} Comment Response : {}".format(BACKUP_LOG_ID, comment_response))
            disable_response = self.response_parser.\
                parse_networker_minion_host_comment_salt_response(comment_response, hostname)

        except TASException as e:
            disable_response['status'] = False
            disable_response['err_code'] = e.err_code
            disable_response['comment'] = e.err_message
            disable_response['err_trace'] = e.err_trace
            logger.error('{} {}'.format(BACKUP_LOG_ID, disable_response))

        except KeyError as error:
            disable_response['status'] = False
            disable_response['err_code'] = "KEY_ERROR"
            disable_response['comment'] = "Response received: {}".format(str(error))
            disable_response['err_trace'] = ""
            logger.error('{} {}'.format(BACKUP_LOG_ID, disable_response))

        except IndexError as error:
            disable_response['status'] = False
            disable_response['err_code'] = "INDEX_ERROR"
            disable_response['comment'] = "Response received: {}".format(str(error))
            disable_response['err_trace'] = ""
            logger.error('{} {}'.format(BACKUP_LOG_ID, disable_response))

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {}".format(BACKUP_LOG_ID, message))
            raise Exception(message)

        return disable_response

    @log_func_calls(BACKUP_LOG_ID)
    def decommission_vm_backup_service(self, hostname, task_id):
        """
        :param hostname: VM hostname.
        :param task_id: Task Id for service request.
        :return: return response for backup service decommission.
        """
        logger.info("{} decommission_vm_backup_service: parameters - {}, {}"
                    .format(BACKUP_LOG_ID, hostname, task_id))
        decommission_response = dict(status=True)
        salt_api = SaltNetAPI()

        comment_script_path = get_config(KEY_NETWORKER_CLIENT, "COMMENT_BACKUP_SCRIPT_PATH")

        try:

            # Step 1: Pause Backup Service on VM - We should not delete client in NVE,
            # instead just put the VM in maintenance mode
            pause_vm_backup_response = self.pause_vm_backup_service(hostname, task_id)
            if 'err_code' in pause_vm_backup_response.keys():
                return pause_vm_backup_response

            # Step 2: Fetch Correct Networker
            networker = self.get_networker_for_client(hostname)['networker']
            if not networker:
                raise TASException("BACKUP011_CLIENT_NOT_CONFIGURED",
                                   BACKUP_ERRORS["BACKUP011_CLIENT_NOT_CONFIGURED"],
                                   "")

            # Step 3: Perform Comment Operation on Networker
            comment_response = salt_api.execute_command(networker['minionid'],
                                                        args=comment_script_path,
                                                        pillar_details={
                                                            'pillar': {'minion_hostname': hostname}})
            logger.debug("{} Comment Response : {}".format(BACKUP_LOG_ID, comment_response))
            decommission_response = self.response_parser\
                .parse_networker_minion_host_comment_salt_response(comment_response, hostname)

        except TASException as e:
            decommission_response['status'] = False
            decommission_response['err_code'] = e.err_code
            decommission_response['comment'] = e.err_message
            decommission_response['err_trace'] = e.err_trace
            logger.error('{} {}'.format(BACKUP_LOG_ID, decommission_response))

        except KeyError as error:
            decommission_response['status'] = False
            decommission_response['err_code'] = "KEY_ERROR"
            decommission_response['comment'] = "Response received: {}".format(str(error))
            decommission_response['err_trace'] = ""
            logger.error('{} {}'.format(BACKUP_LOG_ID, decommission_response))

        except IndexError as error:
            decommission_response['status'] = False
            decommission_response['err_code'] = "INDEX_ERROR"
            decommission_response['comment'] = "Response received: {}".format(str(error))
            decommission_response['err_trace'] = ""
            logger.error('{} {}'.format(BACKUP_LOG_ID, decommission_response))

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {}".format(BACKUP_LOG_ID, message))
            raise Exception(message)

        return decommission_response

    @log_func_calls(BACKUP_LOG_ID)
    def resume_vm_backup_service(self, hostname, task_id):
        """
        :param hostname: VM hostanme.
        :param task_id: Task Id for service request.
        :return: return response for backup service resume.
        """
        logger.info("{} resume_vm_backup_service: parameters - {}, {}"
                    .format(BACKUP_LOG_ID, hostname, task_id))

        resume_vm_backup_response = {'status': False}
        try:
            data = {}
            data['task_id'] = task_id
            data['state'] = True
            resp = self.action_on_vm_at_networker('ResumeVM', hostname, **data)
            if isinstance(resp, dict):
                resume_vm_backup_response['comment'] = resp['error_message']
                resume_vm_backup_response['err_code'] = resp['error_code']
                logger.debug('{} Backup service resume on VM failed..'.format(BACKUP_LOG_ID))
            elif resp.ok:
                resume_vm_backup_response['status'] = True
                logger.debug('{} Backup service is resume on VM succeeded.'.format(BACKUP_LOG_ID))
            else:
                err_code = "BACKUP500_INTERNAL_SERVER_ERROR"
                err_message = BACKUP_ERRORS[err_code]
                err_trace = ""
                raise TASException(err_code, err_message, err_trace)
        except TASException as e:
            resume_vm_backup_response['err_code'] = e.err_code
            resume_vm_backup_response['comment'] = e.err_message
            resume_vm_backup_response['err_trace'] = e.err_trace
            logger.error('{} {}'.format(BACKUP_LOG_ID, resume_vm_backup_response))
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {}".format(BACKUP_LOG_ID, message))
            raise Exception(message)
        return resume_vm_backup_response
