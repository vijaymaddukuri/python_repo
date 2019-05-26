from robot.api import logger
from utils.SSHUtils import SSHUtil
from utils.GetConfigurations import GetConfigurations
from conf.restConstants import REST_TIMEOUT
import datetime
import time
import re


class ExecuteLogCheck:
    """
            Based on the Start time of the test case, It fetches All Log entries
            generated from that time. user should provide an exit pattern in form
            of a regex to segregate the log entries. It tries for 5 times to fetch
            the correct entries and in case no entry is generates, it returns ""
            e.g:

            My If my desired Log chunk Looks like
            start Backup:
            Lines....
            .........
            .........
            End backup:

            My Regex should be:
            start Backup:((.|\n)*?)End backup:

    """
    def current_time_utc(self):
        """
        Use it in Robot file in beginning of test to get the start time
        :return: Time in UTC
        """
        dt = datetime.datetime.utcnow()
        dt = dt.strftime("%d/%b/%Y %H:%M:%S")
        return dt

    def asleep(self, sleep_time):
        """
        Use it in Robot for waiting in Seconds
        :param sleep_time: time in seconds
        :return:
        """
        time.sleep(float(sleep_time))

    def get_log(self, **kwargs):
        """
        :param kwargs:

        Args:
        service:        middleware, tas or worker
        start_time:     Use output of current_time_utc defined in the beginning of test
        exit_pattern:   REGEX pattern

            My If my desired Log chunk Looks like
            start Backup:
            Lines....
            .........
            .........
            End backup:

            My Regex should be:
            start Backup:((.|\n)*?)End backup:

        :return: Log chunk
        """

        # Get all configurations
        c = GetConfigurations()
        service = kwargs.get('service')

        if service == 'middleware':
            ip = c.get_config('local', 'MW_DETAILS', 'MW_IP')
            user = c.get_config('local', 'MW_DETAILS', 'MW_USER')
            pwd = c.get_config('local', 'MW_DETAILS', 'MW_PWD')
            log_location = c.get_config('local', 'LOG', 'MW_SERVICE_LOG')

        elif service == 'tas':
            ip = c.get_config('local', 'TAS_DETAILS', 'TAS_IP')
            user = c.get_config('local', 'TAS_DETAILS', 'TAS_USER')
            pwd = c.get_config('local', 'TAS_DETAILS', 'TAS_PWD')
            log_location = c.get_config('local', 'LOG', 'TAS_SVC')

        elif service == 'worker':
            ip = c.get_config('local', 'MW_DETAILS', 'MW_IP')
            user = c.get_config('local', 'MW_DETAILS', 'MW_USER')
            pwd = c.get_config('local', 'MW_DETAILS', 'MW_PWD')
            log_location = c.get_config('local', 'LOG', 'WORKER_LOG')

        self.ssh_obj = SSHUtil(host=ip, username=user,
                               password=pwd, timeout=100)

        regex_pattern = kwargs.get('exit_pattern')

        # AWK command to fetch the logs starting from the test start time
        tail_cmd = 'awk -F\'[]]|[[]\'  \'$0 ~ /^\\[/ && $2 >= \"' + \
                   kwargs.get('start_time').encode('ascii','ignore') + \
                   '\" { p=1 }  p { print $0 }\' ' + log_location

        logger.info(tail_cmd)

        # Loop until the regex pattern is found in logs
        for i in range(5):

            # Fetch logs in a string
            logs = self.ssh_obj.execute_command(tail_cmd)['output']
            matched = re.search(regex_pattern, logs)
            if matched:
                logger.info('###################   Matched Log Start ###########################')
                logger.info(matched.group(0))
                logger.info('###################   Matched Log End   ###########################')
                return matched.group(0)
            logger.info("Couldn't find log entry. Waiting for the log to update...")
            self.asleep(REST_TIMEOUT)

        return ""
