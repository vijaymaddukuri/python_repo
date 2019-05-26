import sys
from auc.baseusecase import BaseUseCase
from robot.api import logger
from utils.SSHUtils import SSHUtil
from utils.GetYamlValue import GetYamlValue
from os.path import dirname, abspath

current_dir = dirname(dirname(abspath(__file__)))
sys.path.append(current_dir)


class CleanupMonitoring(BaseUseCase):
    def test_cleanup_monitoring(self):
        """
            Function to Cleanup/Uninstall Monitoring on the target VM.

            :return:
            True  : Cleanup done successfully
            False : Cleanup failed
        """
        self.config = GetYamlValue()

        sm_ip = self.config.get_config('SALT_MASTER_DETAILS', 'SM_IP')
        sm_user = self.config.get_config('SALT_MASTER_DETAILS', 'SM_SSH_USER')
        sm_pwd = self.config.get_config('SALT_MASTER_DETAILS', 'SM_SSH_PWD')
        minion_hostname = self.ctx_in['minion_hostname']
        command_uninstall = "salt '{}' state.apply nimsoft/nimldr/uninstall".format(minion_hostname)
        command_cleanup = "salt '{}' state.apply nimsoft/nimldr/cleanup".format(minion_hostname)
        try:
            ssh_obj = SSHUtil(sm_ip, sm_user, sm_pwd)
            result_uninstall = ssh_obj.execute_command(command_uninstall)
            logger.info("Cleaning up the Nimsoft Installation")
            result_cleanup = ssh_obj.execute_command(command_cleanup)
            status = True if result_cleanup and result_uninstall else False
            self.ctx_out = True
            return status

        except(IOError, ValueError) as e:
            logger.debug("Exception while connecting to target VM,Exception: %s" % e)

    def run_test(self):
        status = self.test_cleanup_monitoring()
        return status

    def _finalize_context(self):
        assert self.ctx_out == True, 'Could not finish cleanup'





