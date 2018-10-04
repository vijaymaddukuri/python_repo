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
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, WorkingSetsPage
from fbdl_e2e.auc.delete_registered_workingsets.delete_registered_workingsets_context import DeleteRegisteredWorkingSetsContext


class DeleteRegisteredWorkingSets(BaseUseCase):
    """
    Data scientist delete working set from workspace
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        DeleteRegisteredWorkingSetsContext.validate()
        self.details_page = WSDetailsPage()
        if not self.details_page.btnShowDSDetails.enabled:
            key = 'created_workspace_names'
            _ws_name = list(DeleteRegisteredWorkingSetsContext.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        _registered_datasets = DeleteRegisteredWorkingSetsContext.get('accepted_datasets')
        self.assertTrue(bool(_registered_datasets),
                        msg='No registered dataset exists!')
        self.ds_name = _registered_datasets[-1]['name']

    def test_delete_working_set(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertTrue(self.details_page.btnShowDSDetails.exists(),
                        msg=_formatter(step='Button show detailed list does not exists!'))
        self.details_page.btnShowDSDetails.click()

        self.working_sets_page = WorkingSetsPage(self.ds_name)
        self.__delete_working_set(self.ds_name)

        self.assertIsNone(self.working_sets_page.target_working_set,
                          msg=_formatter(step='Delete working set'))

        # _registered_datasets = DeleteRegisteredWorkingSetsContext.get('registered_datasets')
        # _registered_datasets = _registered_datasets.pop(-1)
        # DeleteRegisteredWorkingSetsContext.set('registered_datasets', _registered_datasets)

        self.working_sets_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_delete_working_set()

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

    def __delete_working_set(self, ds_name):
        _formatter = 'Runing on step: "{step}" - FAILED'.format

        self.working_sets_page.page_down_to_the_bottom()
        btn_delete = self.working_sets_page.btnDelete

        self.assertIsNotNone(
            btn_delete, msg=_formatter(
                step='Get corresponding delete button of working set ' + ds_name))
        btn_delete.click()

        import time
        timeout = 10

        while timeout > 0 and (
                not self.working_sets_page.fmDeleteConfirm):
            time.sleep(1)
            timeout -= 1

        self.assertTrue(
            self.working_sets_page.fmDeleteConfirm.is_displayed(),
            msg=_formatter(step='Alert delete confirm dialog'))
        btn_OK = self.working_sets_page.btnDeleteConfirm
        self.assertTrue(btn_OK.is_enabled(),
                        msg='Click OK button')
        btn_OK.click()

        import time
        timeout = 30
        while self.working_sets_page.btnDelete and (timeout >= 0):
            time.sleep(1)
            timeout -= 1


