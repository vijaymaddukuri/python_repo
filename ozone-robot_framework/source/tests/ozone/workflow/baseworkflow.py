from ehc_auto_install.utils.context import DataContext
from robot.api import logger
from tests.ozone.auc.executables import StartOzoneDeploymentSession, StartOzoneSession, DeployOzoneVM, ConfigureOzoneVM, \
    CreateProject, DeleteProject, UpdateVariables, ExecutePlaybook, ReadExcelData


class BaseWorkflow(object):

    ROBOT_LIBRARY_SCOPE = 'Test Suite'

    def __init__(self, ctx=None):
        self._GC_TAG = 'GC'
        self._WORKFLOW_TAG = 'WORKFLOW'

        if not ctx or not hasattr(ctx, self._GC_TAG):
            self.ctx = DataContext(None, self._GC_TAG)
            self.ctx.update_context(None, self._WORKFLOW_TAG)

        self.wf_context = getattr(self.ctx, self._WORKFLOW_TAG)
        self.gc_context = getattr(self.ctx, self._GC_TAG)

    def apply_settings_from_files(self, global_file, *workflow_files):
        self.ctx.update_context(global_file, self._GC_TAG)
        for yaml_file in workflow_files:
            self.ctx.update_context(yaml_file, self._WORKFLOW_TAG)

    def reset_settings(self):
        self.wf_context = None
        self.wf_context = None

    def read_excel_data(self):
        ReadExcelData(
            self.read_excel_data.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def start_ozone_session(self):
        StartOzoneSession(
            self.start_ozone_session.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def start_vcenter_session(self):
        StartOzoneDeploymentSession(
            self.start_vcenter_session.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def deploy_ozone_vapp(self):
        DeployOzoneVM(
            self.deploy_ozone_vapp.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def configure_ozone_vapp(self):
        ConfigureOzoneVM(
            self.configure_ozone_vapp.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def create_project(self):
        CreateProject(
            self.create_project.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def delete_project(self):
        DeleteProject(
            self.delete_project.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def update_project_variables(self):
        UpdateVariables(
            self.update_project_variables.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
        ).run()

    def execute_prevalidation_playbook(self):
        kw = {'section': 'execute_prevalidation_playbook'}
        ExecutePlaybook(
            self.execute_prevalidation_playbook.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
            **kw
        ).run()

    def execute_main_playbook(self):
        kw= {'section' : 'execute_main_playbook'}
        ExecutePlaybook(
            self.execute_main_playbook.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context,
            **kw
        ).run()






