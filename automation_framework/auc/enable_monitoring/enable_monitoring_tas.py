from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req


class ExecuteEnableMonitoring(BaseUseCase):
    def test_execute_enable_monitoring(self):
        """
        Function to Enable Monitoring on the target VM.

        :return:
            Function returns status code from the REST API response and the messages
            200: OK
            500: INTERNAL SERVER ERROR
        """

        enable_monitoring_data = {'VirtualMachineID': self.ctx_in['vm_uuid'],
                                  'VirtualMachineHostName': self.ctx_in['vm_hostname'],
                                  'VirtualMachineIPAddress': self.ctx_in['vm_ip']
                                  }
        logger.info(enable_monitoring_data)
        try:
            enable_monitoring_resp = req.post(TAS_ENABLE_MONITORING.format(self.ctx_in['tas_ip']),
                                              json=enable_monitoring_data)
            self.ctx_out = True

        except Exception as e:
            logger.info("Exception occurred while calling Enable Monitoring API. \n "
                        "Monitoring could not be enabled.\nException: %s" % e)
            self.ctx_out = False
            raise Exception("Exception: %s" % e)

        response_code = enable_monitoring_resp.status_code
        logger.info(enable_monitoring_resp.content)
        logger.info(response_code)
        self.ctx_out = response_code
        return response_code

    def run_test(self):
        rc = self.test_execute_enable_monitoring()
        logger.info("Status Code = %s" % rc)
        return rc

    def _finalize_context(self):
        assert self.ctx_out == 200, 'Could not enable backup'
