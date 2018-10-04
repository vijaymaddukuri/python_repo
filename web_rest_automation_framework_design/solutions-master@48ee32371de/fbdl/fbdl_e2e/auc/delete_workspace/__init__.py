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
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage
from fbdl_e2e.entity.pcf_rest_validation import PCFRestRequest
from fbdl_e2e.entity.vSphere_validation import vSphereValidation

from .delete_workspace_context import DeleteWorkSpaceContext
from fbdl_e2e.entity import DACRESTQuery
from urlparse import urljoin

class DeleteWorkspace(BaseUseCase):
    """
    Data scientist delete workspace
    """

    def setUp(self):
        DeleteWorkSpaceContext.validate()
        key = 'created_workspace_names'
        self._ws_list = DeleteWorkSpaceContext.get(key)
        self._ws_name = self._ws_list[-1]
        self.detail_page = WSDetailsPage()
        _rest_service = DeleteWorkSpaceContext.get('dac_service')
        if _rest_service.find('http://') == -1:
            _rest_service = 'http://' + _rest_service
        self._rest_service = urljoin(_rest_service,'dac/rest/1.0/')
        if not self.detail_page.btnDeleteWS.enabled:
            self.__navigate_to_workspace_details_page(self._ws_name)

    def test_delete_workspace(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.assertTrue(self.detail_page.btnDeleteWS.enabled,
                        msg=_formatter(step='Click delete workspace button'))
        # self._VM_list = self.detail_page.get_deployed_workbenches()
        self._ws_id = self.detail_page.workspace_id
        self._cluster_list = self.__get_deployed_cluster_name_list()
        self.assertIsNotNone(self._ws_id,
                             msg=_formatter(step='Get current url'))

        self.detail_page.btnDeleteWS.click()
        self.assertTrue(self.detail_page.fmDeleteWS.exists(),
                        msg=_formatter(step='Alert delete workspace dialog'))

        self.detail_page.txtDeleteWSName.set(self._ws_name)
        self.detail_page.btnConfirm.click()
        self.__wait_for_redirection()
        self.assertFalse(self.__target_workspace_exists(self._ws_name),
                         msg=_formatter(step='Delete workspace'))

        self.__validate_space_is_deleted_from_pcf()
        self.__validate_manifest_is_deleted_from_dac()
        self.__validate_clusters_are_deleted_from_vSphere()
        _created_workspaces = DeleteWorkSpaceContext.get('created_workspace_names')
        _created_workspaces.pop(-1)
        DeleteWorkSpaceContext.set('created_workspace_names', _created_workspaces)

    def runTest(self):
        self.test_delete_workspace()

    def __navigate_to_workspace_details_page(self, ws_name):
        self.main_page = MainPage(workspace_name=ws_name)

        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.assertTrue(
            self.main_page.lnkWorkspace.exists(),
            msg=_formatter(
                step='Navigate to My Workspace page'))
        self.main_page.lnkWorkspace.click()

        self.assertTrue(
            self.__target_workspace_exists(ws_name),
            msg=_formatter(
                step='Navigate to Workspace Details page'))
        self.main_page.get_target_workspace(self._ws_name).click()

    def __target_workspace_exists(self, ws_name):
        if self.main_page.ws_container.exists():
            self.main_page.page_down_to_the_bottom()
            target_ws = self.main_page.get_target_workspace(ws_name)
            if target_ws:
                return True
        return False

    def __wait_for_redirection(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        import time
        timeout = 30
        self.main_page = MainPage()
        while timeout > 0 and (not self.main_page.lblWorkspaceTitle.exists()):
            time.sleep(1)
            timeout -= 1
        self.assertTrue(self.main_page.lblWorkspaceTitle.exists(),
                        msg=_formatter(step='Automatically redirect to workspaces page'))

    def __validate_space_is_deleted_from_pcf(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        pcf_username = None
        pcf_password = None
        _primary_user = DeleteWorkSpaceContext.get('primary_user')
        if _primary_user:
            pcf_username = _primary_user.get('username')
            pcf_password = _primary_user.get('password')

        _pcf_info = DeleteWorkSpaceContext.get('pcf_info', True)
        pcf_org = _pcf_info['organization']
        pcf_api_url = _pcf_info['api_url']
        pcf_uaa_url = _pcf_info['uaa_url']
        pcf_space = self._ws_name
        with PCFRestRequest(
                username=pcf_username,
                password=pcf_password,
                api_url=pcf_api_url,
                uaa_url=pcf_uaa_url
        ) as pcf_rest:
            self.assertTrue(pcf_rest.verify_space_deleted(pcf_org, pcf_space),
                            msg=_formatter(step='Validate space is deleted from PCF'))

    def __validate_clusters_are_deleted_from_vSphere(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        _vSphere_info = DeleteWorkSpaceContext.get('vSphere_info', True)
        host_address = _vSphere_info['host_address']
        username = _vSphere_info['username']
        password = _vSphere_info['password']
        port = _vSphere_info['port']
        with vSphereValidation(
            hostaddress=host_address,
            username=username,
            password=password,
            port=port
        ) as vSphere_session:
            # for _VM in self._VM_list:
            #     self.assertTrue(vSphere_session.verify_VM_not_exist_in_vCenter(_VM),
            #                     msg=_formatter(step='Validate VM is deleted from vSphere'))
            default_timeout = 600
            timer = 0
            while timer < default_timeout:
                timer += 1
                for _cluster in self._cluster_list:
                    result = vSphere_session.verify_Folder_not_exist_in_vCenter(_cluster)
                    if result:
                        self._cluster_list.remove(_cluster)
                if len(self._cluster_list) == 0:
                    break
            self.assertEqual(len(self._cluster_list), 0,
                             msg=_formatter(step='Validate Clusters are deleted from vSphere'))



    def __validate_manifest_is_deleted_from_dac(self):

        _list_asset_url = urljoin(self._rest_service,
                                  'asset/list?TemplateCategory={category}&pageNumber=1&pageSize=100'
                                  '&origin=workspace&workspaceId={workspaceId}&state={state}').format

        # validate registered datasets are deleted
        query = DACRESTQuery(_list_asset_url(category='data', workspaceId=self._ws_id, state='registered'))
        _asset_list = query.get_assets_name_list()
        self.assertIsNotNone(_asset_list, msg='Get registered datasets manifests from dac rest service failed')
        self.assertEqual(_asset_list, 0, msg='Registered datasets manifests were not deleted: {name_list}'
                         .format(name_list=_asset_list))

        # validate registered apps are deleted
        query = DACRESTQuery(_list_asset_url(category='app', workspaceId=self._ws_id, state='registered'))
        _asset_list = query.get_assets_name_list()
        self.assertIsNotNone(_asset_list, msg='Get registered app manifests from dac rest service failed')
        self.assertEqual(_asset_list, 0, msg='Registered app manifests were not deleted: {name_list}'
                         .format(name_list=_asset_list))

        # validate deployed datasets are deleted
        query = DACRESTQuery(_list_asset_url(category='data', workspaceId=self._ws_id, state='deployed'))
        _asset_list = query.get_assets_name_list()
        self.assertIsNotNone(_asset_list, msg='Get deployed datasets manifests from dac rest service failed')
        self.assertEqual(_asset_list, 0, msg='Deployed datasets manifests were not deleted: {name_list}'
                         .format(name_list=_asset_list))

        # validate deployed apps are deleted
        query = DACRESTQuery(_list_asset_url(category='app', workspaceId=self._ws_id, state='deployed'))
        _asset_list = query.get_assets_name_list()
        self.assertIsNotNone(_asset_list, msg='Get deployed app manifests from dac rest service failed')
        self.assertEqual(_asset_list, 0, msg='Deployed app manifests were not deleted: {name_list}'
                         .format(name_list=_asset_list))

    def __get_deployed_cluster_name_list(self):
        _list_asset_url = urljoin(self._rest_service,
                                  'asset/list?TemplateCategory=app&TemplateClass=FBDLController&pageNumber=1'
                                  '&pageSize=100&origin=workspace&workspaceId={workspaceId}&state=deployed'
                                  .format(workspaceId=self._ws_id))
        query = DACRESTQuery(_list_asset_url)
        _asset_list = query.get_assets_name_list()
        self.assertIsNotNone(_asset_list, msg='Get deployed FBDLController manifests from dac rest service failed')
        if _asset_list == 0:
            return []
        else:
            return _asset_list