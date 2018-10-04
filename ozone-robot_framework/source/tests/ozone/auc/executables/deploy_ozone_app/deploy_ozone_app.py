"""
Python file to Deploy Ozone Machine
"""
from tests.ozone.auc.executables.baseusecase import BaseUseCase
from robot.api import logger


class DeployOzoneVM(BaseUseCase):
    """
    Deploys the Ozone Machine
    """

    def deploy_ozone_machine(self):
        """"
        To deploy ozone machine
        """
        self.deployment_status = self.deployment_session.deployOzonevApp(self.vcenter_details,
                                        self.ova_details, self.timeout)

    def runTest(self):
        # Actual method call to run the Test
        self.deploy_ozone_machine()

    def _validate_context(self):
        # Validating and mapping the variables taken from the context
        if self.ctx_in:
            assert self.ctx_in.deployment_session, 'Deployment session is None'
            self.deployment_session = self.ctx_in.deployment_session
            self.vcenter_details = {}
            self.vm_details = {}
            self.ova_details = {}

            self.deploy_ozone = self.ctx_in.deploy_ozone_vApp
            assert hasattr(self.deploy_ozone, 'vcenter_details') , 'vcenter details not provided'
            self.vcenter_details['vCenterIPAddress'] = self.deploy_ozone.vcenter_details.vCenterIPAddress
            self.vcenter_details['vCenterUsername'] = self.deploy_ozone.vcenter_details.vCenterUsername
            self.vcenter_details['vCenterPassword'] = self.deploy_ozone.vcenter_details.vCenterPassword
            self.vcenter_details['datastore'] = self.deploy_ozone.vcenter_details.datastore
            self.vcenter_details['cluster'] = self.deploy_ozone.vcenter_details.cluster
            self.vcenter_details['hostName'] = self.deploy_ozone.vcenter_details.hostName
            self.vcenter_details['vCenterPort'] = self.deploy_ozone.vcenter_details.vCenterPort
            self.vcenter_details['dataCenter'] = self.deploy_ozone.vcenter_details.dataCenter
            self.vcenter_details['resourcePool'] = self.deploy_ozone.vcenter_details.resourcePool

            assert hasattr(self.deploy_ozone, 'ova_details'), 'ova details not provided'
            self.ova_details['vmName'] = self.deploy_ozone.ova_details.vmName
            self.ova_details['network'] = self.deploy_ozone.ova_details.network
            self.ova_details['ovaPath'] = self.deploy_ozone.ova_details.ovaPath
            self.ova_details['masterIP'] = self.deploy_ozone.ova_details.masterIP
            self.ova_details['masterFQDN'] = self.deploy_ozone.ova_details.masterFQDN
            self.ova_details['workerIP'] = self.deploy_ozone.ova_details.workerIP
            self.ova_details['workerFQDN'] = self.deploy_ozone.ova_details.workerFQDN
            self.ova_details['gateway'] = self.deploy_ozone.ova_details.gateway
            self.ova_details['netmask'] = self.deploy_ozone.ova_details.netmask
            self.ova_details['dns'] = self.deploy_ozone.ova_details.dns

            assert hasattr(self.deploy_ozone, 'timeout'), 'timeout not provided'
            self.timeout = self.deploy_ozone.timeout

    def _finalize_context(self):
        if self.deployment_status:
            logger.info('Deploy Ozone VM Successful', False, True)
        else:
            logger.error('Deploy Ozone VM Failed')
            raise AssertionError, 'Deploy Ozone VM Failed'