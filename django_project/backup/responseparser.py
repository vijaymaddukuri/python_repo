import logging
from common.constants import BACKUP_LOG_ID
from backup.constants import (INSTALL_NETWORKER_RESPONSE_STEPS,
                              CLEANUP_NETWORKER_RESPONSE_STEPS,
                              COMMENT_NETWORKER_RESPONSE_STEPS,
                              BACKUP_ERRORS)
from common.exceptions import TASException
logger = logging.getLogger(__name__)


class ResponseParser:
    """
    This class will parse the json response of salt scripts and
    return status and message as key-value pair
    """
    def parse_networker_agent_install_script_response(self, response_in_dict):
        """
        Parse the response received after executing networker agent install salt script on the minion VM
        :param response_in_dict: Minion response
        :return: simplified parsed response
        """
        status_dict = {}
        try:
            status_dict['status'] = False
            if 'return' not in response_in_dict or not response_in_dict['return'] or \
                    not isinstance(response_in_dict['return'][0], dict):
                status_dict['comment'] = 'Response received after executing the state files on the VM is not proper'
                logger.critical("{} {}".format(BACKUP_LOG_ID, status_dict['comment']))
                return status_dict

            minion_key = next(iter(response_in_dict['return'][0]))
            minion_output = response_in_dict['return'][0][minion_key]
            if minion_output is None or isinstance(minion_output, list):
                status_dict['comment'] = "unable to apply states on VM. " \
                                         "check salt-master configurations."
                logger.debug("{} {}".format(BACKUP_LOG_ID, status_dict))
                return status_dict

            status_dict['status'] = True
            status_dict['comment'] = ""
            step_fail = -1
            fail_msg = ""
            for cmd_key, cmd_value in minion_output.items():
                if 'result' not in cmd_value and 'comment' not in cmd_value and \
                        '__run_num__' not in cmd_value:
                    status_dict['status'] = False
                    status_dict['comment'] = "Response received after executing the " \
                                             "state files on the VM is not proper"
                    logger.debug("{} {}".format(BACKUP_LOG_ID, status_dict))
                    return status_dict
                step = cmd_value['__run_num__']
                if not cmd_value['result'] and (step_fail == -1 or step_fail > step):
                    step_fail = step
                    fail_msg = str(cmd_value['comment'])
            if step_fail is not -1:
                status_dict['status'] = False
                status_dict['comment'] = INSTALL_NETWORKER_RESPONSE_STEPS[step_fail] + fail_msg
            return status_dict
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {} ".format(BACKUP_LOG_ID, message))
            raise Exception(message)

    def parse_add_host_entry_script_response(self, response_in_dict):
        """
        Parse the response received after executing addhosts/etchosts salt script on the minion VM
       :param response_in_dict: Minion response
       :return: simplified parsed response
       """
        status_dict = {}
        try:
            status_dict['status'] = False
            if 'return' not in response_in_dict or not response_in_dict['return'] or \
                    not isinstance(response_in_dict['return'][0], dict):
                status_dict['comment'] = 'Response received after executing the state files ' \
                                         'on the VM is not proper'
                logger.critical("{} {}".format(BACKUP_LOG_ID, status_dict['comment']))
                return status_dict

            minion_key = next(iter(response_in_dict['return'][0]))
            minion_output = response_in_dict['return'][0][minion_key]
            if minion_output is None or isinstance(minion_output, list):
                status_dict['comment'] = "unable to apply states on VM. " \
                                         "check salt-master configurations."
                logger.debug("{} {}".format(BACKUP_LOG_ID, status_dict))
                return status_dict

            status_dict['status'] = True
            status_dict['comment'] = ""
            for cmd_key, cmd_value in minion_output.items():
                if 'result' not in cmd_value and 'comment' not in cmd_value and \
                        '__run_num__' not in cmd_value:
                    status_dict['status'] = False
                    status_dict['comment'] = "Response received after executing the " \
                                             "state files on the VM is not proper"
                    logger.debug("{} {}".format(BACKUP_LOG_ID, status_dict))
                    return status_dict
                if not cmd_value['result']:
                    status_dict['status'] = False
                    status_dict['comment'] = 'Script failed to add host entry'
                    break
            return status_dict
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {} ".format(BACKUP_LOG_ID, message))
            raise Exception(message)

    def parse_networker_response(self, response_in_dict, vm_hostname):
        """
        Parse the response received after executing backup enable/disable request on the client VM
        :param response_in_dict: networker response
        :return: simplified parsed response
        """
        status_dict = {}
        status_dict['target_vm'] = vm_hostname
        status_dict['status'] = False
        try:
            if not response_in_dict:
                status_dict['comment'] = 'Unable to fulfill the request. Response is not in proper format.'
                status_dict['error_code'] = '500'
                return status_dict
            for item in response_in_dict:
                if 'error' in item and item['error'] and 'error_message' in item['error']:
                    status_dict['status'] = False
                    status_dict['comment'] = item['error']['error_message']
                    status_dict['error_code'] = item['error']['error_code']
                    return status_dict
                status_dict['status'] = True
                status_dict['comment'] = item['result']
            return status_dict
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug("{} {}".format(BACKUP_LOG_ID, message))
            raise Exception(message)

    def parse_minion_backup_cleanup_salt_response(self, response_in_dict, vm_hostname):
        """
        Parse the response received after executing backup cleanup request on the client VM
        :param response_in_dict: networker response
        :return: simplified parsed response
        """
        status_dict = dict(target_vm=vm_hostname, status=True, comment="Cleanup successfully done")

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
                # Last 2 steps are Fixed. Apart from that the other steps can vary in number
                error_comment = CLEANUP_NETWORKER_RESPONSE_STEPS[(total_steps -
                                                                  failed_step_num) if (total_steps -
                                                                                       failed_step_num)
                                                                                       <= 2 else 0]
                raise TASException(error_comment,
                                   BACKUP_ERRORS[error_comment] + fail_msg,
                                   "")

        except KeyError as error:
            raise TASException("BACKUP015_SALT_EXECUTION_ERROR",
                               "{} || Response received: {} || Error Message: {}".format(
                                 BACKUP_ERRORS["BACKUP015_SALT_EXECUTION_ERROR"],
                                 response_in_dict, str(error)),
                               "")

        except IndexError as error:
            raise TASException("BACKUP015_SALT_EXECUTION_ERROR",
                               "{} || Response received: {} || Error Message: {}".format(
                                   BACKUP_ERRORS["BACKUP015_SALT_EXECUTION_ERROR"],
                                   response_in_dict, str(error)),
                               "")

        return status_dict

    def parse_networker_minion_host_comment_salt_response(self, response_in_dict, vm_hostname):
        """
                Parse the response received after executing comment host entry request on the client VM
                :param response_in_dict: networker response
                :return: simplified parsed response
                """
        status_dict = dict(target_vm=vm_hostname, status=True, comment="Minion Entry Successfully commented")

        try:
            minion_response = response_in_dict['comment']['return'][0]
            minion_response = minion_response[next(iter(minion_response))]
            for cmd_key, cmd_value in minion_response.items():
                if not cmd_value['result']:
                    error_comment = COMMENT_NETWORKER_RESPONSE_STEPS[0]
                    raise TASException(error_comment,
                                       BACKUP_ERRORS[error_comment] + str(cmd_value['comment']),
                                       "")

        except KeyError as error:
            raise TASException("BACKUP015_SALT_EXECUTION_ERROR",
                               "{} || Response received: {} || Error Message: {}".format(
                                 BACKUP_ERRORS["BACKUP015_SALT_EXECUTION_ERROR"],
                                 response_in_dict, str(error)),
                               "")

        except IndexError as error:
            raise TASException("BACKUP015_SALT_EXECUTION_ERROR",
                               "{} || Response received: {} || Error Message: {}".format(
                                   BACKUP_ERRORS["BACKUP015_SALT_EXECUTION_ERROR"],
                                   response_in_dict, str(error)),
                               "")

        return status_dict


