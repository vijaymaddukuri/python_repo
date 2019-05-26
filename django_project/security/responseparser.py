import logging
from security.constants import SECURITY_ERRORS
from common.exceptions import TASException
from common.constants import SECURITY_LOG_ID

logger = logging.getLogger(__name__)


class ResponseParser:
    """
    This class will parse the json response of salt scripts and
    return status and message as key-value pair

    """

    def parse_security_salt_script_response(self, response_in_dict):
        """
        Parse the response received after executing default salt script on the minion VM
        :param response_in_dict: Minion response
        :return: simplified parsed response
        """
        logger.info("{} Inside: parse_security_salt_script_response".format(SECURITY_LOG_ID))
        status_dict = {}
        try:
            if 'return' not in response_in_dict or not response_in_dict['return'] or \
                    not isinstance(response_in_dict['return'][0], dict):
                err_code = "SEC005_UNKNOWN_SALT_API_RESPONSE"
                err_message = SECURITY_ERRORS[err_code]
                err_trace = response_in_dict
                logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                                .format(SECURITY_LOG_ID, err_code, err_message, err_trace))
                logger.info("{} Exit: parse_security_salt_script_response".format(SECURITY_LOG_ID))
                raise TASException(err_code, err_message, err_trace)

            minion_key = next(iter(response_in_dict['return'][0]))
            minion_output = response_in_dict['return'][0][minion_key]
            if minion_output is None or isinstance(minion_output, list):
                err_code = "SEC006_SALT_CONFIGURATION_ISSUE"
                err_message = SECURITY_ERRORS[err_code]
                err_trace = minion_output
                logger.debug("{} {} {} {}".format(SECURITY_LOG_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

            # Fetching agentDeployment script output
            for step_key, step_val in minion_output.items():
                if any(key not in step_val for key in ('result', 'comment', '__run_num__')) \
                        or ("managed" not in step_key and 'changes' not in step_val):
                    err_code = "SEC005_UNKNOWN_SALT_API_RESPONSE"
                    err_message = SECURITY_ERRORS[err_code]
                    err_trace = response_in_dict
                    logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                                    .format(SECURITY_LOG_ID, err_code, err_message, err_trace))
                    logger.info("{} Exit: parse_security_salt_script_response".format(SECURITY_LOG_ID))
                    raise TASException(err_code, err_message, err_trace)

                # For windows VM, if transfer of power shell script to minion is succeeded or not
                if "managed" in step_key and step_val['result']:
                    continue
                if "managed" in step_key and not step_val['result']:
                    err_code = "SEC007_AGENT_DEPLOY_SCRIPT_COPY_FAILED"
                    err_message = SECURITY_ERRORS[err_code]
                    err_trace = step_val['comment']
                    logger.debug("{} Result extracted from Salt-script response: error_message:{} "
                                 "err_code:{} err_trace:{} ".format(SECURITY_LOG_ID, err_message,
                                                                    err_code, err_trace))
                    raise TASException(err_code, err_message, err_trace)

                # If Trend Micro Deep Security Agent is already present
                if not step_val['changes'] and (step_val['comment'] in
                                                ('unless execution succeeded', 'unless condition is true')):
                    logger.info("{} Trend Micro agent is already installed and security is enabled."
                                .format(SECURITY_LOG_ID))
                    err_code = "SEC010_SECURITY_ENABLED"
                    err_message = SECURITY_ERRORS[err_code]
                    err_trace = ""
                    raise TASException(err_code, err_message, err_trace)

                script_output = step_val['changes']['stdout']
                # content of changes field of command execution output
                if (script_output is None or script_output.find
                    ("Failed to download the Deep Security Agent installation script.") > 0) \
                        and step_val['changes']['stderr']:
                    err_code = "SEC002_TREND_MICRO_AGENT_DOWNLOAD_FAILURE"
                    err_message = SECURITY_ERRORS[err_code]
                    err_trace = step_val['changes']['stderr']
                    logger.debug("{} Result extracted from Salt-script response: error_message:{} "
                                 "err_code:{} err_trace:{} ".format(SECURITY_LOG_ID, err_message,
                                                                    err_code, err_trace))
                    raise TASException(err_code, err_message, err_trace)

                count_status = len(script_output.split("HTTP Status: 200 - OK"))
                # Installation and enable security both succeeded
                if count_status == 3:
                    status_dict['status'] = True
                    status_dict['comment'] = ""
                    logger.info("{} Exit: parse_security_salt_script_response".format(SECURITY_LOG_ID))
                    return status_dict
                # Installation only succeeded and activation failed
                elif count_status == 2:
                    err_code = "SEC004_ENABLE_SECURITY_FAILED"
                    err_message = SECURITY_ERRORS[err_code]
                    err_trace = script_output
                    logger.debug("{} Result extracted from Salt-script response: error_message: {} "
                                 "err_code: {} err_trace: {}".format(SECURITY_LOG_ID, err_message,
                                                                     err_code, err_trace))
                    raise TASException(err_code, err_message, err_trace)
                # Installation and enable security both failed
                else:
                    err_code = "SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE"
                    err_message = SECURITY_ERRORS[err_code]
                    err_trace = script_output
                    logger.debug("{} Result extracted from Salt-script response: error_message:{} "
                                 "err_code:{} err_trace:{} ".format(SECURITY_LOG_ID, err_message,
                                                                    err_code, err_trace))
                    raise TASException(err_code, err_message, err_trace)

        except TASException:
            logger.info("{} Exit: parse_security_salt_script_response".format(SECURITY_LOG_ID))
            raise
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug('{} {}'.format(SECURITY_LOG_ID, message))
            raise Exception(message)







