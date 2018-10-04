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
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage

from fbdl_e2e.workflow import Context


class ValidateUserPermission(BaseUseCase):
    """
    Validate the current user's permission within specific workspace
    """

    def setUp(self):
        """
        Make sure the current user is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.lstCollaborators.exists():
            key = 'created_workspace_names'
            Context.validate([key])
            self._ws_name = list(Context.get(key))[-1]

            self.__navigate_to_workspace_details_page(self._ws_name)

    def test_user_permission(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        _current_username = self.details_page.lblCurrentUserAccount.value

        role_dict = {
            'is_manager': _current_username in self.details_page.get_managers(),
            'is_developer': _current_username in self.details_page.get_developers(),
        }

        if role_dict.get('is_manager'):
            self.__validate_manager_permission(_current_username)
        elif role_dict.get('is_developer'):
            self.__validate_developer_permission()
        else:
            self.assertIsNotNone(
                _current_username,
                msg=_formatter(step='Validate user has logged in'))

            self.assertNotIn(
                _current_username,
                self.details_page.get_collaborators(),
                msg=_formatter(
                    step='Viewer is not shown on the Collaborators panel'))

    def runTest(self):
        self.test_user_permission()

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

    def __validate_manager_permission(self, mgr_name):
        _formatter = 'Validating manager\'s permission: "{item}" - FAILED'.format

        self.assertTrue(
            self.details_page.btnAddMember.enabled,
            msg=_formatter(
                item='Add Members button is enabled'))

        self.assertIsNotNone(
            self.details_page.edit_toggle_button,
            msg=_formatter(item='Edit button is visible'))

        self.__toggle_edit_mode(on=True)

        self.assertIsNone(
            self.details_page.get_delete_button_by_name(mgr_name),
            msg=_formatter(item='Delete button is invisible to ' + mgr_name))

        for user in self.details_page.get_collaborators()[::-1]:
            if user.lower() != mgr_name.lower():
                self.assertTrue(
                    self.details_page.get_delete_button_by_name(user).is_enabled(),
                    msg=_formatter(item='Delete button is visible to ' + user))

                break

        self.__toggle_edit_mode(on=False)

    def __validate_developer_permission(self):
        _formatter = 'Validating developer\'s permission: "{item}" - FAILED'.format

        self.assertFalse(
            self.details_page.btnAddMember.exists(),
            msg=_formatter(
                item='Add Members button is invisible'))

        self.assertIsNone(
            self.details_page.edit_toggle_button,
            msg=_formatter(
                item='Validate Edit button is invisible'))

    def __toggle_edit_mode(self, on=False):
        _formatter = 'Switching collaborator edit mode to: "{mode}" - FAILED'.format

        _state_key = 'on' if on else 'off'
        _text = {
            'on': ['cancel', 'done'],
            'off': ['edit'],
        }

        _toggleEdit = self.details_page.edit_toggle_button
        self.assertIsNotNone(
            _toggleEdit, msg=_formatter(mode=_state_key))

        if _toggleEdit.text.lower().strip() not in _text.get(_state_key):
            _toggleEdit.click()
