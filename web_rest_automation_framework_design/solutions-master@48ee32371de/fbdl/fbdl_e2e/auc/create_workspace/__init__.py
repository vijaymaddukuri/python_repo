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

import datetime

from robot.api import logger

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.create_workspace.create_workspace_context import CreateWorkSpaceContext
from fbdl_e2e.auc.uimap.shared import MainPage
from fbdl_e2e.auc.uimap.specific import CreateWorkspaceMainPage


class CreateWorkSpace(BaseUseCase):
    """
    Data scientist creates workspace
    """

    def setUp(self):
        CreateWorkSpaceContext.validate()
        self._ws_name = 'auto' + datetime.datetime.now().strftime('%y%m%d%H%M')
        # self._ws_name = CreateWorkSpaceContext.get('to_create_workspace_names')[-1]
        self.home_page = CreateWorkspaceMainPage()
        self.main_page = MainPage(workspace_name=self._ws_name)
        self.main_page.lnkBrand.click()

        self._validate_dict = {'datasets_number': 0, 'tools_number': 0, 'members_number': 1}

        # _credential_queue = CreateWorkSpaceContext.get('credentials_queue')
        # _login_role = _credential_queue[0]['role']
        # if _login_role == 'manager':
        #     self._validate_dict = {'datasets_number': 0, 'tools_number': 0, 'members_number': 1}
        # else:
        #     self._validate_dict = {'datasets_number': 0, 'tools_number': 0, 'members_number': 1}

    def test_create_workspace(self):
        logger.info('Create workspace..', False, True)
        self.assertTrue(self.main_page.lnkWorkspace.enabled,
                        msg='Failed to direct to My Workspaces page.')
        self.main_page.lnkWorkspace.click()
        self.assertTrue(self.home_page.btnAddWorkSpace.exists(),
                        msg='Has no permission to create workspace.')

        if self.__target_workspace_exists(self._ws_name):
            logger.info('Workspace %s already exists!' % self._ws_name, False, True)
        else:
            self.home_page.btnAddWorkSpace.click()
            self.assertTrue(self.home_page.fmCreateWorkSpace.exists(),
                            msg='Failed to pop up create workspace dialog.')
            self.home_page.txtWorkSpaceName.set(self._ws_name)
            self.home_page.btnSave.click()
            self.assertTrue(self.__target_workspace_exists(self._ws_name),
                            msg='Failed to create workspace {}!'.format(self._ws_name))

            result_dict = self.__get_target_ws_attr(self._ws_name)
            self.assertEqual(result_dict['datasets_number'], str(self._validate_dict['datasets_number']),
                             msg='Validate default data sets number')

            # self.assertEqual(result_dict['tools_num'], str(self._validate_dict['tools_number']),
            #                  msg='Validate default tools number')
            self.assertEqual(result_dict['members_num'], str(self._validate_dict['members_number']),
                             msg='Validate default members number')

        # to_create_workspaces = CreateWorkSpaceContext.get('to_create_workspace_names')
        created_workspaces = CreateWorkSpaceContext.get('created_workspace_names')

        # to_create_workspaces.pop()
        created_workspaces.append(self._ws_name)

        # CreateWorkSpaceContext.set('to_create_workspace_names', to_create_workspaces)
        CreateWorkSpaceContext.set('created_workspace_names', created_workspaces)
        import time
        time.sleep(10)

    def runTest(self):
        self.test_create_workspace()

    def __target_workspace_exists(self, ws_name):
        if self.main_page.ws_container.exists():
            self.main_page.page_down_to_the_bottom()
            target_ws = self.main_page.get_target_workspace(ws_name)
            if target_ws:
                return True
        return False

    def __get_target_ws_attr(self, ws_name):
        if self.main_page.ws_container.exists():
            self.main_page.page_down_to_the_bottom()
            target_ws = self.main_page.get_target_workspace(ws_name)
            if target_ws:
                _attr_list = str(target_ws.text).strip().split('\n')
                return {'datasets_number': _attr_list[1], 'tools_num': _attr_list[3], 'members_num': _attr_list[5]}
        return None