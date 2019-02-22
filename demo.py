import re

result = """
[21/Feb/2019 13:51:31] DEBUG [urllib3.connectionpool:396] http://100.64.51.150:36792 "POST /api/v1/security/enable HTTP/1.1" 200 0
[21/Feb/2019 13:51:31] DEBUG [common.utils:88] received status : 200
[21/Feb/2019 13:51:31] DEBUG [common.utils:89] received text   :
[21/Feb/2019 13:51:31] DEBUG [common.utils:90] received resp   : <Response [200]>
[21/Feb/2019 13:51:31] INFO [common.utils:91] Exit: make_post_request

TEST AUTOMATION LOG2019-02-21 16:14:58.655493

[21/Feb/2019 13:51:31] DEBUG [__main__:253] |*SECURITY*| service_now_call_back_data : {'TaskID': '79385', 'status': 'success', 'status_message': ''}
[21/Feb/2019 13:51:31] INFO [callbacks:51] |*SECURITY*| Inside: invoke_service_now_callback
[21/Feb/2019 13:51:31] DEBUG [callbacks:52] |*SECURITY*| invoke_service_now_callback: parameters -
[21/Feb/2019 13:51:31] DEBUG [callbacks:53] |*SECURITY*| url    : https://rubicondev.service-now.com/api/79385/middleware
[21/Feb/2019 13:51:31] DEBUG [callbacks:54] |*SECURITY*| data   : {'TaskID': '79385', 'status': 'success', 'status_message': ''}
[21/Feb/2019 13:51:31] INFO [common.functions:93] Inside: get_config
[21/Feb/2019 13:51:31] DEBUG [common.functions:94] get_config: parameters - servicenow, SERVICENOW_USERNAME
[21/Feb/2019 13:51:31] INFO [common.functions:99] Exit: get_config
[21/Feb/2019 13:51:31] INFO [common.functions:93] Inside: get_config
[21/Feb/2019 13:51:31] DEBUG [common.functions:94] get_config: parameters - servicenow, SERVICENOW_PASSWORD
[21/Feb/2019 13:51:31] INFO [common.functions:99] Exit: get_config
[21/Feb/2019 13:51:31] DEBUG [urllib3.connectionpool:824] Starting new HTTPS connection (1): rubicondev.service-now.com
[21/Feb/2019 13:51:39] DEBUG [urllib3.connectionpool:396] https://rubicondev.service-now.com:443 "POST /api/79385/middleware HTTP/1.1" 200 None
[21/Feb/2019 13:51:39] DEBUG [callbacks:69] |*SECURITY*| received status : 200
[21/Feb/2019 13:51:39] DEBUG [callbacks:70] |*SECURITY*| received text   :
[21/Feb/2019 13:51:39] DEBUG [callbacks:71] |*SECURITY*| received resp   : <Response [200]>
[21/Feb/2019 13:51:39] INFO [callbacks:72] |*SECURITY*| Exit: invoke_service_now_callback
[21/Feb/2019 13:51:39] DEBUG [pika.heartbeat:130] Received 30 heartbeat frames, sent 62, idle intervals 0
[21/Feb/2019 13:51:39] DEBUG [pika.adapters.select_connection:203] call_later: added timeout <pika.adapters.select_connection._Timeout object at 0x7f23185684a8> with deadline=1550757684.2845461 and callback=<bound method HeartbeatChecker._check_heartbeat of <pika.heartbeat.HeartbeatChecker object at 0x7f2318823fd0>>; now=1550757099.2845461; delay=585
[21/Feb/2019 13:51:39] INFO [__main__:303] |*SECURITY*| Exit: process_security_message
"""

automation_tag = "TEST AUTOMATION LOG2019-02-21 16:14:58.655493"
service_name = 'security'

data = result.split(automation_tag)

print("\|\*%s\*\|\s+ Exit: process_%s_message" % (service_name.upper(), service_name))

matchObj = re.findall("\|\*%s\*\|\s+ Exit: process_%s_message"
                      % (service_name.upper(), service_name),
                      str(data))

print(matchObj)


import datetime
import time
import re
from robot.api import logger

from deployment_automation.common.ssh_utility import SSHUtil

class WorkerLogValidation:
    def __init__(self, sshObject):
        """
        :param  sshObject: SSH Object to connect to the remote machine and fetch the log
        """
        ctime = (datetime.datetime.now())
        # self.automation_tag = 'TEST AUTOMATION LOG ' + str(ctime)
        self.automation_tag = 'TEST AUTOMATION LOG2019-02-21 16:14:58.655493'
        self.sshObject = sshObject

    def add_automation_tag_in_log(self):
        # Update the worker log with the automation tag
        update_worker_log  = "echo \"{}\" >> /var/log/middleware/worker.log".format(self.automation_tag)
        self.sshObject.execute_command(update_worker_log)
        logger.info("Added the automation tag in worker log")

    def validate_worker_log(self, vm_ip, service_name):
        """
        vm_ip: IP of the VM where service is installed/uninstalled
        service_name: Service name (backup or security or monitoring)

        :return: True or False
        """
        extract_log = 'tail -n 300 /var/log/middleware/worker.log'
        search = False
        logger.info('Waiting for enable {} API to process the request'.format(service_name))

        # Try to fetch the log in the time period of 120 secs
        for i in range(4):
            time.sleep(3)
            result = self.sshObject.execute_command(extract_log)
            if not result['status']:
                logger.error('Unable to extract the worker log')
                return False

            # Split the log with tag name and fetch the information
            data = result['output'].split(self.automation_tag)
            matchObj = re.findall("\|\*%s\*\|\s+ Exit: process_%s_message"
                                 % (service_name.upper(), service_name),
                                 str(data))
            print(matchObj)

            # If log is updated start performing the validation
            if matchObj is not None:
                cdate = datetime.datetime.now().strftime("%d/%b/%Y")

                # Check for errors
                error_check = re.findall("%s\s\d+\:\d+\:\d+\]\s+ERROR \[\S+\:\d+\] \|\*%s\*\|"
                                      % (cdate, service_name.upper()), str(data))

                # If errors are not there in the code, check for status code of the VM
                if not error_check:
                    status = re.findall("\s\d+\:\d+\:\d+\]\s+DEBUG \[\S+\:\d+\] http://%s:\d+ "
                                        "\"POST /api/v1/%s/enable HTTP/1.1\" 200"
                                        % (vm_ip, service_name), str(data))
                    if status:
                        return True
                    else:
                        return False
                else:
                    return False

            if not search:
                return False

ssh_obj = SSHUtil(host='10.100.26.124', username='root',
                               password='Password1', timeout=10)

logObj = WorkerLogValidation(ssh_obj)

# logObj.add_automation_tag_in_log()

logObj.validate_worker_log('100.64.51.150', 'security')