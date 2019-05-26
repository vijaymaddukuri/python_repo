import sys
from auc.baseusecase import BaseUseCase
from robot.api import logger
from utils.SSHUtils import SSHUtil


class ValidateMonitoring(BaseUseCase):

    def validate_enable_monitor(self):
        """
        Function to Validate Enable Monitoring on the target VM.

        :return:
            Function returns status based on Monitoring/Nimbus service status :
                1: ACTIVE
                0: OTHERWISE
        """
        host = self.ctx_in['target_host']
        user = self.ctx_in['user']
        password = self.ctx_in['password']

        try:
            con = SSHUtil(host, user, password)
            result = con.execute_command('service nimbus status')
            status = 1 if "active" in result['output'] else 0
            self.ctx_out = True
            return status

        except(IOError, ValueError) as e:
            logger.debug("Exception while connecting to target VM,Exception: %s" % e)

    def run_test(self):
        status = self.validate_enable_monitor()
        return status

    def _finalize_context(self):
        assert self.ctx_out == 1
