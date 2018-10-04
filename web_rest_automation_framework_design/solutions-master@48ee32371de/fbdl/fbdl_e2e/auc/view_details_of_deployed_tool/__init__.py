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
from fbdl_e2e.workflow import Context


class ViewDetailsOfDeployedTool(BaseUseCase):
    """
    View the details (the fields listed on the sidebar) of the deployed tools
    """

    def setUp(self):
        """
        Make sure the current user is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.btnShowSVCDetails.exists():
            key = 'created_workspace_names'
            Context.validate([key])
            self._ws_name = list(Context.get(key))[-1]

            self.__navigate_to_workspace_details_page(self._ws_name)

        key = 'deployed_tools'
        Context.validate([key])
        self._lstTools = Context.get(key)

    def test_viewing_deployed_tool(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertGreater(
            len(self._lstTools), 0,
            msg=_formatter(step='Validate context of deployed tools'))

        self._tool = self._lstTools.pop(-1)
        _tool_instance = self._tool.get('instance')
        self.tool_page = ToolsPage()

        self.details_page.btnShowSVCDetails.click()

        self.assertTrue(
            self.tool_page.tools_container.exists(),
            msg=_formatter(step='Validate deployed tools on detailed list'))

        _tools = [tool.text.split('\n')[0]
                  for tool in self.tool_page.tools_list]

        self.assertIn(
            _tool_instance,
            _tools,
            msg=_formatter(step='Validate the latest deployed tool'))

        _btnExpand = self.tool_page.get_tool_expand_button(_tool_instance)
        self.assertIsNotNone(
            _btnExpand,
            msg=_formatter(step='Show detailed information of the deployed tool'))
        _btnExpand.click()

        _tool_fields = Context.get('detailed_fields_of_tool') or []

        for field in _tool_fields:
            self._tool[field] = self.tool_page.get_tool_info_by_key(field)

        self._lstTools.append(self._tool)
        Context.set('deployed_tools', self._lstTools)

        self.tool_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_viewing_deployed_tool()

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
