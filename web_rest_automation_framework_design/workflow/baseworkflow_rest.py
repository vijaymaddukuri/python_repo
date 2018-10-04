
from auc import (TestVsRestapi, StartSession)
from utils.context import DataContext


class BaseWorkflow(object):
    """
    In this class we need to define all procedures,
    which are going to use in robot file
    """

    # Robot Framework to share the common testcase
    ROBOT_LIBRARY_SCOPE = 'Test Suite'

    def __init__(self, ctx=None):
        """
        Step 1: Create variables for both golbal and local yaml files to store data
        Step 2: Passes the variables names to DataContext proc to assign values
        :param ctx:
        """
        # Step 1: Create variables for both golbal and local yaml files to store data
        self._GC_TAG = 'GC'
        self._WORKFLOW_TAG = 'WORKFLOW'

        # Step 2: Passes the variables names to DataContext proc to assign values
        if not ctx or not hasattr(ctx, self._GC_TAG):
            self.ctx = DataContext(None, self._GC_TAG)
            self.ctx.update_context(None, self._WORKFLOW_TAG)

        self.wf_context = getattr(self.ctx, self._WORKFLOW_TAG)
        self.gc_context = getattr(self.ctx, self._GC_TAG)

    def apply_settings_from_files(self, global_file, *workflow_files):
        """
        Description: Collects the data from each YAML file and forms the dictionary
        Args:
        :param global_file: generic yaml file path
        :param workflow_files: Path of Specific yaml file
        :return: Dictionary with all the parameters
        """
        self.ctx.update_context(global_file, self._GC_TAG)

        for yaml_file in workflow_files:
            # YAML Data in all files is appended to the dictionary
            self.ctx.update_context(yaml_file, self._WORKFLOW_TAG)

    def reset_settings(self):
        """
        Description: At the end of the test, reset the variables to none
        :return: None
        """
        self.wf_context = None
        self.gc_context = None
        self.ctx = None

    def start_rest_session(self):
        """
        Description: Start Rest session
        :return: Rest session object
        """
        StartSession(
            self.start_rest_session.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context).run()

    def test_virtustream_api(self):
        """
        Description: Get VM ID with template name
        :return: Returns the Virtual machine ID
        """
        TestVsRestapi(
            self.test_virtustream_api.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()