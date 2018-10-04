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

from uiacore.modeling.webui.controls import WebLabel


class CollaboratorsPage(object):
    def __init__(self):
        super(CollaboratorsPage, self).__init__()

        self.lstCollaborators = WebLabel(xpath='//fbdl-community-list')

    def get_add_button_by_name(self, username):
        self.__scroll_down_page_to_bottom()

        _btnAdd = None
        _added = False

        for user in self.__get_users():
            if user.text.split()[0] == username:
                try:
                    _btnAdd = user.find_element_by_xpath(
                        './/button[@class="add-user-button btn primary ng-scope"]')
                except:
                    # Ignore runtime error
                    pass

                if not _btnAdd:
                    _added = True

                break

        return _btnAdd, _added

    def __scroll_down_page_to_bottom(self):
        _users = self.__get_users()
        if _users:
            _ = _users[-1].location_once_scrolled_into_view

        while self.lstCollaborators.exists() and (
                    len(_users) < len(self.__get_users())):
            _users = self.__get_users()

            _ = _users[-1].location_once_scrolled_into_view

    def __get_users(self):
        _users = []

        container = self.lstCollaborators.current
        if container:
            _users = container.find_elements_by_xpath('.//tbody/tr') or []

        return _users
