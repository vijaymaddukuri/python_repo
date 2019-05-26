import datetime
import re
import requests as req
import time

from auc.baseusecase import BaseUseCase
from base64 import b64encode
from robot.api import logger
from conf.restConstants import *
from utils.SSHUtils import SSHUtil


class ExecuteMwDecommissionSecurityAPI(BaseUseCase):
    def test_execute_mw_decommission_security_api(self):
        """
        Function to enable the security for a given VM from Middleware.
        Args:
        tenant_id (mandatory): String	tenant  uuid in xstream
        vm_id (mandatory): String    vm uuid in xstream
        hostname (mandatory): String  hostname of the vm
        vm_ip (mandatory): String
        task_id (mandatory): String
        callback_url (mandatory): String
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        self.mw_ip = self.ctx_in['mw_ip']
        self.mw_user = self.ctx_in['mw_user']
        self.mw_pwd = self.ctx_in['mw_pwd']
        self.tenant_id = self.ctx_in['tenant_id']
        self.vm_hostname = self.ctx_in['vm_hostname']
        self.vm_ip = self.ctx_in['vm_ip']
        self.mw_header = JSON_HEADER
        self.swagger_user = self.ctx_in['swagger_user']
        self.swagger_pwd = self.ctx_in['swagger_pwd']
        self.task_id = self.ctx_in['task_id']
        self.vmid = self.ctx_in['vmid']
        self.vmrid = self.ctx_in['vm_rid']
        self.callback_url = self.ctx_in['callback_url']

        userAndPass = '{}:{}'.format(self.swagger_user, self.swagger_pwd)
        convertToBytes = bytes(userAndPass, 'utf-8')
        auth = b64encode(convertToBytes).decode("ascii")
        self.mw_header['Authorization'] = 'Basic %s' % auth

        # Connect to Middlware machine
        self.ssh_obj = SSHUtil(host=self.mw_ip, username=self.mw_user,
                               password=self.mw_pwd, timeout=10)
        logger.info('############################')
        logger.info("Validating MW decommission security API")
        security_result = "PASS"
        decommission_security_data = {'TenantID': self.tenant_id,
                                'VirtualMachineID': self.vmid,
                                'VirtualMachineHostName': self.vm_hostname,
                                'VirtualMachineIPAddress': self.vm_ip,
                                'VirtualMachineRID': self.vmrid,
                                'TaskID': self.task_id,
                                'Callback': self.callback_url
                                }
        try:
            decommission_security_resp = req.post(MIDDLEWARE_API_DECOMMISSION_SECURITY.
                                            format(self.mw_ip),
                                            json=decommission_security_data,
                                            headers=self.mw_header)
        except Exception as e:
            logger.info("Exception occurred while calling Decommission security API. \n "
                        "Security decommissioning did not happen.\nException: %s" % e)
            return 0

        logger.info("Status Code = %s" % decommission_security_resp.status_code)
        logger.info("Message = %s" % decommission_security_resp.text)

        if decommission_security_resp.status_code != 200:
            message = 'Could not access middleware security API', \
                      decommission_security_resp.status_code
            logger.error(message)
            logger.debug(message)
            security_result = "FAIL"
        else:
            logger.info('Can access middleware security API. '
                        'Response code = 200')

        # Validating the worker log
        if decommission_security_resp.status_code == 200:
            logger.info('Waiting for decommission security API to process the request')
            time.sleep(200)
            command = 'tail -n 32 /var/log/middleware/worker.log'
            result = self.ssh_obj.execute_command(command)

            logger.info('############################')
            logger.info("Validating worker log for Middleware to "
                        "tas connectivity")
            if "No route to host" in result['output']:
                message = 'Middleware to tas connectivity failed'
                logger.error(message)
                security_result = "FAIL"
            else:
                logger.info("Communication is proper between TAS and middleware")

            cdate = datetime.datetime.now().strftime("%d/%b/%Y")
            matchObj = re.findall("{}\s\d+\:\d+\:\d+\]\s+ERROR \[\S+\:\d+\] \|\*SECURITY\*\|"
                                  .format(cdate), result['output'])
            if matchObj:
                message = 'Unable to decommission security from middleware.'
                logger.error(message)
                logger.debug(message)
                logger.info(result['output'])
                security_result = "FAIL"
            else:
                logger.info('Decommission security API is Successfully executed')
                logger.info(result['output'])
        else:
            security_result = "FAIL"
        return security_result

    def run_test(self):
        mw_result = self.test_execute_mw_decommission_security_api()
        logger.info("Middleware Decommission SECURITY API RESULT = %s" % mw_result)
        return mw_result

    def _finalize_context(self):
        assert self.ctx_out == "PASS", "Could not initiate decommission security API from Middleware"
