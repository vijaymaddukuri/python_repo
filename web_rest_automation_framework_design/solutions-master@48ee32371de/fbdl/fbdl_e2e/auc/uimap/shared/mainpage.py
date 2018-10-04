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

from uiacore.modeling.webui.controls import WebLink, WebLabel


class MainPage(object):
    def __init__(self, account=None, workspace_name=None):
        self._account = account or ''
        self._workspace_name = workspace_name or ''

        self.lnkAccount = WebLink(
            xpath='//a[contains(text(), "{}")]'.format(self._account))
        self.lnkBrand = WebLink(xpath='//a[@class="brand-logo"]')
        self.lnkLogout = WebLink(xpath='//a[@class="logout"]')
        self.lnkWorkspace = WebLink(xpath='//a[@href="/#/workspaces"]')

        self.lnkTargetWorkspace = WebLink(
            xpath='//div[contains(text(), "{}")]'.format(
                self._workspace_name))
        self.lblWorkspace = WebLabel(
            xpath='//h1[contains(text(), "{}")]'.format(
                self._workspace_name))

        self.ws_container = WebLabel(xpath="//div[@class='row workspaceList']")

        self.lblWorkspaceTitle = WebLabel(css='.workspaces-title')

        self.default_datasets = None
        self.default_tools = None
        self.default_memebers = None

    def get_target_workspace(self, ws_name):
        target_ws = None
        workspaces = self.__get_workspaces_collection()
        if workspaces:
            for workspace in workspaces:
                workspace_content = workspace.text
                workspace_content_list = str(workspace_content).strip().split('\n')
                if workspace_content_list[0] == ws_name:
                    target_ws = workspace
                    break
        return target_ws

    def page_down_to_the_bottom(self):
        _index = 0

        while self.ws_container.exists() and \
                (_index < len(self.__get_workspaces_collection())):
            _index = len(self.__get_workspaces_collection())
            _ = self.__get_workspaces_collection()[-1].location_once_scrolled_into_view

    def __get_workspaces_collection(self):
        workspaces = []
        container = self.ws_container.current

        if container:
            workspaces = container.find_elements_by_tag_name(
                'fbdl-workspace-tile'
            ) or []

        return workspaces
