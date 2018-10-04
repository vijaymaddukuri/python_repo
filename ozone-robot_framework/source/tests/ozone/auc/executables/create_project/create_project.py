"""
Python file to Create Project
"""
from ozone.auc.executables.baseusecase import BaseUseCase
from robot.api import logger


class CreateProject(BaseUseCase):
    """
    Create Project
    """

    def create_project(self):
        """"
        To Create Project
        """
        self.status = self.ozone_session.create_project(self.project_details)

    def runTest(self):
        # Actual method call to run the Test
        self.create_project()

    def _validate_context(self):
        # Validating and mapping the variables taken from the context
        if self.ctx_in:
            assert self.ctx_in.ozone_session, 'Ozone session is None'
            self.ozone_session = self.ctx_in.ozone_session
            self.project_details = {}

            self.create_project_details = self.ctx_in.create_project
            self.project_details['name'] = self.create_project_details.name
            self.project_details['type'] = self.create_project_details.type
            
    def _finalize_context(self):
        if self.status:
            logger.info('Create Project Successful', False, True)
        else:
            logger.error('Create Project Failed')
            raise AssertionError, 'Create Project Failed'