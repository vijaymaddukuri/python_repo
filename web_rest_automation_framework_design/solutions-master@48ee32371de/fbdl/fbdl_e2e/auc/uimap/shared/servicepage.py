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

from uiacore.modeling.webui.controls import WebLabel, WebTextBox, WebButton


class ServicePage(object):

    def __init__(self):
        self.lblTitle = WebLabel(css='h4.truncate.workspace-name.ng-binding')
        self.txtSearch = WebTextBox(xpath="//input[@name='search']")
        self.btnSearch = WebButton(xpath="//button[@class='btn primary search-icon-button small']")
        self.lblLoading = WebLabel(xpath="//div[contains(text(), 'Loading']")

        self.services_container = WebLabel(
                xpath='//div/fbdl-marketplace-services-list')
        self._btnDeploy = None
        self._btnDelete = None

        self.lblAlertNotificationMsg = WebLabel(
            css='div.alert.alert-dismissible.notification-bar.row.alert-danger ul.notification-messages')
        self.lblConfirmDeletion = WebLabel(xpath='//div[@class="modal open"]')

        self.txtPcfInstance = WebTextBox(
            css='#create-service-instance-form.modal input.service-instance-name')
        self.btnPcfDeploy = WebButton(
            css='#create-service-instance-form.modal button.block.btn.create-service-button.primary')

        self.txtTargetVM = WebTextBox(xpath='//div/input[@name="targetIP"]')

        self.frmDeployDacApp = WebLabel(id='create-dacapp-instance-form')
        self.txtAssetVisibleName = WebTextBox(xpath='//div/input[@name="assetVisibleName"]')
        self.txtClusterName = WebTextBox(xpath='//div/input[@name="clusterName"]')

        self.btnDacDeploy = WebButton(
            css='#create-dacapp-instance-form.modal button.block.btn.create-vm-button.primary')

        self.lblDeployedServices = WebLabel(css='ul.deployed-services')
        self.lblDeployingServices = WebLabel(css='ul.deploying-services')

        self.btnBackToWorkspaceDetails = WebButton(
            xpath='//a[@class="back-to-workspace-details"]')

    def get_pcf_deploy_button(self, service):
        return self.__get_deploy_button_from_list(self.pcf_svc_list, service)

    def get_dac_deploy_button(self, service):
        return self.__get_deploy_button_from_list(self.dac_svc_list, service)

    def get_dac_delete_button(self, service):
        self.page_down_to_the_bottom()

        for svc_item in self.__get_dac_services():
            if svc_item.text.split('\n')[0] == service:
                self._btnDelete = svc_item.find_element_by_xpath(
                    './/*[@class="btn primary small ng-binding"]')
                break

        return self._btnDelete

    def get_confirmation_button(self):
        _btn_OK = None

        try:
            _btn_OK = self.lblConfirmDeletion.current.find_element_by_xpath(
                './/div/button[@class="block btn primary"]')
        except:
            pass

        return _btn_OK

    def get_deployed_services(self):
        return self.__get_svc_instances_from_panel(
            self.lblDeployedServices.current)

    def get_deploying_services(self):
        return self.__get_svc_instances_from_panel(
            self.lblDeployingServices.current)

    def page_down_to_the_bottom(self):
        self.__scroll_services_by_type('pcf')
        self.__scroll_services_by_type('dac')

    @property
    def pcf_svc_list(self):
        return self.__get_services_by_type('pcf')

    @property
    def dac_svc_list(self):
        return self.__get_services_by_type('dac')

    def __get_services_by_type(self, svc_type):
        svc_dict = {
            "pcf": self.__get_pcf_services,
            "dac": self.__get_dac_services,
        }

        return svc_dict[svc_type]()

    def __get_pcf_services(self):
        return self.__get_services_by_tag(
            'fbdl-marketplace-service')

    def __get_dac_services(self):
        return self.__get_services_by_tag(
            'fbdl-marketplace-dac')

    def __get_services_by_tag(self, tag_name):
        services = []

        if tag_name:
            container = self.services_container.current

            if container:
                services = container.find_elements_by_tag_name(tag_name) or []

        return services

    def __get_deploy_button_from_list(self, svc_list, service):
        for svc in svc_list:
            if svc.text.split('\n')[0] == service:
                self._btnDeploy = svc.find_element_by_xpath(
                    './/*[@class="btn deploy-button primary small"]')
                break

        return self._btnDeploy

    def __get_svc_instances_from_panel(self, panel=None):
        _services = []

        try:
            if panel:
                _services = [svc.text for svc in
                             panel.find_elements_by_tag_name('li')]
        except:
            # StaleElementReferenceException issues
            # if the page has been refreshed or element has been deleted
            pass

        return _services

    def __scroll_services_by_type(self, svc_type):
        _length = 0

        while self.services_container.exists() and \
                (_length < len(self.__get_services_by_type(svc_type))):
            _length = len(self.__get_services_by_type(svc_type))

            _ = self.__get_services_by_type(
                svc_type)[-1].location_once_scrolled_into_view
