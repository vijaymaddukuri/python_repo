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
from fbdl_e2e.auc.publish_data_sets.publish_data_sets_context import PublishDataSetsContext
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, WorkingSetsPage


class PublishDataSets(BaseUseCase):
    """
    Data scientist submit a publish request for a data set in working set page
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        PublishDataSetsContext.validate()
        self.details_page = WSDetailsPage()
        if not self.details_page.btnShowDSDetails.enabled:
            key = 'created_workspace_names'
            _ws_name = list(PublishDataSetsContext.get(key))[-1]
            self.__navigate_to_workspace_details_page(_ws_name)

        self._ws_id = self.details_page.workspace_id
        self._pub_ds = PublishDataSetsContext.get('registered_datasets')[-1]
        self.assertTrue(bool(self._pub_ds), msg='No asset info provided')

    def test_publish_data_set_into_dac(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertTrue(self.details_page.btnShowDSDetails.exists(),
                        msg=_formatter(step='Button show detailed list does not exists!'))
        self.details_page.btnShowDSDetails.click()

        self.working_sets_page = WorkingSetsPage(self._pub_ds)
        self.working_sets_page.page_down_to_the_bottom()
        self.__publish_data_set(self._pub_ds)

        class Object(object):
            pass
        response = Object()
        response.code = '0'
        response.category='data'
        response.guid = ''
        response.name = self._pub_ds
        response.workspace = self._ws_id

        PublishDataSetsContext.set('submitted_assets', [response])
        _registered_datasets = PublishDataSetsContext.get('registered_datasets')
        _registered_datasets = _registered_datasets.pop(-1)
        PublishDataSetsContext.set('registered_assets', _registered_datasets)

        self.working_sets_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_publish_data_set_into_dac()

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

    def __publish_data_set(self, ds_name):
        _formatter = 'Runing on step: "{step}" - FAILED'.format

        btn_publish = self.working_sets_page.btnPublish

        self.assertIsNotNone(
            btn_publish, msg=_formatter(step='Get corresponding publish button of data set ' + ds_name))
        btn_publish.click()
        import time
        timeout = 30
        while str(btn_publish.text).strip() == 'Publishing' and (timeout >= 0):
            time.sleep(1)
            timeout -= 1
        self.assertEqual(str(btn_publish.text).strip(), 'Cancel Publication',
                         msg=_formatter(step='Publish data set to DAC'))
