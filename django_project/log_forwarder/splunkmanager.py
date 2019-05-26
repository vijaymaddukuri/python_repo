from saltmanager.salt_utils import SaltNetAPI
from log_forwarder.constants import (KEY_SPLUNK_CLIENT,
                                     KEY_SPLUNK_SERVER)
from common.functions import (get_config, log_func_calls)
from log_forwarder.constants import (LOG_FORWARDER_ERROR,
                                     LOG_FORWARDER_ID)
from log_forwarder.responseparser import ResponseParser
from common.constants import KEY_SALT_RETRY_CONFIG_VALUES
from common.exceptions import TASException
import logging
import time

logger = logging.getLogger(__name__)


class SplunkSaltManager:
    def __init__(self):
        self.response_parser = ResponseParser()

    @log_func_calls(LOG_FORWARDER_ID)
    def install_splunk_forwarder(self, vm_ip):
        """Run splunk forwarder installer command into the Minion from Master VM
           :param vm_ip: Minion VM ip address
           :return: extracted response in dictionary with keys as success and failure
           :except: Exception when could not install or configuration agent on minion
           """
        installer_agent_script_path = get_config(KEY_SPLUNK_CLIENT, "INSTALLER_AGENT_SCRIPT_PATH")
        forwarder_password = get_config(KEY_SPLUNK_CLIENT, "SPLUNK_FORWARDER_ADMIN_PASSWORD")
        deployserver_ip = get_config(KEY_SPLUNK_SERVER, "SPLUNK_DEPLOYMENT_SERVER_IP")
        deployserver_port = get_config(KEY_SPLUNK_SERVER, "SPLUNK_DEPLOYMENT_SERVER_PORT")
        salt_api = SaltNetAPI()
        forwarder_details = {"pillar": {"deployment_server_ip": deployserver_ip,
                                        "deployment_server_port": deployserver_port,
                                        "forwarder_password": forwarder_password}}
        # Check if client vm is up and running
        vm_minion_status_resp = salt_api.check_minion_status(vm_ip)
        if not vm_minion_status_resp:
            err_code = "LOG_FWRDR012_CHECK_VM_STATUS"
            err_message = LOG_FORWARDER_ERROR[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(LOG_FORWARDER_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        minion_name = salt_api.get_minion_name_from_ip(vm_ip)
        splunk_api_response = salt_api.execute_command(minion_name['minion_name'],
                                                       args=installer_agent_script_path,
                                                       pillar_details=forwarder_details)

        if not splunk_api_response:
            err_code = "LOG_FWRDR009_UNABLE_INSTALL"
            err_message = LOG_FORWARDER_ERROR[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(LOG_FORWARDER_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        if 'status' not in splunk_api_response or \
                'comment' not in splunk_api_response:
            err_code = "LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE"
            err_message = LOG_FORWARDER_ERROR[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(LOG_FORWARDER_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        if not splunk_api_response['status']:
            err_code = "LOG_FWRDR000_SALT_SERVER_ERROR"
            err_message = LOG_FORWARDER_ERROR[err_code]
            err_trace = ""
            logger.error('{} err_code: {}, err_message: {}, err_trace: {}'
                         .format(LOG_FORWARDER_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        logger.info("{} Response received after executing "
                    "the Installation of Log Forwarder script".format(LOG_FORWARDER_ID))
        logger.debug("{} Response for Installation of Log Forwarder{}"
                     .format(LOG_FORWARDER_ID, str(splunk_api_response['comment'])))
        os_kernel = salt_api.get_os_kernel_from_minion_id(minion_name['minion_name'])
        os_kernel_fold = os_kernel.casefold()
        self.response_parser.parse_salt_script_response(splunk_api_response['comment'], os_kernel_fold)
        return True
