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
from fbdl_e2e.auc.accept_asset.accept_asset_context import AcceptAssetContext
from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.entity.dac_cli_response import DACCLIResponse
from fbdl_e2e.entity.dac_rest_query import DACRESTQuery
from robot.api import logger
from cliacore import CLIRunner


class AcceptAsset(BaseUseCase):
    """
    Data scientist accepts asset
    """

    def setUp(self):
        AcceptAssetContext.validate()
        self._dac_cli_address = AcceptAssetContext.get('dac_cli_address')
        self._dac_cli_username = AcceptAssetContext.get('dac_cli_username')
        self._dac_cli_password = AcceptAssetContext.get('dac_cli_password')
        self._ssh = CLIRunner(hostname=self._dac_cli_address, username=self._dac_cli_username,
                              password=self._dac_cli_password)
        self._submitted_assets = AcceptAssetContext.get('submitted_assets')
        self._dac_service = AcceptAssetContext.get('dac_service', True)

    def test_accept_assets(self):
        outputs = []
        for asset_obj in self._submitted_assets:
            if asset_obj.code == '0':
                new_guid = self.__get_asset_guid(asset_obj)
                submit_asset_cli = 'dac-cli accept -i {}'.format(new_guid)
                response = DACCLIResponse(self._ssh.run_command(submit_asset_cli))
                response.guid = new_guid
                response.workspace = asset_obj.workspace
                response.category=asset_obj.category
                response.name = asset_obj.name
                self.assertTrue(str(response.message).strip()=='Success', msg='Asset accept operation failed: {} .'.format(response.raw_message))
                logger.info('Return code: {}, Status: {}, Message: {}'.format(response.code,response.message, response.message_description), False, False)
                self.__wait_for_completion(response)
                self.assertTrue(self.__is_asset_accepted(response), msg='Asset accept operation failed: {} .'.format(response.raw_message))
                outputs.append(response)
            else:
                logger.error('asset accept operation failed as no valid GUID...', False)
                continue

        _accepted_tools_list = [{'name': output.name}
                                for output in outputs
                                if output.category == 'app']
        _accepted_datasets_list = [{'name': output.name}
                                   for output in outputs
                                   if output.category == 'data']

        AcceptAssetContext.set('accepted_datasets', _accepted_datasets_list)
        AcceptAssetContext.set('accepted_tools', _accepted_tools_list)
        AcceptAssetContext.set('submitted_assets', [])


    def runTest(self):
        self.test_accept_assets()

    def __get_asset_guid(self, asset_obj):
        filter = asset_obj.guid if asset_obj.guid!='' else asset_obj.name
        list_asset_cli = 'dac-cli list -c {} -a -e pendingPublication | grep \'{}\''.format(asset_obj.category, filter)
        logger.debug(list_asset_cli, True)
        import time
        time.sleep(7)
        cli_response = self._ssh.run_command(list_asset_cli)
        logger.debug('Search the pending publication asset by original GUID...', True)
        logger.debug(cli_response, True)
        fields = cli_response.split('|')
        if len(fields) < 39:
            logger.error('Publication GUID was not found!', False)
            raise AssertionError('Publication GUID was not found! ')
        else:
            index = self.__index_of_column(asset_obj.category, 'AssetGUID')
            guid = fields[index].strip()
            return guid

    def __index_of_column(self, category, col_name):
        response = self._ssh.run_command('dac-cli list -c {} -a -e pendingPublication|grep {}'.format(category, col_name))
        if response is None or response=='':
            logger.error('Can locate the index of column {}!'.format(col_name))
            raise AssertionError('Can locate the index of column {}!'.format(col_name))
        col_array = response.split('|')
        col_array = [column.strip() for column in col_array]
        index = col_array.index(col_name)
        return index

    def __is_asset_accepted(self, asset_obj):
        filter = asset_obj.guid if asset_obj.guid!='' else asset_obj.name
        list_published_asset_cli = 'dac-cli list -c {} -a -e published | grep \'{}\''.format(asset_obj.category, filter)
        logger.debug(list_published_asset_cli, True)
        cli_response = self._ssh.run_command(list_published_asset_cli)
        logger.debug('Search the published asset by original GUID...', True)
        logger.debug(cli_response, True)
        if cli_response is not None and cli_response!='':
            logger.info('Asset {} is published successfully!'.format(asset_obj.name))
            return True
        else:
            return False

    def __wait_for_completion(self, asset_obj):
        query = DACRESTQuery('http://{}/dac/rest/1.0/asset/process/status''?workspaceId={}&assetGUID={}'\
            .format(self._dac_service,asset_obj.workspace, asset_obj.guid))
        query.run()
