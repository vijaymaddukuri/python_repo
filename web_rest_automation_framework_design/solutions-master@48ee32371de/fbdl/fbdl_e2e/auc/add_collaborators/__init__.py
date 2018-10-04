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
from fbdl_e2e.auc.uimap.specific import CollaboratorsPage

from fbdl_e2e.workflow import Context


class AddCollaborators(BaseUseCase):
    """
    Admin / Manager adds collaborators to specific workspace
    """

    def setUp(self):
        """
        Make sure admin / manager is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.btnAddMember.enabled:
            key = 'created_workspace_names'
            Context.validate([key])
            self._ws_name = list(Context.get(key))[-1]

            self.__navigate_to_workspace_details_page(self._ws_name)

        key = 'collaborators_to_be_added'
        Context.validate([key])
        self._lstCollaborators = Context.get(key)
        self._new_collaborators = [item.get('username').strip()
                                   for item in self._lstCollaborators]

        self.collaborators_page = CollaboratorsPage()
        self._ws_name = self.details_page.lblWorkspaceName.value

        _collaborators = self.details_page.get_collaborators()
        _added_collaborators = [
            user for user in self._new_collaborators
            if user in _collaborators]

        [self._new_collaborators.pop(
            self._new_collaborators.index(user))
         for user in _added_collaborators]

        if _added_collaborators:
            _value = Context.get('added_collaborators')

            [_value.append(item)
             for item in self._lstCollaborators
             if item.get('username') in _added_collaborators]

            Context.set('added_collaborators', _value)

    def test_adding_collaborators(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        if not self._new_collaborators:
            return

        self.assertTrue(
            self.details_page.btnAddMember.enabled,
            msg=_formatter(step='Navigate to Collaborators page'))
        self.details_page.btnAddMember.click()

        _added_collaborators = []

        for _new_user in self._new_collaborators:
            self.__add_collaborator(_new_user)
            _added_collaborators.append(_new_user)

        self.__navigate_to_workspace_details_page(self._ws_name)

        [self.assertIn(
            added_user, self.details_page.get_collaborators(),
            msg=_formatter(step='Validate added collaborator')
        ) for added_user in _added_collaborators]

        _role_users_pair = {
            'developer': self.details_page.get_developers,
            'manager': self.details_page.get_managers
        }

        for added_user in _added_collaborators:
            _role = [collaborator.get('role')
                     for collaborator in self._lstCollaborators
                     if collaborator.get('username') == added_user]

            self.assertIn(
                added_user, _role_users_pair[_role[0]](),
                msg=_formatter(step='Validate the role of the added collaborator')
            )

            # Set unique newly added collaborator
            _value = Context.get('added_collaborators')
            for _user in _value[::-1]:
                if added_user.strip().lower() == _user.get('username').strip().lower():
                    break
            else:
                for item in self._lstCollaborators:
                    if item.get('username') == added_user:
                        _value.append(item)
                        Context.set('added_collaborators', _value)

                        break

    def runTest(self):
        self.test_adding_collaborators()

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

    def __add_collaborator(self, username):
        _formatter = 'Adding collaborator: "{user}" - FAILED'.format

        _btnAdd, _added = self.collaborators_page.get_add_button_by_name(username)

        if not _added:
            self.assertIsNotNone(
                _btnAdd, msg=_formatter(user=username))

            _btnAdd.click()
