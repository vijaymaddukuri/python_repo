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
from fbdl_e2e.auc.logout.logout_context import LogoutContext
from fbdl_e2e.auc.uimap.specific import LoginPage
from fbdl_e2e.auc.uimap.shared import MainPage


class LogoutGlobalUI(BaseUseCase):

    def setUp(self):
        LogoutContext.validate()

        self._logout_context = LogoutContext.get('last_login_user')

        self.login_page = LoginPage()
        self.main_page = MainPage(
            account=self._logout_context['username'])

    def test_logout_global_UI(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.main_page.lnkAccount.click()
        self.main_page.lnkLogout.click()

        self.assertTrue(
            self.login_page.lblWelcome.exists(),
            msg=_formatter(step='Logout from global UI'))

        LogoutContext.set('is_login', False)

        self._name = 'data_scientist({})_logs_out_from_global_ui'.format(
            self._logout_context['username'])

        # workaround for using existing workspace
        LogoutContext.get('created_workspace_names').pop(-1)

    def runTest(self):
        self.test_logout_global_UI()
