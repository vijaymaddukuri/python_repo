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

from robot.api import logger
from cliacore import CLIRunner

class ViewQuota(BaseUseCase):
    """
    View Quota info
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.btnAddServices.enabled:
            key = 'created_workspace_names'
            Context.validate([key])
            _ws_name = list(Context.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

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

    def test_view_quota(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        _quotas = self.details_page.get_quota_info()

        self.assertIsNotNone(_quotas,msg=_formatter(step='Validate quotas information'))

        logger.info('Total {0}: {1}'.format('Services',_quotas[0]),also_console=True)
        logger.info('Total {0}: {1}'.format('CPUs',_quotas[1]),also_console=True)
        logger.info('Total {0}: {1}'.format('Memory',_quotas[2]),also_console=True)
        logger.info('Total {0}: {1}'.format('Storage',_quotas[3]),also_console=True)
        logger.info('Total {0}: {1}'.format('VMs',_quotas[4]),also_console=True)


    def runTest(self):
        self.test_view_quota()


