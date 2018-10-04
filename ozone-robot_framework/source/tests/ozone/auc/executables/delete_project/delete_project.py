"""
Python file to Delete Project
"""
from ozone.auc.executables.baseusecase import BaseUseCase
from robot.api import logger


class DeleteProject(BaseUseCase):
    """
    Delete Project
    """

    def delete_project(self):
        """"
        To Delete Project
        """
        self.status = self.ozone_session.delete_project(self.project_name)

    def runTest(self):
        # Actual method call to run the Test
        self.delete_project()

    def _validate_context(self):
        # Validating and mapping the variables taken from the context
        if self.ctx_in:
            assert self.ctx_in.ozone_session, 'Ozone session is None'
            self.ozone_session = self.ctx_in.ozone_session
            self.project_details = {}

            self.delete_project_details = self.ctx_in.delete_project
            self.project_name = self.delete_project_details.name

    def _finalize_context(self):
        if self.status:
            logger.info('Delete Project Successful', False, True)
        else:
            logger.error('Delete Project Failed')
            raise AssertionError, 'Delete Project Failed'