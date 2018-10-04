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
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage,DatasetsPage
from fbdl_e2e.auc.delete_datasets.delete_datasets_context import DeleteDataSetsContext
from fbdl_e2e.workflow import Context

class DeleteDataSets(BaseUseCase):
    """
    Data scientist deletes tools into a workbench
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        DeleteDataSetsContext.validate()
        self.details_page = WSDetailsPage()

        if not self.details_page.btnAddDataSet.enabled:
            key = 'created_workspace_names'
            _ws_name = list(DeleteDataSetsContext.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        key = 'data_set_to_be_deleted'
        self._delete_ds = DeleteDataSetsContext.get(key)

        self.ds_page = DatasetsPage()

    def test_delete_data_set_from_dac(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertTrue(
            self.details_page.btnAddDataSet.enabled,
            msg=_formatter(step='Navigate to DataSets page'))
        self.details_page.btnAddDataSet.click()

        self.ds_page.page_down_to_the_bottom()

        self.__delete_data_set(self._delete_ds)


    def runTest(self):
        self.test_delete_data_set_from_dac()

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

    def __delete_data_set(self, ds_name):

        _formatter = 'Deleting dataset: "{ds}" - FAILED'.format
        btn_delete = self.ds_page.get_delete_button_by_ds_name(ds_name)
        btn_ok = self.ds_page.get_delete_ok_by_ds_name(ds_name)


        self.assertIsNotNone(
            btn_delete, msg=_formatter(ds=ds_name))
        btn_delete.click()

        self.assertTrue(
            btn_ok.is_displayed(),msg=_formatter(ds=ds_name))
        btn_ok.click()

        from time import sleep
        sleep(1)
        self.assertEqual(
            btn_delete.text,'Deleting',msg=_formatter(ds=ds_name))

        self.ds_page.btnSearch.click() #workaround
        self.ds_page.page_down_to_the_bottom()

        sleep(5)
        dataset_div = self.ds_page.get_dataset_by_ds_name(ds_name)
        self.assertIsNone(
            dataset_div,msg=_formatter(ds=ds_name))

