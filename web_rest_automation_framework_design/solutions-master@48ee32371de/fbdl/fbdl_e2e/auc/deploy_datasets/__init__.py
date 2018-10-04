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

import time

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.uimap.shared import (
    MainPage, WSDetailsPage, DatasetsPage, WorkingSetsPage)
from fbdl_e2e.workflow import Context


class DeployDataSets(BaseUseCase):
    """
    Data Scientist deploys data set to existing data container
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.btnAddDataSet.enabled:
            key = 'created_workspace_names'
            Context.validate([key])
            _ws_name = list(Context.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        key = 'datasets_to_be_deployed'
        Context.validate([key])
        self.datasets = Context.get(key)

        self.assertGreaterEqual(
            len(self.datasets), 1,
            msg='No asset info provided.')

        self.ds_page = DatasetsPage()

    def test_deploy_datasets(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertTrue(
            self.details_page.btnAddDataSet.enabled,
            msg=_formatter(step='Navigate to DataSets page'))
        self.details_page.btnAddDataSet.click()

        deployed_datasets = []

        for ds in self.datasets:
            _dsname = ds.get('name')
            _container = ds.get('container')
            _wsname = ds.get('workingset')
            self.__deploy_dataset(_dsname, _container, _wsname)

            deployed_datasets.append(ds)

        self.ds_page.btnBackToWorkspaceDetails.click()

        _now = time.time()
        _timeout_mins = 10 * 60

        while (_timeout_mins > (time.time() - _now)) and (
                    deployed_datasets[-1].get('workingset') not in
                    self.details_page.get_datasets()):
            time.sleep(5)

        self.assertTrue(
            self.details_page.btnShowDSDetails.enabled,
            msg=_formatter(step='Navigate to Dataset Details page'))
        self.details_page.btnShowDSDetails.click()

        self.workingset_page = WorkingSetsPage()
        self.assertTrue(
            self.workingset_page.datasets_container.exists(),
            msg=_formatter(step='Validate deployed datasets on detailed list'))

        _datasets = [ds.text.split('\n')[0]
                     for ds in self.workingset_page.deployed_datasets]
        
        [self.assertIn(
            ds.get('workingset'), _datasets,
            msg=_formatter(step='Validate deployed dataset - %s'
                                % ds.get('workingset')))
         for ds in deployed_datasets]

        Context.set('deployed_datasets', deployed_datasets)

        self.ds_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_deploy_datasets()

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

    def __deploy_dataset(self, ds_name, container_name, ws_name):
        _formatter = 'Deploying dataset: "{ds}" - FAILED'.format

        self.ds_page.page_down_to_the_bottom()

        btn_deploy = self.ds_page.get_deploy_button_by_ds_name(ds_name)

        self.assertIsNotNone(
            btn_deploy, msg=_formatter(ds=ds_name))
        btn_deploy.click()

        self.assertTrue(
            self.ds_page.frmDeployDataset.exists(),
            msg=_formatter(ds=ds_name))

        self.assertGreaterEqual(
            self.ds_page.cboDataContainer.get_items_count, 1,
            msg=_formatter(ds=container_name))

        self.ds_page.cboDataContainer.select(
            by_visible_text=container_name)

        self.ds_page.txtWorkingSetName.set(ws_name)

        from datetime import datetime
        timespan = datetime.now().strftime('%y%m%d%H%M')

        text_boxes = self.ds_page.deploy_dataset_fields

        for textbox in text_boxes:
            name = textbox.get('name')
            item = textbox.get('item')

            if item:
                if ('Path' in name) or (
                            'URL' in name):
                    # Existing bug while deleting working set
                    # So we have to deploy the dataset to a subdirectory under /tmp
                    _value = '/tmp/dir'
                elif 'table' in name:
                    _value = 'table' + timespan
                elif 'database' in name:
                    _value = 'database' + timespan
                elif 'collection' in name:
                    _value = 'collection' + timespan
                else:
                    self.fail(msg='Unexpected field: {}'.format(name))

                item.set(_value)

        self.assertTrue(
            self.ds_page.btnConfirm.enabled,
            msg=_formatter(ds=ds_name))

        self.ds_page.btnConfirm.click()

        _now = time.time()
        _timeout_mins = 1 * 60

        while _timeout_mins > (time.time() - _now):
            if self.ds_page.lblMsgNotification.exists():
                self.ds_page.lblMsgNotification.current\
                    .find_element_by_xpath('.//button/span').click()

                time.sleep(5)
                break
