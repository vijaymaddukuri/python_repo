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

from uiacore.modeling.webui.controls import WebLabel, WebButton


class WorkingSetsPage(object):
    def __init__(self, workingset_name=''):
        self.workingset_name = workingset_name
        self.datasets_container = WebLabel(xpath='//fbdl-working-set-list')

        self.lblDatasetPanel = WebLabel(xpath='//fbdl-working-set-sidebar/div/section')

        self.btnBackToWorkspaceDetails = WebButton(
            xpath='//a[@class="back-to-workspace-details"]')

    @property
    def deployed_datasets(self):
        return self.__get_datasets()

    def page_down_to_the_bottom(self):
        self.__scroll_data_sets()

    @property
    def target_working_set(self):
        return self.__get_workingset_by_name(self.workingset_name)

    @property
    def btnPublish(self):
        return self.__get_element_by_xpath(
            './/button[starts-with(@ng-click, "cancelable")]')

    @property
    def btnDelete(self):
        return self.__get_element_by_xpath(
            './/button[starts-with(@ng-click, "deleteWorkingSet")]')

    @property
    def fmDeleteConfirm(self):
        _confirm = None
        try:
            _confirm = self.datasets_container.current.find_element_by_css_selector('div[class="modal open"]')
        except:
            pass
        return _confirm


    @property
    def btnDeleteConfirm(self):
        _ok = None
        try:
            _ok = self.fmDeleteConfirm.find_element_by_xpath('.//button[contains(text(), "Ok")]')
        except:
            pass
        return _ok

    @property
    def btnExpand(self):
        return self.__get_element_by_xpath('.//div/*/span/a/span')

    def get_dataset_info_by_key(self, key):
        _retValue = None

        if self.lblDatasetPanel.exists():
            try:
                for _key, _value in self.__iter_dataset_items(
                    self.lblDatasetPanel.current.find_element_by_xpath(
                        './/ul[@class="detailed-datasets"]')):
                    if str(key).lower() == _key:
                        _retValue = _value
                        break
            except:
                pass

        return _retValue

    def __get_datasets(self):
        _workingsets = []

        container = self.datasets_container.current

        if container:
            try:
                _workingsets = container.find_elements_by_tag_name(
                    'fbdl-working-set') or []
            except:
                pass

        return _workingsets

    def __scroll_data_sets(self):
        _length = 0

        while self.datasets_container.exists() and \
                (_length < len(self.__get_datasets())):
            _length = len(self.__get_datasets())

            _ = self.__get_datasets()[-1].location_once_scrolled_into_view

    def __get_workingset_by_name(self, name):
        _workingset = None

        for ds in self.__get_datasets():
            # if ds.text.split('\n')[0] == name:
            title = ds.find_element_by_xpath('.//div[@class="card-title ng-binding"]')
            if title and str(title.text).strip() == name:
                _workingset = ds
                break

        return _workingset

    def __get_element_by_xpath(self, xpath):
        _element = None

        _ws = self.__get_workingset_by_name(self.workingset_name)
        if _ws:
            try:
                _element = _ws.find_element_by_xpath(xpath)
            except:
                pass

        return _element

    def __iter_dataset_items(self, ds_container):
        if ds_container:
            try:
                for item in ds_container.find_elements_by_tag_name('li'):
                    _kvp = item.find_elements_by_tag_name('span')
                    _key = _kvp[0].text.split('\n')[0].lower()
                    _value = _kvp[1].text.split('\n')[0]

                    yield _key, _value
            except:
                pass

        raise StopIteration()
