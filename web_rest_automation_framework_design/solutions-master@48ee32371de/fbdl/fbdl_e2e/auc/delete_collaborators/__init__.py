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


class DeleteCollaborators(BaseUseCase):
    """
    Admin / Manager deletes collaborators within specific workspace
    """

    def setUp(self):
        """
        Make sure admin / manager is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.lstCollaborators.exists():
            key = 'created_workspace_names'
            Context.validate([key])
            self._ws_name = list(Context.get(key))[-1]

            self.__navigate_to_workspace_details_page(self._ws_name)

        key = 'added_collaborators'
        Context.validate([key])
        self._lstAddedCollaborators = Context.get(key)
        self._collaborators_to_be_deleted = [item.get('username').strip()
                                             for item in self._lstAddedCollaborators]

    def test_deleting_collaborators(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        removed_collaborators = []

        for user in self._collaborators_to_be_deleted:
            self.__delete_collaborator(user)
            self.assertNotIn(
                user, self.details_page.get_collaborators(),
                msg=_formatter(step='Validate deleted collaborator'))
            removed_collaborators.append(user)

        _value = Context.get('added_collaborators')

        # if Context.get('secondary_user') in _value:
        #     Context.set('secondary_user', None)

        for removed_user in removed_collaborators:
            for item in _value[::-1]:
                if item.get('username').lower() != removed_user.lower():
                    continue
                else:
                    _value.pop(_value.index(item))

        Context.set('added_collaborators', _value)

    def runTest(self):
        self.test_deleting_collaborators()

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

    def __delete_collaborator(self, username):
        _formatter = 'Deleting collaborator: "{user}" - FAILED'.format

        self.__toggle_edit_mode(on=True)

        _btnDelete = self.details_page.get_delete_button_by_name(username)
        self.assertIsNotNone(_btnDelete, msg=_formatter(user=username))
        _btnDelete.click()

        self.__toggle_edit_mode(on=False)

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
