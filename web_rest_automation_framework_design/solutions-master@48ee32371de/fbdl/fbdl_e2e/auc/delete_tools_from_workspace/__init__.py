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
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, ToolsPage
from fbdl_e2e.workflow import Context


class DeleteToolsFromWorkspace(BaseUseCase):
    """
    Data Scientist deletes deployed tools (applications) from workspace
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.btnShowSVCDetails.enabled:
            key = 'created_workspace_names'
            Context.validate([key])
            _ws_name = list(Context.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        if self.details_page.btnShowSVCDetails.exists():
            self.details_page.btnShowSVCDetails.click()

        key = 'tools_to_be_deleted'

        Context.validate([key])
        self._tools = Context.get(key)
        self.tools_page = ToolsPage()

    def test_deleting_tools(self):
        """
        Delete registered / deployed tools from Details page
        """
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertTrue(
            self.tools_page.tools_container.exists(),
            msg=_formatter(step='Loading registered / deployed tools')
        )

        self.assertGreaterEqual(
            len(self.tools_page.tools_list),
            len(self._tools),
            msg=_formatter(step='Validate registered / deployed tools'))

        for tool in self._tools[::-1]:
            self.__delete_tool(tool)

            _now = time.time()
            _timeout = 3 * 60

            while (_timeout > (time.time() - _now))\
                    and (self.tools_page.get_tool_delete_button(tool)):
                time.sleep(5)

            self.assertNotIn(
                tool, [item.text.split('\n')[0]
                       for item in self.tools_page.tools_list],
                msg=_formatter(step='Validate the tool is deleted')
            )

            self._tools.pop(-1)

        Context.set('tools_to_be_deleted', self._tools)
        self.tools_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_deleting_tools()

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

    def __delete_tool(self, tool_name):
        _formatter = 'Deleting tool: "{tool}" - FAILED'.format

        btn_delete = self.tools_page.get_tool_delete_button(tool_name)

        self.assertIsNotNone(
            btn_delete, msg=_formatter(tool=tool_name))
        self.assertTrue(
            btn_delete.is_enabled(),
            msg=_formatter(tool=tool_name))

        btn_delete.click()

        self.assertTrue(
            self.tools_page.lblConfirmDeletion.exists(),
            msg=_formatter(tool=tool_name))

        btn_ok = self.tools_page.get_confirmation_button()

        self.assertIsNotNone(
            btn_ok, msg=_formatter(tool=tool_name))

        self.assertTrue(
            btn_ok.is_enabled(),
            msg=_formatter(tool=tool_name))

        btn_ok.click()
