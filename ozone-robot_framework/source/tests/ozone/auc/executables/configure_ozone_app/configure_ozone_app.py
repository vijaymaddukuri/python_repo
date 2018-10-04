"""
Python file to Configure Ozone Machine
"""
from ozone.auc.executables.baseusecase import BaseUseCase
from robot.api import logger


class ConfigureOzoneVM(BaseUseCase):
    """
    Configures the Ozone Machine
    """

    def configure_ozone_password(self):
        """"
        To configure ozone password
        """
        assert self.ozone_session.config_master_password(self.masterpassword), 'configuring master password failed'
        assert self.ozone_session.config_user_password(self.username, self.oldpassword, self.newpassword), \
            'configuring user password failed'
        assert self.ozone_session.start_service(), 'Ozone service not started'
        assert self.ozone_session.is_set_user_password(self.newpassword), 'User password is not setted'
        assert self.ozone_session.is_set_master_password(), 'Master Password is not setted'


    def configure_ozone_worker(self):
        assert self.deployment_session.configAgent(self.vcenter_details, self.vm_details), 'Configuring Agent Failed'

    def configure_ozone_machine(self):
        self.configure_ozone_password()
        self.configure_ozone_worker()

    def runTest(self):
        # Actual method call to run the Test
        self.configure_ozone_machine()

    def _validate_context(self):
        # Validating and mapping the variables taken from the context
        if self.ctx_in:
            assert self.ctx_in.deployment_session, 'Ozone Deployment session is None'
            assert self.ctx_in.ozone_session, 'Ozone REST Session is None'
            self.deployment_session = self.ctx_in.deployment_session
            self.ozone_session = self.ctx_in.ozone_session
            self.vcenter_details = {}
            self.vm_details = {}

            self.configure_ozone = self.ctx_in.configure_ozone_vApp
            assert hasattr(self.configure_ozone, 'master_details') , 'master details not provided'
            self.masterpassword = self.configure_ozone.master_details.password

            assert hasattr(self.configure_ozone, 'user_details'), 'user details not provided'
            self.username = self.configure_ozone.user_details.username
            self.oldpassword = self.configure_ozone.user_details.oldpassword
            self.newpassword = self.configure_ozone.user_details.newpassword

            assert hasattr(self.configure_ozone, 'vcenter_details'), 'vcenter details not provided'
            self.vcenter_details['host'] = self.configure_ozone.vcenter_details.host
            self.vcenter_details['username'] = self.configure_ozone.vcenter_details.username
            self.vcenter_details['password'] = self.configure_ozone.vcenter_details.password

            assert hasattr(self.configure_ozone, 'worker_vm_details'), 'worker vm details not provided'
            self.vm_details['vmname'] = self.configure_ozone.worker_vm_details.vmname
            self.vm_details['vmusername'] = self.configure_ozone.worker_vm_details.vmusername
            self.vm_details['vmpassword'] = self.configure_ozone.worker_vm_details.vmpassword
            self.vm_details['datacenter'] = self.configure_ozone.worker_vm_details.datacenter
            self.vm_details['folderPath'] = self.configure_ozone.worker_vm_details.folderPath
            self.vm_details['vappname'] = self.configure_ozone.worker_vm_details.vappname

    def _finalize_context(self):
        try:
            assert self.ozone_session.validate_system_service(), 'System Service not working'
            assert self.ozone_session.validate_system_agent(), 'System Agent not working'
            logger.info('Configure Ozone VM Passed')
        except Exception as err:
            logger.error('Configure Ozone VM Failed with {}'.format(err))
            raise AssertionError, 'Configure Ozone VM Failed'