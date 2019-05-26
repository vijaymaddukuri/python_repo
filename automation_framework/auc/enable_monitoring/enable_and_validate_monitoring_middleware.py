import time
import datetime
import re
from auc.baseusecase import BaseUseCase
from robot.api import logger
from utils.SSHUtils import SSHUtil
from conf.restConstants import *
import requests as req
from base64 import b64encode


class EnableAndValidateMonitoringMiddleware(BaseUseCase):
    def test_execute_enable_monitoring(self):
        """
        Function to Enable Monitoring on the target VM.

        :return:
            Function returns status code from the REST API response and the messages
            200: OK
            500: INTERNAL SERVER ERROR
        """
        self.mw_ip = self.ctx_in['mw_ip']
        self.mw_user = self.ctx_in['mw_user']
        self.mw_pwd = self.ctx_in['mw_pwd']
        self.mw_header = JSON_HEADER
        enable_monitoring_data = {'TenantID': self.ctx_in['tenant_id'],
                                  'VirtualMachineID': self.ctx_in['vm_uuid'],
                                  'VirtualMachineHostName': self.ctx_in['vm_hostname'],
                                  'VirtualMachineIPAddress': self.ctx_in['vm_ip'],
                                  'Callback': self.ctx_in['callback'],
                                  'TaskID': self.ctx_in['task_id'],
                                  }
        logger.info(enable_monitoring_data)
        swagger_user = self.ctx_in['swagger_user']
        swagger_pwd = self.ctx_in['swagger_pwd']

        swagger_credentials = '{}:{}'.format(swagger_user, swagger_pwd)
        to_bytes = bytes(swagger_credentials)
        auth = b64encode(to_bytes).decode("ascii")
        self.mw_header['Authorization'] = 'Basic %s' % auth
        monitoring_result = "PASS"
        self.ssh_obj = SSHUtil(self.mw_ip, self.mw_user, self.mw_pwd)
        try:
            enable_monitoring_resp = req.post(MW_ENABLE_MONITORING.format(self.ctx_in['mw_ip']),
                                              json=enable_monitoring_data, headers=self.mw_header)

        except Exception as e:
            logger.info("Exception occurred while calling Enable Monitoring API. \n "
                        "Monitoring enabling did not happen.\nException: %s" % e)
            return 0

        logger.info("Status Code = %s" % enable_monitoring_resp.status_code)
        logger.info("Message = %s" % enable_monitoring_resp.text)
        if enable_monitoring_resp.status_code != 200:
            message = 'Could not access middleware monitoring API', \
                      enable_monitoring_resp.status_code
            logger.error(message)
            logger.debug(message)
            monitoring_result = "FAIL"

        else:
            logger.info('Can access middleware Monitoring API. '
                        'Response code = 200')

        # Validating the worker log
        if enable_monitoring_resp.status_code == 200:
            logger.info('Waiting for enable monitoring API to process the request')
            time.sleep(60)
            command = 'tail -n 210 /var/log/middleware/worker.log'
            result = self.ssh_obj.execute_command(command)
            logger.info('############################')
            logger.info("Validating worker log for Middleware to "
                        "tas connectivity")
            if "No route to host" in result['output']:
                message = 'Middleware to tas connectivity failed'
                logger.error(message)
                monitoring_result = "FAIL"
            else:
                logger.info("Communication is proper between TAS and middleware")
            cdate = datetime.datetime.now().strftime("%d/%b/%Y")
            matchObj = re.findall("{}\s\d+\:\d+\:\d+\]\s+ERROR \[\S+\:\d+\] \|\*MONITORING\*\|"
                                  .format(cdate), result['output'])
            if matchObj:
                message = 'Unable to enable monitoring from middleware.'
                logger.error(message)
                logger.debug(message)
                logger.info(result['output'])
                monitoring_result = "FAIL"
            else:
                logger.info('Enable Monitoring API is Successfully executed')
                logger.info(result['output'])
        else:
            monitoring_result = "FAIL"
        return monitoring_result

    def run_test(self):
        status = self.test_execute_enable_monitoring()
        logger.info("Status Code = %s" % status)
        return status

    def _finalize_context(self):
        assert self.ctx_out == 200, 'Could not enable monitoring'
