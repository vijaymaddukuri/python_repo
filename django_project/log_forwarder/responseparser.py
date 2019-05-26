import logging
from log_forwarder.constants import (LOG_FORWARDER_ERROR,
                                     LOG_FORWARDER_ID,
                                     INSTALL_SPLUNK_RESPONSE_STEPS)
from common.exceptions import TASException

logger = logging.getLogger(__name__)


class ResponseParser:
    """
    This class will parse the json response of salt scripts and
    return status and message as key-value pair
    """

    def parse_salt_script_response(self, response_in_dict, kernel_type):
        """
        Parse the response received after executing splunk forwarder install salt script on the minion VM
        :param kernel_type: kernel type
        :param response_in_dict: Minion response
        :return: simplified parsed response
        """
        try:
            status_dict = False
            if 'return' not in response_in_dict or not response_in_dict['return'] or \
                    not isinstance(response_in_dict['return'][0], dict):
                err_code = "LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE"
                err_message = LOG_FORWARDER_ERROR[err_code]
                err_trace = response_in_dict
                logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                                .format(LOG_FORWARDER_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

            minion_key = next(iter(response_in_dict['return'][0]))
            minion_output = response_in_dict['return'][0][minion_key]
            if minion_output is None or isinstance(minion_output, list):
                err_code = "LOG_FWRDR010_SALT_CONFIGURATION_ISSUE"
                err_message = LOG_FORWARDER_ERROR[err_code]
                err_trace = minion_output
                logger.critical("{} {} {} {}".format(LOG_FORWARDER_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

            status_dict = True
            failed_step_num = -1
            fail_msg = ""
            for cmd_key, cmd_value in minion_output.items():
                if 'result' not in cmd_value and 'comment' not in cmd_value and \
                        '__run_num__' not in cmd_value:
                    err_code = "LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE"
                    err_message = LOG_FORWARDER_ERROR[err_code]
                    err_trace = response_in_dict
                    logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                                    .format(LOG_FORWARDER_ID, err_code, err_message, err_trace))
                    logger.info("{} Exit: parse_salt_script_response".format(LOG_FORWARDER_ID))
                    raise TASException(err_code, err_message, err_trace)
                step = cmd_value['__run_num__']
                if not cmd_value['result'] and (failed_step_num == -1 or failed_step_num > step):
                    failed_step_num = step
                    fail_msg = str(cmd_value['comment'])
            if failed_step_num is -1:
                return status_dict

            err_code = INSTALL_SPLUNK_RESPONSE_STEPS[kernel_type][failed_step_num]
            err_message = LOG_FORWARDER_ERROR[err_code]
            err_trace = fail_msg
            logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                            .format(LOG_FORWARDER_ID, err_code, err_message, err_trace))
            raise TASException(err_code, err_message, err_trace)

        except TASException:
            logger.info("{} Exit: parse_salt_script_response".format(LOG_FORWARDER_ID))
            raise

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {} ".format(LOG_FORWARDER_ID, message))
            raise Exception(message)
