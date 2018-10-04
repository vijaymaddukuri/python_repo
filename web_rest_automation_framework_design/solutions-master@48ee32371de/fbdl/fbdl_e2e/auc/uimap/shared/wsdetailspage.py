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

from uiacore.modeling.webui.controls import WebButton, WebLabel, WebTextBox


class WSDetailsPage(object):
    def __init__(self):
        self.lblCurrentUserAccount = WebLabel(
            css='fbdl-account-panel a.account-panel.dropdown-button.ng-binding')
        self.lblWorkspaceName = WebLabel(
            css='h1.left.mtn.workspace-name.ng-binding')
        self.btnAddServices = WebButton(id='add-service')
        self.btnAddDataSet = WebButton(css='a.action.deployments')
        self.btnAddMember = WebButton(id='add-user')

        self.btnShowSVCDetails = WebButton(
            xpath='//fbdl-services-list/div/*/a[contains(text(), "Show More")]')
        self.btnShowDSDetails = WebButton(
            xpath='//fbdl-deployments-list/div/*/a[contains(text(), "Show More")]')

        self.lstDatasets = WebLabel(xpath='//fbdl-deployments-list')
        self.lstServices = WebLabel(xpath='//fbdl-services-list')
        self.lstWorkbenches = WebLabel(xpath='//fbdl-vm-list')
        self.lstCollaborators = WebLabel(xpath='//fbdl-users-list')

        self.btnDeleteWS = WebButton(
            xpath='//button[contains(text(), "Delete Workspace")]')
        self.fmDeleteWS = WebLabel(id='delete-workspace-form')
        self.txtDeleteWSName = WebTextBox(
            xpath='//div[@id="delete-workspace-form"]//input[@name="name"]')
        self.btnConfirm = WebButton(
            xpath='//div[@id="delete-workspace-form"]//button[contains(text(), "Confirm")]')
        # self.lblSuccess = WebLabel(xpath='//ul[@class="notification-messages"]/li[contains(text(), '
        #                                  '"Workspace successfully deleted!")')
        # self.lblNotification = WebLabel(css='.notification-bar')
        self.lblSSH = WebLabel(xpath='//p[@class="codeblock ng-binding"]')
        self.lstQuota = WebLabel(xpath='//fbdl-space-quota')

    def get_deployed_workbenches_elements(self):
        workbenches = []

        if self.lstWorkbenches.exists():
            workbenches = self.lstWorkbenches.current\
                .find_elements_by_xpath('.//tbody/tr[@class="ng-scope"]')

        workbenches = [workbench.find_elements_by_tag_name('td')[0]
                       for workbench in workbenches
                       if workbench.text.split('\n')[-1].lower() == 'deployed']

        return workbenches

    def get_deployed_workbenches(self):
        workbenches = []
        elements = self.get_deployed_workbenches_elements()
        if elements:
            workbenches = [ele.text for ele in elements]

        return workbenches

    def get_datasets(self):
        datasets = []

        if self.lstDatasets.exists():
            try:
                datasets = self.lstDatasets.current.find_elements_by_xpath(
                    './/tbody/tr/td[@class="dataset-name pll"]')
            except:
                pass
            finally:
                datasets = [ds.text for ds in datasets]

        return datasets

    def get_deployed_services(self):
        return self.__get_services_by_status('deployed')

    def get_registered_services(self):
        return self.__get_services_by_status('registered')

    def get_collaborators(self):
        return self.__get_users_by_role('email')

    def get_developers(self):
        return self.__get_users_by_role('developer')

    def get_managers(self):
        return self.__get_users_by_role('manager')

    def get_delete_button_by_name(self, username):
        _btnDelete = None

        try:
            if self.lstCollaborators.exists():
                _collaborators = self.lstCollaborators\
                    .current.find_elements_by_xpath('.//tbody/tr')

                for user in _collaborators:
                    if user.text.split()[0].strip() == username:
                        # _user_row = user.find_elements_by_tag_name('td')[-1]
                        # _btnDelete = _user_row.find_element_by_tag_name('a')
                        _btnDelete = user.find_element_by_xpath('.//td/a')

                        break
        except:
            pass

        return _btnDelete

    def get_quota_info(self):
        quota = []
        if self.lstQuota.exists():
            quota = self.lstQuota.current.find_elements_by_xpath(
                '//div[@class="col m2 space-quota-usage-content ng-binding"]')

            quota = [str(q.text) for q in quota]

        return quota

    @property
    def edit_toggle_button(self):
        _btnEdit = None

        try:
            if self.lstCollaborators.exists():
                _col = self.__get_headers(self.lstCollaborators.current)[-1]
                _btnEdit = _col.find_element_by_tag_name('button')
        except:
            pass

        return _btnEdit

    @property
    def workspace_id(self):
        current = self.btnAddServices.current
        if current:
            return str(current.parent.current_url).split('/')[-1]
        else:
            return None

    def __get_services_by_status(self, svc_status):
        services = []

        if self.lstServices.exists():
            services = self.lstServices\
                .current.find_elements_by_xpath('.//tbody/tr')

        services = [svc.find_elements_by_tag_name('td')[0].text
                    for svc in services
                    if svc.text.split()[-1].lower() == svc_status]

        return services

    def __get_users_by_role(self, role=''):
        _users = []

        if role.strip() and self.lstCollaborators.exists():
            _index = -1
            for col in self.__get_headers(self.lstCollaborators.current):
                _index += 1

                if str(col.text).strip().lower() == role.strip().lower():
                    break
            else:
                _index = -1

            if _index != -1:
                _collaborators = self.lstCollaborators\
                    .current.find_elements_by_xpath('.//tbody/tr')

                if _index == 0:
                    _users = [user.text.split()[0]
                              for user in _collaborators]
                else:
                    _users = [user.find_elements_by_tag_name('td')[0].text
                              for user in _collaborators
                              if user.find_elements_by_tag_name('td')[_index]
                                  .find_elements_by_xpath('.//input[@checked="checked"]')]

        return _users

    def __get_headers(self, container):
        _headers = []

        if container:
            _header_row = container.find_element_by_xpath('.//thead/tr')
            _headers = _header_row.find_elements_by_tag_name('th') or []

        return _headers
