"""
Python file to Create Ozone Deployment Session
"""

from ozone.auc.executables.baseusecase import BaseUseCase
from ozone.library import Ozone


class StartOzoneDeploymentSession(BaseUseCase):
    """
    Starts the Ozone Deployment Session
    """

    def start_ozone_session(self):
        """"
        To Start Ozone Deployment Session
        """
        self.vcenter_session = Ozone(self.vcenter_credentials)

    def runTest(self):
        self.start_ozone_session()

    def _validate_context(self):
        self.vcenter_session = None
        if self.ctx_in:
            assert self.ctx_in.vcenter_details.host is not None, 'vcenter hostname is None'
            assert self.ctx_in.vcenter_details.username is not None, 'vcenter username is None'
            assert self.ctx_in.vcenter_details.password is not None, 'vcenter password is None'

        self.vcenter_credentials ={'host' : self.ctx_in.vcenter_details.host,
                              'username': self.ctx_in.vcenter_details.username,
                              'password': self.ctx_in.vcenter_details.password,
                              'portNum': self.ctx_in.vcenter_details.port}



    def _finalize_context(self):
        setattr(self.ctx_out, 'deployment_session', self.vcenter_session)
