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
from fbdl_e2e.auc.login.login_context import LoginContext
from fbdl_e2e.auc.uimap.specific import LoginPage
from fbdl_e2e.auc.uimap.shared import MainPage


class LoginGlobalUI(BaseUseCase):
    """
    Data scientist logs in to BDL global UI
    """

    def setUp(self):
        LoginContext.validate()

        _users = ['primary_user', 'secondary_user']
        self._login_context = LoginContext.get(_users[0])
        _last_login = LoginContext.get('last_login_user')

        if _last_login:
            if _last_login['username'] == self._login_context['username']:
                self._login_context = LoginContext.get(_users[-1])
                LoginContext.set(_users[-1], self._login_context)
        else:
            LoginContext.set(_users[0], self._login_context)

        self.login_page = LoginPage()

    def test_login_global_UI(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        _username = self._login_context['username']
        _password = self._login_context['password']

        self.main_page = MainPage(account=_username)

        self.login_page.txtUsername.set(_username)
        self.login_page.txtPassword.set(_password)
        self.login_page.btnSignIn.click()

        self.assertTrue(
            self.main_page.lnkAccount.exists(),
            msg=_formatter(step='Login to BDL global UI'))

        LoginContext.set('is_login', True)
        LoginContext.set('last_login_user', self._login_context)

        self._name = 'data_scientist({})_logs_in_to_global_ui'.format(
            self._login_context['username'])

    def runTest(self):
        self.test_login_global_UI()
