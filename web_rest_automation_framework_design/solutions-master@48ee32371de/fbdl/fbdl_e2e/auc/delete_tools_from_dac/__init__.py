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

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, ServicePage

from fbdl_e2e.workflow import Context


class DeleteToolsFromDAC(BaseUseCase):
    """
    Data Scientist deletes tools (applications) from DAC (publications)
    """

    def setUp(self):
        """
        Data scientist navigates to the services page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.btnShowSVCDetails.enabled:
            key = 'created_workspace_names'
            Context.validate([key])
            _ws_name = list(Context.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        self.details_page.btnAddServices.click()

        key = 'accepted_tools_queue'

        Context.validate([key])
        self._accepted_tools = Context.get(key)
        self.svc_page = ServicePage()

    def test_delete_tools(self):
        """
        Delete tools from DAC (publications)
        """
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertGreaterEqual(
            len(self.svc_page.dac_svc_list),
            len(self._accepted_tools),
            msg=_formatter(step='Validate available DAC services'))

        for tool in self._accepted_tools[::-1]:
            self.__delete_service(tool)

            self.assertNotIn(
                tool, [item.text.split('\n')[0]
                       for item in self.svc_page.dac_svc_list],
                msg=_formatter(step='Validate the tool is deleted')
            )

            self._accepted_tools.pop(-1)

        Context.set('accepted_tools_queue', self._accepted_tools)

        self.svc_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_delete_tools()

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

    def __delete_service(self, svc_name):
        _formatter = 'Deleting service: "{svc}" - FAILED'.format

        btn_delete = self.svc_page.get_dac_delete_button(svc_name)

        self.assertIsNotNone(
            btn_delete, msg=_formatter(svc=svc_name))
        self.assertTrue(
            btn_delete.is_enabled(),
            msg=_formatter(svc=svc_name))

        btn_delete.click()

        self.assertTrue(
            self.svc_page.lblConfirmDeletion.exists(),
            msg=_formatter(svc=svc_name))

        btn_ok = self.svc_page.get_confirmation_button()

        self.assertIsNotNone(
            btn_ok, msg=_formatter(svc=svc_name))

        self.assertTrue(
            btn_ok.is_enabled(),
            msg=_formatter(svc=svc_name))

        btn_ok.click()
