import sys

from auc.run_saltstate_n_verify_response.run_saltstate_n_verify_response import RunSaltStateNVerify

from utils.context import DataContext
from os.path import dirname, abspath

current_dir = dirname(dirname(abspath(__file__)))
sys.path.append(current_dir)


class BaseWorkflowRunSaltStateNVerify(object):
    """
    In this class we are defining all procedures that can be
    commonly used for all services
    """

    def __init__(self, ctx=None):
        """
        Step 1: Create variables for both global and local
        yaml files to store data
        Step 2: Passes the variables names to DataContext
        process to assign values
        Args:
        :param ctx:
        """
        self._GC_TAG = 'GC'
        self._WORKFLOW_TAG = 'WORKFLOW'
        if not ctx or not hasattr(ctx, self._GC_TAG):
            self.ctx = DataContext(None, self._GC_TAG)
            self.ctx.update_context(None, self._WORKFLOW_TAG)

        self.wf_context = getattr(self.ctx, self._WORKFLOW_TAG)
        self.gc_context = getattr(self.ctx, self._GC_TAG)

    def reset_settings(self):
        """
        Description: At the end of the test, reset the variables to none
        :return: None
        """
        self.wf_context = None
        self.gc_context = None
        self.ctx = None

    def generic_run_salt_state_cleanup_or_validate(self, vm_minion_id, login_type,
                                                   state_file, service_resp_str):
        """
        Description: Update the VM service and validate the results
        :param vm_minion_id: VM Minion ID
        :param login_type: remote or local machine
        :param state_file: Salt state file name with path
        :param service_resp_str: String to validate.

        :return: PASS or FAIL
        """
        self.ctx_in = {
                       'vm_minion_id': vm_minion_id,
                       'login_type': login_type,
                       'state_file': state_file,
                       'service_resp_str': service_resp_str
                       }
        result = RunSaltStateNVerify(
            self.generic_run_salt_state_cleanup_or_validate.__name__,
            ctx_in=self.ctx_in, ctx_out="").run()
        return result
