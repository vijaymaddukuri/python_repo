
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
from fbdl_e2e.auc.search_tools.search_tools_context import SearchToolsContext
from fbdl_e2e.auc.uimap.shared import WSDetailsPage
from fbdl_e2e.auc.uimap.shared import ServicePage
from fbdl_e2e.auc.uimap.shared import MainPage


class SearchTools(BaseUseCase):
    """
    Data scientist searches tools (DAC services)
    """

    def setUp(self):
        SearchToolsContext.validate()
        self.detail_page = WSDetailsPage()
        self.service_page = ServicePage()
        key = 'created_workspace_names'
        _ws_name = list(SearchToolsContext.get(key))[-1]

        self.__get_search_date()
        attempts = 2
        while (attempts > 0) and (not self.service_page.lblTitle.exists()):
            if not self.detail_page.btnAddServices.exists():
                self.__navigate_to_workspace_details_page(_ws_name)
            self.detail_page.btnAddServices.click()
            attempts -= 1

        self.assertTrue(self.service_page.lblTitle.exists(),
                        msg='Failed to navigate to service page!')

    def test_search_tools(self):
        for key, value in self._search_dict.iteritems():
            _search_strategy = key
            for item in value:
                _search_value = item
                _search_content = '{}:{}'.format(_search_strategy, _search_value)
                self.__search_tools_action(_search_content)
                self.__validate_search_result(_search_strategy, _search_value)

        self.service_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_search_tools()

    def __navigate_to_workspace_details_page(self, ws_name):
        self.main_page = MainPage(workspace_name=ws_name)
        self.main_page.lnkWorkspace.click()
        self.main_page.lnkTargetWorkspace.click()

    def __search_tools_action(self, search_content):
        self.service_page.txtSearch.set('"{}"'.format(search_content))
        self.service_page.btnSearch.click()
        self.assertFalse(self.service_page.lblLoading.exists(),
                         msg='Failed to load services!')
        self.service_page.page_down_to_the_bottom()

    def __validate_search_result(self, search_strategy, search_value):
        svc_list = self.service_page.dac_svc_list

        self.assertGreater(len(svc_list), 0, msg="Got empty result!")
        if search_strategy == 'AssetVisibleName':
            svc_name_list = self.__get_svc_name_list(svc_list)
            self.assertTrue(all(item == search_value for item in svc_name_list),
                            msg='Got wrong search result!\nSearch result: {}'.format(svc_name_list))

    def __get_svc_name_list(self, svc_list):
            return (str(item.text).strip().split('\n')[0]
                    for item in svc_list) or []

    def __get_search_date(self):
        _accepted_tools = SearchToolsContext.get('accepted_tools')
        if _accepted_tools:
            self._search_dict = {
                'AssetVisibleName': [tool['name'] for tool in _accepted_tools]
            }
        else:
            self._search_dict = SearchToolsContext.get('search_tools_name')
        self.assertTrue(bool(self._search_dict),
                        msg='No asset info provided.')
