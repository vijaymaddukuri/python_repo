from auc.baseusecase import BaseUseCase
from robot.api import logger
from utils.SaltUtils import SALTUtil


class RunSaltStateNVerify(BaseUseCase):
    def test_run_salt_state_n_verify(self):
        """
        Function to verify VM service
        (Installation Status and Uninstall service)
        Function returns PASS or FAIL
        """
        self.login_type = self.ctx_in['login_type']
        self.state_file = self.ctx_in['state_file']
        self.service_resp_str = self.ctx_in['service_resp_str']
        self.vm_minion_id = self.ctx_in['vm_minion_id']

        saltobj = SALTUtil()
        self.ctx_out = saltobj.execute_salt_state(self.login_type,
                                                  self.state_file,
                                                  self.service_resp_str,
                                                  self.vm_minion_id)
        return self.ctx_out

    def run_test(self):
        result = self.test_run_salt_state_n_verify()
        logger.info("VM service status RESULT = %s" % result)
        return result

    def _finalize_context(self):
        assert self.ctx_out == "PASS", "Could not perform the operation on VM"
