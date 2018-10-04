
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
from fbdl_e2e.auc.search_data_sets.search_data_sets_context import SearchDataSetsContext
from fbdl_e2e.auc.uimap.shared import DatasetsPage
from fbdl_e2e.auc.uimap.shared import MainPage
from fbdl_e2e.auc.uimap.shared import WSDetailsPage
from fbdl_e2e.workflow.context import Context


class SearchDataSets(BaseUseCase):
    """
    Data scientist search data sets in the workspace
    """
    def setUp(self):
        SearchDataSetsContext.validate()
        self.detail_page = WSDetailsPage()
        self.datasets_page = DatasetsPage()
        key = 'created_workspace_names'
        _ws_name = list(SearchDataSetsContext.get(key))[-1]
        # self.__get_search_data()

        attempts = 2
        while (attempts > 0) and (not self.datasets_page.lblTitle.exists()):
            if not self.detail_page.btnAddDataSet.exists():
                self.__navigate_to_workspace_details_page(_ws_name)
            self.detail_page.btnAddDataSet.click()
            attempts -= 1

        self.assertTrue(self.datasets_page.lblTitle.exists(),
                        msg='Failed to navigate to data sets page!')

    def test_search_data_sets(self):
        self._search_ds = SearchDataSetsContext.get('search_data_sets')
        if isinstance(self._search_ds, dict):
            for key, value in self._search_ds.iteritems():
                _search_strategy = key
                for item in value:
                    _search_value = item
                    _search_content = '{}:{}'.format(_search_strategy, _search_value)
                    self.__search_data_sets_action(_search_content)
                    self.__validate_search_result(_search_strategy, _search_value)
        elif isinstance(self._search_ds, list):
            for ds in self._search_ds:
                self.__search_data_sets_action(ds) #use tag to search
                self.__validate_search_result('Tag', ds)

        self.datasets_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_search_data_sets()

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

    def __search_data_sets_action(self, search_content):
        self.datasets_page.txtSearch.set('"{}"'.format(search_content))
        self.datasets_page.btnSearch.click()
        self.assertFalse(self.datasets_page.lblLoading.exists(),
                         msg='Failed to load data sets!')
        self.datasets_page.page_down_to_the_bottom()

    def __validate_search_result(self, search_strategy, search_value):
        data_sets_list = self.datasets_page.data_sets
        ds_result_list = []
        self.assertGreater(len(data_sets_list), 0,
                           msg="Got empty result!")
        if search_strategy == 'AssetVisibleName':
            ds_result_list = self.__get_data_sets_name_list(data_sets_list)

        if search_strategy == 'AssetPublishedDate':
            ds_result_list = self.__get_data_sets_published_date_list(data_sets_list)

        if search_strategy == 'AssetRegisteredDate':
            ds_result_list = self.__get_data_sets_registered_date_list(data_sets_list)

        if search_strategy == 'OriginatorsName':
            ds_result_list = self.__get_data_sets_author_list(data_sets_list)

        if search_strategy == 'TemplateType':
            ds_result_list = self.__get_data_sets_data_type_list(data_sets_list)

        if search_strategy == 'Tag':
            ds_result_list = self.__get_data_sets_tag_list(data_sets_list)

        self.assertTrue(all(item == search_value for item in ds_result_list),
                        msg='Got wrong search result!\nSearch result: {}'.format(ds_result_list))

        # key = 'datasets_to_be_deployed'
        # dataset_deploy = Context.get(key)[-1]
        # dataset_deploy['AssetVisibleName'] = self.__get_data_sets_name_list(data_sets_list)[-1]
        # Context.set(key,dataset_deploy)


    def __get_data_sets_name_list(self, ds_list):
        return [str(item.text.split('\n')[0])
                for item in ds_list] or []

    def __get_data_sets_published_date_list(self, ds_list):
        return [str(item.text.split('\n')[1].lstrip('Asset Published Date:').strip())
                for item in ds_list] or []

    def __get_data_sets_registered_date_list(self, ds_list):
        return [str(item.text.split('\n')[2].lstrip('Asset Registered Date:').strip())
                for item in ds_list] or []

    def __get_data_sets_author_list(self, ds_list):
        return [str(item.text.split('\n')[3].lstrip('Author:').strip())
                for item in ds_list] or []

    def __get_data_sets_data_type_list(self, ds_list):
        return [str(item.text.split('\n')[4].lstrip('Data Type:').strip())
                for item in ds_list] or []

    def __get_data_sets_tag_list(self, ds_list):
        return [str(tag[:-2])for tag in ds_list[0].text.split('\n')[5:-1] if 'TAG' in tag][-1:] or []
                    # [:-1] remove 'x'   [5:-1]   tags and description         [-1:] latest tags
