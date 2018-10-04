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
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, ToolsPage
from fbdl_e2e.auc.publish_tools.publish_tools_context import PublishToolsContext


class PublishTools(BaseUseCase):
    """
    Data scientist submit a publish request for a DAC tool in my tools page
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        PublishToolsContext.validate()
        self.details_page = WSDetailsPage()
        if not self.details_page.btnShowSVCDetails.enabled:
            key = 'created_workspace_names'
            _ws_name = list(PublishToolsContext.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        self._ws_id = self.details_page.workspace_id
        self._pub_svc = PublishToolsContext.get('registered_tools')[-1]
        self.assertTrue(bool(self._pub_svc), msg='No asset info provided')

    def test_publish_tools_into_dac(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertTrue(self.details_page.btnShowSVCDetails.exists(),
                        msg=_formatter(step='Button show detailed list does not exists!'))
        self.details_page.btnShowSVCDetails.click()

        self.tl_page = ToolsPage()
        self.tl_page.page_down_to_the_bottom()

        self.__publish_tool(self._pub_svc)

        class Object(object):
            pass
        response = Object()
        response.code = '0'
        response.category='app'
        response.guid = ''
        response.name = self._pub_svc
        response.workspace = self._ws_id

        PublishToolsContext.set('submitted_assets', [response])
        _registered_tools = PublishToolsContext.get('registered_tools')
        _registered_tools = _registered_tools.pop(-1)
        PublishToolsContext.set('registered_tools', _registered_tools)

        self.tl_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_publish_tools_into_dac()

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

    def __publish_tool(self, tl_name):
        _formatter = 'Runing on step: "{step}" - FAILED'.format

        btn_publish = self.tl_page.get_tool_publish_button(tl_name)

        self.assertIsNotNone(
            btn_publish, msg=_formatter(step='Get corresponding publish button of tool ' + tl_name))
        btn_publish.click()
        import time
        timeout = 30
        while str(btn_publish.text).strip() == 'Publishing' and (timeout >= 0):
            time.sleep(1)
            timeout -= 1
        self.assertEqual(str(btn_publish.text).strip(), 'Cancel Publication',
                         msg=_formatter(step='Publish tool to DAC'))

