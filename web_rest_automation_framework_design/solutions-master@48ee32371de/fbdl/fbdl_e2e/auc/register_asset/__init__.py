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

from cliacore import CLIRunner
from robot.api import logger

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.register_asset.register_asset_context import RegisterAssetContext
from fbdl_e2e.entity.dac_cli_response import DACCLIResponse


class RegisterAsset(BaseUseCase):
    """
    Data scientist registers asset
    """

    def setUp(self):
        RegisterAssetContext.validate()
        self._dac_cli_address = RegisterAssetContext.get('dac_cli_address')
        self._dac_cli_username = RegisterAssetContext.get('dac_cli_username')
        self._dac_cli_password = RegisterAssetContext.get('dac_cli_password')
        self._ssh = CLIRunner(hostname=self._dac_cli_address, username=self._dac_cli_username,
                              password=self._dac_cli_password)
        self._to_register_assets = RegisterAssetContext.get('to_register_assets')

    def __generate_manifest_str(self, manifest):
        manifest_dict = {}
        workspace = ''
        arg_type = str(type(manifest))
        if arg_type == "<type 'dict'>":
            manifest_dict = manifest
        elif arg_type == "<type 'str'>":
            import ast
            manifest_dict = ast.literal_eval(manifest)
        else:
            logger.error('Not supported type for manifest!', False)
            raise ValueError('Not supported type for manifest!')
        rt_str = ''
        for key, value in manifest_dict.items():
            rt_str += '-k \'{}={}\' '.format(key, value)
            if key == 'WorkspaceId':
                workspace = value
        return rt_str, workspace

    def test_register_assets(self):
        outputs = []
        for asset_obj in self._to_register_assets:
            for key, value in asset_obj.items():
                # hdfs_path and port are optional
                if key =='hdfs_path' or key =='port':
                    continue
                self.assertFalse( (asset_obj[key] is None) or (asset_obj[key]==''), msg='{} is not specified.'.format(key))

            manifest_str, workspace = self.__generate_manifest_str(asset_obj['manifest_entry'])
            _new_file = asset_obj['file_name'] #self.__change_file_or_dir_name(asset_obj['path'],asset_obj['file_name'])
            register_asset_cli = 'dac-cli register -p \'{}\' -f {} -c {} -t {} -s {} {} -vn {} -sd \'{}\' -un {}' ' -wm {} -wp {}'\
                .format(asset_obj['path'], _new_file, asset_obj['category'], asset_obj['type'],
                        asset_obj['class'], manifest_str,asset_obj['visible_name'],
                        asset_obj['short_description'], asset_obj['user_name'],asset_obj['work_email'],asset_obj['work_phone'])
            # check whether it's hadoop asset
            if asset_obj.get('hdfs_path', None) and asset_obj['hdfs_path'].strip():
                register_asset_cli = '{} -u {}/{} -port {}'.format(register_asset_cli, asset_obj['hdfs_path'],_new_file, asset_obj['port'])
            self.assertIsNotNone(self._ssh, 'SSH connection was not established.')
            response = DACCLIResponse(self._ssh.run_command(register_asset_cli))
            response.workspace = workspace
            response.category = asset_obj['category']
            response.name = asset_obj['visible_name']
            self.assertTrue(response.message=='Success', msg='Asset register operation failed: {} '.format(response.raw_message))
            logger.debug('Return code: {}, Status: {}, Message: {}, GUID: {}'.format(response.code,response.message,
                                                                                    response.message_description, response.guid), True)
            outputs.append(response)
        data_assets_list = [output.name for output in outputs if output.category == 'data']
        app_assets_list = [output.name for output in outputs if output.category == 'app']
        RegisterAssetContext.set('registered_datasets', data_assets_list)
        RegisterAssetContext.set('registered_tools', app_assets_list)
        RegisterAssetContext.set('registered_assets_obj_list', outputs)

    def __change_file_or_dir_name(self, path, file_name):
        old_name = file_name
        new_name = self.__add_suffix(file_name)
        self._ssh.run_command('mv {}/{} {}/{}'.format(path, old_name, path,new_name))
        return new_name

    def __add_suffix(self, path):
        import os.path
        from datetime import datetime
        file_split = os.path.splitext(path)
        extension = file_split[1]
        suffix = datetime.now().strftime('%y%m%d%H%M')
        if extension is None or extension=='':
            path = path+ suffix
            return path
        else:
            path = '{}{}{}'.format(file_split[0],suffix, file_split[1])
            return path

    def runTest(self):
        self.test_register_assets()