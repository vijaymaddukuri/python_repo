import logging
from monitoring.constants import MONITORING_ERRORS
from monitoring.constants import INSTALL_NIMSOFT_RESPONSE_STEPS_WINDOWS, INSTALL_NIMSOFT_RESPONSE_STEPS_LINUX,\
    UNINSTALL_NIMSOFT_RESPONSE_STEPS_WINDOWS, CLEANUP_NIMSOFT_RESPONSE_STEPS_LINUX

from common.constants import MONITORING_LOG_ID
from common.exceptions import TASException

logger = logging.getLogger(__name__)


class ResponseParser:
    """
    This class will parse the json response of salt scripts and
    return status and message as key-value pair
    """

    def parse_salt_script_response(self, response_in_dict, kernel_type):
        """
        Parse the response received after executing networker agent install salt script on the minion VM
        :param kernel_type: kernel type
        :param response_in_dict: Minion response
        :return: simplified parsed response
        """

        try:
            status_dict = False
            if 'return' not in response_in_dict or not response_in_dict['return'] or \
                    not isinstance(response_in_dict['return'][0], dict):
                err_code = "MON008_UNKNOWN_SALT_API_RESPONSE"
                err_message = MONITORING_ERRORS[err_code]
                err_trace = response_in_dict
                logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                                .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

            minion_key = next(iter(response_in_dict['return'][0]))
            minion_output = response_in_dict['return'][0][minion_key]
            if minion_output is None or isinstance(minion_output, list):
                err_code = "MON010_SALT_CONFIGURATION_ISSUE"
                err_message = MONITORING_ERRORS[err_code]
                err_trace = minion_output
                logger.critical("{} {} {} {}".format(MONITORING_LOG_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

            status_dict = True
            failed_step_num = -1
            fail_msg = ""
            for cmd_key, cmd_value in minion_output.items():
                if 'result' not in cmd_value and 'comment' not in cmd_value and \
                        '__run_num__' not in cmd_value:
                    err_code = "MON008_UNKNOWN_SALT_API_RESPONSE"
                    err_message = MONITORING_ERRORS[err_code]
                    err_trace = response_in_dict
                    logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                                    .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
                    logger.info("{} Exit: parse_monitoring_salt_script_response".format(MONITORING_LOG_ID))
                    raise TASException(err_code, err_message, err_trace)
                step = cmd_value['__run_num__']
                if not cmd_value['result'] and (failed_step_num == -1 or failed_step_num > step):
                    failed_step_num = step
                    fail_msg = str(cmd_value['comment'])
            if failed_step_num is -1:
                return status_dict

            if kernel_type == 'windows':
                err_code = INSTALL_NIMSOFT_RESPONSE_STEPS_WINDOWS[failed_step_num]
                err_message = MONITORING_ERRORS[err_code]
                err_trace = fail_msg
                logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                                .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)
            else:
                err_code = INSTALL_NIMSOFT_RESPONSE_STEPS_LINUX[failed_step_num]
                err_message = MONITORING_ERRORS[err_code]
                err_trace = fail_msg
                logger.critical('{} err_code: {}, err_message: {}, err_trace: {}'
                                .format(MONITORING_LOG_ID, err_code, err_message, err_trace))
                raise TASException(err_code, err_message, err_trace)

        except TASException:
            logger.info("{} Exit: parse_monitoring_salt_script_response".format(MONITORING_LOG_ID))
            raise

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {} ".format(MONITORING_LOG_ID, message))
            raise Exception(message)

    def parse_cleanup_linux_salt_response(self, response_in_dict, vm_hostname):
        """
                Parse the response received after cleaning up the packages client VM
                :param response_in_dict: nimsoft agent response
                :return: simplified parsed response
                """
        status_dict = dict(target_vm=vm_hostname, status=True, comment="Cleanup successfully done")

        try:
            minion_response = response_in_dict['comment']['return'][0]
            minion_response = minion_response[next(iter(minion_response))]
            for cmd_key, cmd_value in minion_response.items():
                if not cmd_value['result']:
                    error_comment = CLEANUP_NIMSOFT_RESPONSE_STEPS_LINUX[0]
                    raise TASException(error_comment,
                                       MONITORING_ERRORS[error_comment] + str(cmd_value['comment']),
                                       "")

        except KeyError as error:
            raise TASException("MON008_UNKNOWN_SALT_API_RESPONSE",
                               "{} || Response received: {} || Error Message: {}".format(
                                 MONITORING_ERRORS["MON008_UNKNOWN_SALT_API_RESPONSE"],
                                 response_in_dict, str(error)),
                               "")

        except IndexError as error:
            raise TASException("MON008_UNKNOWN_SALT_API_RESPONSE",
                               "{} || Response received: {} || Error Message: {}".format(
                                   MONITORING_ERRORS["MON008_UNKNOWN_SALT_API_RESPONSE"],
                                   response_in_dict, str(error)),
                               "")

        return status_dict

    def parse_uninstall_windows_salt_response(self, response_in_dict, vm_hostname):
        """
        Parse the response received after executing monitoring uninstall request on the client VM
        :param response_in_dict: nimsoft agent response
        :return: simplified parsed response
        """
        status_dict = dict(target_vm=vm_hostname, status=True, comment="Uninstallation successfully done")

        try:

            # -1 Indicates that no steps have failed yet
            failed_step_num = -1
            minion_response = response_in_dict['comment']['return'][0]
            minion_response = minion_response[next(iter(minion_response))]

            # Find No. of Steps
            total_steps = len(minion_response.keys())

            for cmd_key, cmd_value in minion_response.items():
                step = cmd_value['__run_num__']
                if not cmd_value['result'] and (failed_step_num == -1 or failed_step_num > step):
                    failed_step_num = step
                    fail_msg = str(cmd_value['comment'])

            if failed_step_num is not -1:
                error_comment = UNINSTALL_NIMSOFT_RESPONSE_STEPS_WINDOWS[(total_steps -
                                                                         failed_step_num) if (total_steps -
                                                                                              failed_step_num)
                                                                                               <= 2 else 0]
                raise TASException(error_comment,
                                   MONITORING_ERRORS[error_comment] + fail_msg,
                                   "")

        except KeyError as error:
            raise TASException("MON008_UNKNOWN_SALT_API_RESPONSE",
                               "{} || Response received: {} || Error Message: {}".format(
                                 MONITORING_ERRORS["MON008_UNKNOWN_SALT_API_RESPONSE"],
                                 response_in_dict, str(error)),
                               "")

        except IndexError as error:
            raise TASException("MON008_UNKNOWN_SALT_API_RESPONSE",
                               "{} || Response received: {} || Error Message: {}".format(
                                   MONITORING_ERRORS["MON008_UNKNOWN_SALT_API_RESPONSE"],
                                   response_in_dict, str(error)),
                               "")

        return status_dict

    def parse_uninstall_linux_salt_response(self, response_in_dict, vm_hostname):
        """
        Parse the response received after executing monitoring uninstall request on the client VM
        :param response_in_dict: nimsoft agent response
        :return: simplified parsed response
        """
        status_dict = dict(target_vm=vm_hostname, status=True, comment="Uninstallation successfully done")

        try:

            # -1 Indicates that no steps have failed yet
            failed_step_num = -1
            minion_response = response_in_dict['comment']['return'][0]
            minion_response = minion_response[next(iter(minion_response))]

            # Find No. of Steps
            total_steps = len(minion_response.keys())

            for cmd_key, cmd_value in minion_response.items():
                step = cmd_value['__run_num__']
                if not cmd_value['result'] and (failed_step_num == -1 or failed_step_num > step):
                    failed_step_num = step
                    fail_msg = str(cmd_value['comment'])

            if failed_step_num is not -1:
                error_comment = UNINSTALL_NIMSOFT_RESPONSE_STEPS_WINDOWS[(total_steps -
                                                                         failed_step_num) if (total_steps -
                                                                                              failed_step_num)
                                                                                               <= 1 else 0]
                raise TASException(error_comment,
                                   MONITORING_ERRORS[error_comment] + fail_msg,
                                   "")

        except KeyError as error:
            raise TASException("MON008_UNKNOWN_SALT_API_RESPONSE",
                               "{} || Response received: {} || Error Message: {}".format(
                                 MONITORING_ERRORS["MON008_UNKNOWN_SALT_API_RESPONSE"],
                                 response_in_dict, str(error)),
                               "")

        except IndexError as error:
            raise TASException("MON008_UNKNOWN_SALT_API_RESPONSE",
                               "{} || Response received: {} || Error Message: {}".format(
                                   MONITORING_ERRORS["MON008_UNKNOWN_SALT_API_RESPONSE"],
                                   response_in_dict, str(error)),
                               "")

        return status_dict

