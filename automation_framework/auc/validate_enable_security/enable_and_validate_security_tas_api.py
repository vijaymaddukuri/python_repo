from auc.baseusecase import BaseUseCase
from conf.restConstants import *
from robot.api import logger
from utils.SSHUtils import SSHUtil


class ExecuteTasEnableSecurityAPI(BaseUseCase):
    def test_execute_tas_enable_security_api(self):
        """
        Function to enable the security for a given VM from TAS.
        Returns:
            Function returns PASS or FAIL
        """
        self.tas_ip = self.ctx_in['tas_ip']
        self.tas_user = self.ctx_in['tas_user']
        self.tas_pwd = self.ctx_in['tas_pwd']
        self.vm_hostname = self.ctx_in['vm_hostname']
        self.vm_ip = self.ctx_in['vm_ip']
        self.vm_id = self.ctx_in['vm_id']
        self.vm_rid = self.ctx_in['vm_rid']
        self.task_id = self.ctx_in['task_id']
        self.linux_policy_id = self.ctx_in['linux_policy_id']
        self.win_policy_id = self.ctx_in['win_policy_id']
        self.tas_header = JSON_HEADER
        self.nat_ip = self.ctx_in['nat_ip']
        self.nat_user = self.ctx_in['nat_user']
        self.nat_pwd = self.ctx_in['nat_pwd']
        self.nat_tmp_location = '/tmp/'

        # Connect to NAT machine
        self.nat_ssh_obj = SSHUtil(host=self.nat_ip, username=self.nat_user,
                                   password=self.nat_pwd, timeout=10)

        logger.info('############################')
        logger.info("Validating TAS Enable SECURITY API")
        url = TAS_API_ENABLE_SECURITY.format(self.tas_ip)
        security_result = 'PASS'
        cmd = TAS_SECURITY_REQUEST % (url,
                                      self.linux_policy_id,
                                      self.win_policy_id,
                                      self.vm_hostname,
                                      self.vm_ip,
                                      self.vm_id,
                                      self.vm_rid,
                                      self.task_id)

        command = 'no_proxy="{}" && {}'.format(self.ctx_in['tas_ip'], cmd)
        logger.info("command: {}".format(command))
        result = self.nat_ssh_obj.execute_command(command)

        logger.info("Output of Enable security command")
        logger.info(result['output'])

        if "HTTP/1.1 200 OK" in result['output']:
            logger.info("Enable security API is initiated successfully from TAS")
        else:
            message = "Failed to enable security from TAS."
            logger.info(message)
            security_result = 'FAIL'
            logger.debug(message)
            logger.debug(result['output'])

        self.ctx_out = security_result
        return security_result

    def run_test(self):
        tas_result = self.test_execute_tas_enable_security_api()
        logger.info("TAS Enable SECURITY API RESULT = %s" % tas_result)
        return tas_result

    def _finalize_context(self):
        assert self.ctx_out == "PASS", "Could not initiate TAS enable security API"
