"""
Python file to Execute Playbook
"""
from ozone.auc.executables.baseusecase import BaseUseCase
from robot.api import logger


class ExecutePlaybook(BaseUseCase):
    """
    Execute Playbook
    """

    def execute_playbook(self):
        """"
        To Execute Playbook
        """
        self.status = self.ozone_session.execute_ansible_job(self.project_name, self.playbook)

    def runTest(self):
        # Actual method call to run the Test
        self.execute_playbook()

    def _validate_input_args(self, **kwargs):
        self.section = kwargs.get('section')

    def _validate_context(self):
        # Validating and mapping the variables taken from the context
        if self.ctx_in:
            assert self.ctx_in.ozone_session, 'Ozone session is None'
            self.ozone_session = self.ctx_in.ozone_session

            self.execute_playbook_details = getattr(self.ctx_in, self.section)
            self.project_name = self.execute_playbook_details.project_name
            self.playbook = self.execute_playbook_details.playbook_details.__dict__
            
    def _finalize_context(self):
        if self.status:
            logger.info('Execute Playbook Successful', False, True)
        else:
            logger.error('Execute Playbook Failed')
            raise AssertionError, 'Execute Playbook Failed'