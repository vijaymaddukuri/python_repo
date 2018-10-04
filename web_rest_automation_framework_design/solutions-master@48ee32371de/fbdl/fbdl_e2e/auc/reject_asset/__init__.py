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
from fbdl_e2e.auc.reject_asset.reject_asset_context import RejectAssetContext
from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.entity.dac_cli_response import DACCLIResponse
from fbdl_e2e.entity.dac_rest_query import DACRESTQuery
from robot.api import logger
from cliacore import CLIRunner


class RejectAsset(BaseUseCase):
    """
    Data scientist rejects asset
    """

    def setUp(self):
        RejectAssetContext.validate()
        self._dac_cli_address = RejectAssetContext.get('dac_cli_address')
        self._dac_cli_username = RejectAssetContext.get('dac_cli_username')
        self._dac_cli_password = RejectAssetContext.get('dac_cli_password')
        self._ssh = CLIRunner(hostname=self._dac_cli_address, username=self._dac_cli_username,
                              password=self._dac_cli_password)
        self._submitted_assets = RejectAssetContext.get('submitted_assets')
        self._dac_service = RejectAssetContext.get('dac_service')

    def test_reject_assets(self):
        outputs = []
        for asset_obj in self._submitted_assets:
            if asset_obj.code == '0':
                new_guid = self.__get_asset_guid(asset_obj)
                submit_asset_cli = 'dac-cli reject -i {} -m \'gse automation\''.format(new_guid)
                response = DACCLIResponse(self._ssh.run_command(submit_asset_cli))
                response.guid = new_guid
                response.workspace = asset_obj.workspace
                self.assertTrue(response.message=='Success', msg='Asset reject operation failed: {} .'.format(response.raw_message))
                logger.info('Return code: {}, Status: {}, Message: {}'.format(response.code,response.message, response.message_description), False, False)
                self.__wait_for_completion(response)
                self.assertTrue(self.__is_asset_rejected(response), msg='Asset reject operation failed: {} .'.format(response.raw_message))
                outputs.append(response)
            else:
                logger.error('asset reject operation failed as no valid GUID...', False)
                continue
        RejectAssetContext.set('rejected_assets', outputs)

    def runTest(self):
        self.test_reject_assets()

    def __get_asset_guid(self, asset_obj):
        filter = asset_obj.guid if asset_obj.guid!='' else asset_obj.name
        list_asset_cli = 'dac-cli list -c {} -a -e pendingPublication | grep \'{}\''.format(asset_obj.category, filter)
        logger.debug(list_asset_cli, True)
        import time
        time.sleep(5)
        cli_response = self._ssh.run_command(list_asset_cli)
        logger.debug('Search the pending publication asset by original GUID...', True)
        logger.debug(cli_response, True)
        fields = cli_response.split('|')
        if len(fields) < 39:
            logger.error('Publication GUID was not found!', False)
            raise AssertionError('Publication GUID was not found! ')
        else:
            index = self.__index_of_column(asset_obj.category, 'AssetGUID')
            return fields[index].strip()

    def __index_of_column(self, category, col_name):
        response = self._ssh.run_command('dac-cli list -c {} -a -e pendingPublication|grep {}'.format(category, col_name))
        if response is None or response=='':
            logger.error('Can locate the index of column {}!'.format(col_name))
            raise AssertionError('Can locate the index of column {}!'.format(col_name))
        col_array = response.split('|')
        col_array = [column.strip() for column in col_array]
        index = col_array.index(col_name)
        return index

    def __is_asset_rejected(self, asset_obj):
        filter = asset_obj.guid if asset_obj.guid!='' else asset_obj.name
        list_published_asset_cli = 'dac-cli list -c {} -a | grep \'{}\''.format(asset_obj.category, filter)
        logger.debug(list_published_asset_cli, True)
        cli_response = self._ssh.run_command(list_published_asset_cli)
        logger.debug('Search the published asset by original GUID...', True)
        logger.debug(cli_response, True)
        if cli_response is not None and cli_response!='':
            logger.info('Asset {} is still found!'.format(asset_obj.name))
            return False
        else:
            return True

    def __wait_for_completion(self, asset_obj):
        import time
        time.sleep(1)