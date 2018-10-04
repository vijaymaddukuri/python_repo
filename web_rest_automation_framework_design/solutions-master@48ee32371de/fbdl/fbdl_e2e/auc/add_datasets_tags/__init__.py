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

from robot.api import logger

from fbdl_e2e.auc.add_datasets_tags.add_datasets_tag_context import AddDataSetsTagsContext
from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, DatasetsPage


class AddDataSetsTags(BaseUseCase):
    """
    add a tag on dataset (default is "TAG160415XXXX"
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        AddDataSetsTagsContext.validate()
        self.details_page = WSDetailsPage()

        if not self.details_page.btnAddDataSet.enabled:
            key = 'created_workspace_names'
            _ws_name = list(AddDataSetsTagsContext.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        _ds_list = AddDataSetsTagsContext.get('accepted_datasets')
        self._ds = [ds['name'] for ds in _ds_list]
        self.assertTrue(bool(self._ds),
                        msg='No asset info provided.')
        self.ds_page = DatasetsPage()

    def test_add_dataset_tag_from_dac(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertTrue(
            self.details_page.btnAddDataSet.enabled,
            msg=_formatter(step='Navigate to DataSets page'))
        self.details_page.btnAddDataSet.click()

        self.ds_page.page_down_to_the_bottom()

        self._tag_list = []
        for dataset in self._ds:
            self.__add_dataset_tag(dataset)

        AddDataSetsTagsContext.set('search_data_sets', self._tag_list)

        self.ds_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_add_dataset_tag_from_dac()

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

    def __add_dataset_tag(self, ds_name):
        _formatter = 'Adding dataset tags: "{ds}" - FAILED'.format

        tag_input = self.ds_page.get_tag_input_by_ds_name(ds_name)

        # self.assertIsNotNone(
        #     tag_input, msg=_formatter(ds=ds_name))
        # tag_input.click()
        from datetime import datetime
        tag = "TAG%s" % datetime.now().strftime('%y%m%d%H%M')
        tag_input.send_keys(tag)

        dataset_div = self.ds_page.get_dataset_by_ds_name(ds_name)

        self.assertTrue(
            dataset_div, msg=_formatter(ds=ds_name))
        dataset_div.click()

        logger.info('Add a Tag: {0} for Workspace: {1}'.format(tag, ds_name), also_console=True)
        self._tag_list.append(tag)
