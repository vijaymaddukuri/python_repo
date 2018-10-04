"""
Python file to Update Variables
"""
from ozone.auc.executables.baseusecase import BaseUseCase
from robot.api import logger


class UpdateVariables(BaseUseCase):
    """
    Update Variables
    """

    def update_variables(self):
        """"
        To Update Variables
        """
        self.status = self.ozone_session.update_ansible_variables(self.project_name, self.json_path)

    def runTest(self):
        # Actual method call to run the Test
        self.update_variables()

    def _validate_context(self):
        # Validating and mapping the variables taken from the context
        if self.ctx_in:
            assert self.ctx_in.ozone_session, 'Ozone session is None'
            self.ozone_session = self.ctx_in.ozone_session
            self.project_details = {}

            self.update_variable_details = self.ctx_in.update_variables
            self.project_name = self.update_variable_details.project_name
            self.json_path = self.update_variable_details.json_path
            
    def _finalize_context(self):
        if self.status:
            logger.info('Update Variables Successful', False, True)
        else:
            logger.error('Update Variables Failed')
            raise AssertionError, 'Update Variables Failed'