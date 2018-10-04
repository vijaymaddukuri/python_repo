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

import random
import string
import time

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, ServicePage
from fbdl_e2e.workflow import Context


class DeployTools(BaseUseCase):
    """
    Data scientist deploys tools into a workbench
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

        key = 'tools_to_be_deployed'
        Context.validate([key])
        self.tools = Context.get(key)

        self.vm_ip_address = '127.0.0.1'

    def test_deploy_tools_into_workbench(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        # Wait for 10 minutes in case the workbench VM is being deployed
        _now = time.time()
        _timeout_mins = 10 * 60

        while (_timeout_mins > (time.time() - _now))\
                and (len(self.details_page.get_deployed_workbenches()) < 1):
            time.sleep(5)

        _workbenches = self.details_page.get_deployed_workbenches_elements()
        self.assertNotEqual(
            len(_workbenches), 0,
            msg=_formatter(step='Validate default workbench'))

        _workbenches[0].find_element_by_tag_name('a').click()

        if self.details_page.lblSSH.exists():
            self.vm_ip_address = self.details_page \
                .lblSSH.value.split()[-1].split('@')[-1]

        self.assertTrue(
            self.details_page.btnAddServices.enabled,
            msg=_formatter(step='Navigate to Services page'))
        self.details_page.btnAddServices.click()

        self.svc_page = ServicePage()

        self.assertGreaterEqual(
            len(self.svc_page.dac_svc_list), 1,
            msg=_formatter(step='Validate available DAC services (tools)'))

        deployed_tools = []
        for tool in self.tools:
            _name = tool.get('name')
            _instance = tool.get('instance')

            if _instance in self.svc_page.get_deployed_services():
                deployed_tools.append(tool)

                continue

            if _instance not in self.svc_page.get_deploying_services():
                # region Resolve bug - TAF-418
                # randomly generate suffix for tool instance
                _suffix = ''.join(random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits)
                                  for _ in range(random.randint(5, 10)))

                _instance += _suffix

                tool['instance'] = _instance
                # endregion

                self.__deploy_tool(_name, _instance)

                # Workaround for refreshing the application set sidebar
                time.sleep(5)
                self.svc_page.btnBackToWorkspaceDetails.click()
                time.sleep(5)
                self.details_page.btnAddServices.click()
                # Workaround - END

                self.assertTrue(
                    self.svc_page.lblDeployedServices.exists(),
                    msg=_formatter(step='Validate deployed panel'))

            _now = time.time()
            _timeout_mins = 60 * 60 # Wait for one hour

            while (_timeout_mins > (time.time() - _now)) and (
                    (_instance not in self.svc_page.get_deployed_services()) or (
                        _instance in self.svc_page.get_deploying_services()
                    )):
                time.sleep(5)

            self.assertIn(
                _instance, self.svc_page.get_deployed_services(),
                msg=_formatter(step='Validate deployed tool - %s' % _instance))

            deployed_tools.append(tool)

        Context.set('deployed_tools', deployed_tools)

        self.assertTrue(
            self.svc_page.btnBackToWorkspaceDetails.enabled,
            msg=_formatter(step='Navigate back to Workspace Details page'))

        self.svc_page.btnBackToWorkspaceDetails.click()

        _tools = self.details_page.get_deployed_services()

        [self.assertIn(
            tool.get('instance'), _tools,
            msg=_formatter(step='Validate deployed tool - %s'
                                % tool.get('instance')))
         for tool in deployed_tools]

    def runTest(self):
        self.test_deploy_tools_into_workbench()

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

    def __deploy_tool(self, tool_name, tool_instance):
        _formatter = 'Deploying Tool: "{tool}" - FAILED'.format

        self.svc_page.page_down_to_the_bottom()
        btn_deploy = self.svc_page.get_dac_deploy_button(tool_name)

        self.assertIsNotNone(
            btn_deploy,
            msg=_formatter(tool=tool_name))
        self.assertTrue(
            btn_deploy.is_enabled(),
            msg=_formatter(tool=tool_name))
        btn_deploy.click()

        self.assertTrue(
            self.svc_page.frmDeployDacApp.exists(),
            msg=_formatter(tool=tool_name)
        )

        self.assertEquals(
            self.vm_ip_address,
            self.svc_page.txtTargetVM.current.get_attribute('value'),
            msg=_formatter(tool=tool_name)
        )

        if not self.svc_page.txtClusterName.exists():
            self.assertTrue(
                self.svc_page.txtAssetVisibleName.exists(),
                msg=_formatter(tool=tool_name))

            self.svc_page.txtAssetVisibleName.set(tool_instance)
        else:
            self.svc_page.txtClusterName.set(tool_instance)

        if not self.svc_page.btnDacDeploy.enabled \
                and self.svc_page.txtAssetVisibleName.exists():
            self.svc_page.txtAssetVisibleName.set(tool_name)

        self.assertTrue(
            self.svc_page.btnDacDeploy.enabled,
            msg=_formatter(tool=tool_name))

        self.svc_page.btnDacDeploy.click()
