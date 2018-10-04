#  Copyright 2016 EMC GSE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, ServicePage, ToolsPage
from fbdl_e2e.workflow import Context


class DeployServices(BaseUseCase):
    """
    Data Scientist deploys services to workspace
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.btnAddServices.enabled:
            key = 'created_workspace_names'
            Context.validate([key])
            _ws_name = list(Context.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        key = 'services_to_be_deployed'
        Context.validate([key])
        self._services = Context.get(key)

        self.svc_page = ServicePage()

    def test_deploy_pcf_services(self):
        """
        Deploy services with specified instances
        """
        _formatter = 'Running on step: "{step}" - FAILED'.format

        _DEPLOY_SVC_ALLOWED = self.details_page.lblCurrentUserAccount.value in \
                              self.details_page.get_collaborators()

        self.assertTrue(
            self.details_page.btnAddServices.enabled,
            msg=_formatter(step='Navigate to Services page'))
        self.details_page.btnAddServices.click()

        self.assertGreaterEqual(
            len(self.svc_page.pcf_svc_list),
            len(self._services),
            msg=_formatter(step='Validate available PCF services'))

        deployed_pcf_services = []
        for service in self._services:
            _name = service.get('name')
            _instance = service.get('instance')
            self.__deploy_service(_name, _instance)

            if not _DEPLOY_SVC_ALLOWED:
                self.assertTrue(
                    self.svc_page.lblAlertNotificationMsg.exists(),
                    msg=_formatter(step='No permission to deploy service')
                )

                return

            _now = time.time()
            _timeout_mins = 10 * 60

            while (_timeout_mins > (time.time() - _now)) and (
                    (_instance not in self.svc_page.get_deployed_services()) or (
                        _instance in self.svc_page.get_deploying_services()
                    )):
                time.sleep(5)

            self.assertTrue(
                self.svc_page.lblDeployedServices.exists(),
                msg=_formatter(step='Validate deployed service panel'))

            self.assertIn(
                _instance, self.svc_page.get_deployed_services(),
                msg=_formatter(step='Validate deployed service - %s'
                                    % _instance))

            deployed_pcf_services.append(service)

        self.assertTrue(
            self.svc_page.btnBackToWorkspaceDetails.enabled,
            msg=_formatter(step='Navigate back to Workspace Details page'))

        self.svc_page.btnBackToWorkspaceDetails.click()

        _services = self.details_page.get_deployed_services()

        [self.assertIn(
            service.get('instance'), _services,
            msg=_formatter(step='Validate deployed service in workspace page - %s'
                                % service.get('instance')))
         for service in deployed_pcf_services]

        self.details_page.btnShowSVCDetails.click()

        self.tools_page = ToolsPage()

        self.assertTrue(
            self.tools_page.tools_container.exists(),
            msg=_formatter(step='Validate deployed services on detailed list'))

        [self.assertIn(
            service.get('instance'),
            self.tools_page.get_service_instances(),
            msg=_formatter(step='Validate deployed service instance:%s'
                                % service.get('instance')))
         for service in deployed_pcf_services]

        Context.set('deployed_services', deployed_pcf_services)

        self.svc_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_deploy_pcf_services()

    def __navigate_to_workspace_details_page(self, ws_name):
        self.main_page = MainPage(workspace_name=ws_name)

        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.assertTrue(
            self.main_page.lnkWorkspace.exists(),
            msg=_formatter(
                step='Navigate to My Workspace page'))
        self.main_page.lnkWorkspace.click()

        self.assertTrue(
            self.main_page.lnkTargetWorkspace.enabled,
            msg=_formatter(
                step='Navigate to Workspace Details page'))
        self.main_page.lnkTargetWorkspace.click()

    def __deploy_service(self, svc_name, svc_instance_name):
        _formatter = 'Deploying service: "{svc}" - FAILED'.format

        btn_deploy = self.svc_page.get_pcf_deploy_button(svc_name)
        self.assertIsNotNone(
            btn_deploy, msg=_formatter(svc=svc_name))
        btn_deploy.click()

        self.assertTrue(
            self.svc_page.txtPcfInstance.exists(),
            msg=_formatter(svc=svc_instance_name))
        self.svc_page.txtPcfInstance.set(svc_instance_name)

        self.assertTrue(
            self.svc_page.btnPcfDeploy.enabled,
            msg=_formatter(svc=svc_name))
        self.svc_page.btnPcfDeploy.click()
