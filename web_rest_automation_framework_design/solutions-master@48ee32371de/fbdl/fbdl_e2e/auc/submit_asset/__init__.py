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
from fbdl_e2e.auc.submit_asset.submit_asset_context import SubmitAssetContext
from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.entity.dac_cli_response import DACCLIResponse
from fbdl_e2e.entity.dac_rest_query import DACRESTQuery
from robot.api import logger
from cliacore import CLIRunner
import requests


class SubmitAsset(BaseUseCase):
    """
    Data scientist submits asset
    """

    def setUp(self):
        SubmitAssetContext.validate()
        self._dac_cli_address = SubmitAssetContext.get('dac_cli_address')
        self._dac_cli_username = SubmitAssetContext.get('dac_cli_username')
        self._dac_cli_password = SubmitAssetContext.get('dac_cli_password')
        self._ssh = CLIRunner(hostname=self._dac_cli_address, username=self._dac_cli_username,
                              password=self._dac_cli_password)
        _registered_assets_obj_list = SubmitAssetContext.get('registered_assets_obj_list')
        self._registered_assets = []
        self._registered_assets.extend([] if _registered_assets_obj_list is None else _registered_assets_obj_list)
        self.assertTrue(len(self._registered_assets)!=0,
                        msg='No registered asset provided')
        self._dac_service = SubmitAssetContext.get('dac_service', True)

    def test_submit_assets(self):
        outputs = []
        for asset_obj in self._registered_assets:
            if asset_obj.code == '0':
                submit_asset_cli = 'dac-cli submit -i {}'.format(asset_obj.guid)
                response = DACCLIResponse(self._ssh.run_command(submit_asset_cli))
                self.assertTrue(response.message=='Success', msg='Asset submit job creation failed: {} '.format(response.raw_message))
                logger.info('Return code: {}, Status: {}, Message: {}'.format(response.code,response.message, response.message_description), False, False)
                self.__wait_for_completion(asset_obj)
                response.copy(asset_obj)
                outputs.append(response)
            else:
                logger.error('asset submit operation failed as no valid GUID...', False)
                continue
        SubmitAssetContext.set('submitted_assets', outputs)

    def runTest(self):
        self.test_submit_assets()

    def __wait_for_completion(self, asset_obj):
        query = DACRESTQuery('http://{}/dac/rest/1.0/asset/process/status''?workspaceId={}&assetGUID={}'.
                             format(self._dac_service,asset_obj.workspace, asset_obj.guid))
        query.run()