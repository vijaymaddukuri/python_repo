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
from fbdl_e2e.auc.uimap.shared import MainPage
from fbdl_e2e.workflow import Context


class AccessWorkspace(BaseUseCase):
    """
    Data scientist accesses created workspace
    """

    def setUp(self):
        key = 'created_workspace_names'
        Context.validate([key])
        _ws_name = Context.get(key)[-1]

        self.main_page = MainPage(workspace_name=_ws_name)

    def test_view_workspace(self):
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

        self.assertTrue(
            self.main_page.lblWorkspace.exists(),
            msg=_formatter(
                step='Load Workspace Details page'))

    def runTest(self):
        self.test_view_workspace()
