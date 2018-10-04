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

from uiacore.modeling.webui.controls import \
    WebLabel, WebTextBox, \
    WebButton, WebCombo


class DatasetsPage(object):
    def __init__(self):
        self.lblTitle = WebLabel(css='h4.truncate.ng-binding')
        self.txtSearch = WebTextBox(xpath="//input[@name='search']")
        self.btnSearch = WebButton(xpath="//button[@class='btn primary search-icon-button small']")
        self.lblLoading = WebLabel(xpath="//div[contains(text(), 'Loading']")
        self.lst_data_sets = WebLabel(
                xpath='//div[@class="data-catalog-list dataSourceList maxl row ng-isolate-scope"]')
        self.frmDeployDataset = WebLabel(id='deploy-dataset-form')
        self.cboDataContainer = WebCombo(id='mySelect')
        self.txtWorkingSetName = WebTextBox(xpath='//input[@name="assetVisibleName"]')

        self.lblMsgNotification = WebLabel(
            css='div.alert.alert-dismissible.notification-bar.row.alert-success')

        self.btnConfirm = WebButton(xpath='//button[@class="block btn create-vm-button primary"]')
        self.btnBackToWorkspaceDetails = WebButton(
            xpath='//a[@class="back-to-workspace-details"]')

    def page_down_to_the_bottom(self):
        _length = 0

        while self.lst_data_sets.exists() and \
                (_length < len(self.data_sets)):
            _length = len(self.data_sets)

            _ = self.data_sets[-1].location_once_scrolled_into_view

    def __get_element_using_xpath_by_ds_name(self, ds_name, xpath=''):
        element = None
        for ds in self.__get_data_sets():
            if ds.text.split('\n')[0] == ds_name:
                if xpath:
                    element = ds.find_element_by_xpath(xpath)
                else:
                    element = ds
                break

        return element

    def get_deploy_button_by_ds_name(self, ds_name):
        return self.__get_element_using_xpath_by_ds_name(
            ds_name, './/button[@class="btn deploy-button primary small"]')

    def get_delete_button_by_ds_name(self, ds_name):
        return self.__get_element_using_xpath_by_ds_name(
            ds_name, './/button[@class="btn deploy-button primary small ng-binding"]')

    def get_delete_ok_by_ds_name(self, ds_name):
        return self.__get_element_using_xpath_by_ds_name(
            ds_name, './/button[@class="block btn primary"]')

    def get_dataset_by_ds_name(self, ds_name):
        return self.__get_element_using_xpath_by_ds_name(
            ds_name, './/a/span')

    def get_tag_input_by_ds_name(self,ds_name):
        return self.__get_element_using_xpath_by_ds_name(
            ds_name, './/input[@type="text"]')
        #.//input[@class="input ng-pristine ng-untouched ng-valid"]

    @property
    def data_sets(self):
        return self.__get_data_sets()

    @property
    def deploy_dataset_fields(self):
        _text_boxes = []
        _xpath = '//div[@id="modal-missingVariables-div"]/input[@{attr}]'

        try:
            _text_boxes = self.frmDeployDataset.current.find_elements_by_xpath(
                '.' + _xpath.format(attr='*'))
        except:
            pass
        finally:
            _text_boxes = [_textbox.get_attribute('name') for _textbox in _text_boxes]

            _fields = [{
                'name': _textbox,
                'item': WebTextBox(xpath=_xpath.format(
                    attr='name="{}"'.format(_textbox)))
            } for _textbox in _text_boxes]

        return _fields

    def __get_data_sets(self):
        _data_set_list = []

        container = self.lst_data_sets.current
        if container:
            _data_set_list = container.find_elements_by_tag_name(
                'fbdl-data-set') or []

        return _data_set_list
