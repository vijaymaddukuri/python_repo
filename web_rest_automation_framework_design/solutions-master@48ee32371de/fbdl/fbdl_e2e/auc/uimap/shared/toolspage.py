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


class ToolsPage(object):
    def __init__(self):
        self.tools_container = WebLabel(xpath='//fbdl-application-sets-list')

        self.lblConfirmDeletion = WebLabel(xpath='//div[@class="modal open"]')
        self.lblToolPanel = WebLabel(xpath='//fbdl-application-sets-sidebar')

        self.btnBackToWorkspaceDetails = WebButton(
            xpath='//a[@class="back-to-workspace-details"]')

    def get_service_instances(self):
        _services = []

        container = self.tools_container.current
        if container:
            _services = [svc.text.split('\n')[0]
                         for svc in container.find_elements_by_tag_name(
                    'fbdl-application-set')] or []

        return _services

    @property
    def tools_list(self):
        return self.__get_tools()

    def page_down_to_the_bottom(self):
        self.__scroll_tools()

    def get_tool_publish_button(self, tl_name):
        return self.__get_publish_button_from_list(self.tools_list, tl_name)

    def get_tool_delete_button(self, tl_name):
        return self.__get_delete_button_from_list(self.tools_list, tl_name)

    def get_tool_expand_button(self, tool_name):
        _btnExpand = None

        for tool in self.__get_tools():
            try:
                if tool.text.split('\n')[0] == tool_name:
                    _btnExpand = tool.find_element_by_xpath(
                        './/div/*/span/a/span')
                    break
            except:
                pass

        return _btnExpand

    def get_confirmation_button(self):
        _btn_OK = None

        try:
            _btn_OK = self.lblConfirmDeletion.current.find_element_by_xpath(
                './/div/button[@class="block btn primary"]')
        except:
            pass

        return _btn_OK

    def get_tool_info_by_key(self, key):
        _retValue = None

        if self.lblToolPanel.exists():
            try:
                for _section in self.lblToolPanel.current.find_elements_by_xpath(
                  './/section/ul[@class="detailed-datasets"]'):
                    for _key, _value in self.__iter_tool_fields(_section):
                        if str(key).lower() == _key:
                            _retValue = _value
                            break
                    else:
                        continue

                    if _retValue:
                        break
            except:
                pass

        return _retValue

    def __iter_tool_fields(self, ds_container):
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

    def __get_tools(self):
        tools = []
        container = self.tools_container.current

        try:
            if container:
                tools = container.find_elements_by_xpath(
                    './/div[@class="col l6 service-item ng-scope"]'
                ) or []
        except:
            pass

        return tools

    def __scroll_tools(self):
        _length = 0

        while self.tools_container.exists() and \
                (_length < len(self.__get_tools())):
            _length = len(self.__get_tools())

            _ = self.__get_tools()[-1].\
                location_once_scrolled_into_view

    def __get_publish_button_from_list(self, svc_list, service):
        self._btnPublish = None
        for svc in svc_list:
            if svc.text.split('\n')[0] == service:
                self._btnPublish = svc.find_element_by_xpath(
                    './/button')
                break

        return self._btnPublish

    def __get_delete_button_from_list(self, tools, tool_name):
        _btnDelete = None

        for tool in tools:
            try:
                if tool.text.split('\n')[0] == tool_name:
                    _btnDelete = tool.find_element_by_xpath(
                        './/button[2]')
                    break
            except:
                # StaleElementReferenceException issues
                # if the page has been refreshed or element has been deleted
                pass

        return _btnDelete
