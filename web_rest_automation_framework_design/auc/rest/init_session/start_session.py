from auc.baseusecase import BaseUseCase
from utils.service.restlibrary import RestLib


class StartSession(BaseUseCase):
    def start_session(self):
        """
        Description: Creates REST session object
        :return: returns REST object
        """
        self.rest_session = RestLib()

    def run_test(self):
        self.start_session()

    def _validate_context(self):
        pass

    def _finalize_context(self):
        """
        :return: returns the session object
        """
        setattr(self.ctx_out, 'session', self.rest_session)