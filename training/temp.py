import time

from robot.api import logger


class WorkerLogValidation:
    """
    Fetch the MW API response worker log and validate the output
    """
    def __init__(self, sshObject):
        """
        :param  sshObject: SSH Object to connect to the MW machine and fetch the log
        """
        self.worker_log = '/var/log/middleware/worker.log'
        self.sshObject = sshObject

    def get_worker_log_line_count(self):
        """
        B efore executing the MW API, get the worker log lines count.
        :return: Integer - Line count
        """
        extract_log = 'wc -l {}|cut -d " " -f1'.format(self.worker_log)
        result = self.sshObject.execute_command(extract_log)
        return result['output']

    def validate_worker_log(self, line_count, service_name, search_string, wait_time=20):
        """
        Validate the worker log
        :param line_count: Output of get_worker_log_count() function
        :param service_name: Service name (backup or security or monitoring)
        :param search_string: Search string or regular expression
        :return: True or False
        """
        search = False
        logger.info('Waiting for enable {} API to process the request'.format(service_name))

        # Command to fetch the last line of log for the executed API call
        find_exit_string = "awk 'NR >= %s' %s|grep 'Exit: process_%s_message'" \
                           %(line_count, self.worker_log, service_name)

        # Command to search for errors in the log
        find_error_string = "awk 'NR >= %s' %s|grep '%s'" %(line_count, self.worker_log, search_string)

        # Try to fetch the log in the time period of 120 secs
        for i in range(6):
            time.sleep(wait_time)
            final_log = self.sshObject.execute_command(find_exit_string)

            # If log is updated, start performing the validation
            if final_log['output'] != '':
                search_error = self.sshObject.execute_command(find_error_string)

                # If error's are not there, return true
                if search_error['output'] == '':
                    return True
                else:
                    # If error's appear, return False
                    logger.error(search_error['output'])
                    return False

        # After wait time, If the log file is not updated, return False
        if not search:
            logger.error('Unable to fetch the log in the give time duration')
            return Faalse


from deployment_automation.common.ssh_utility import SSHUtil

ssh_obj = SSHUtil(host='10.100.26.124', username='root',
                  password='Password1', timeout=10)

logObj = WorkerLogValidation(ssh_obj)

count = logObj.get_worker_log_line_count()

print(count)

time.sleep(30)

error = 'ERROR \[callbacks:*\] \|\*SECURITY*\| Exception occured during ServiceNow call back'

print(logObj.validate_worker_log(count, 'security', error))


