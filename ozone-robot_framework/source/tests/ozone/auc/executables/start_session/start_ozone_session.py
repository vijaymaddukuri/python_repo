"""
Python file to Start the Ozone REST Session
"""
from tests.ozone.auc.executables.baseusecase import BaseUseCase
from tests.ozone.library import OzoneRestLib


class StartOzoneSession(BaseUseCase):
    """
    Starts the Ozone Session
    """

    def start_ozone_session(self):
        """"
        To Start Ozone Session
        """
        self.ozone_session = OzoneRestLib(*self.ozone_credentials)

    def runTest(self):
        self.start_ozone_session()

    def _validate_context(self):
        self.ozone_session = None
        if self.ctx_in:
            for key, value in self.ctx_in.ozone_details.__dict__.iteritems():
                assert value is not None, '{} is not provided.'.format(key)

            self.ozone_credentials = [self.ctx_in.ozone_details.hostname,
                                    self.ctx_in.ozone_details.email,
                                    self.ctx_in.ozone_details.password]

    def _finalize_context(self):
        setattr(self.ctx_out, 'ozone_session', self.ozone_session)
