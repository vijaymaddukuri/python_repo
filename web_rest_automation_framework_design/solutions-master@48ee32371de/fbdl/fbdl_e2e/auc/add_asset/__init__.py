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
from fbdl_e2e.auc.add_asset.add_asset_context import AddAssetContext
from fbdl_e2e.auc.uimap.shared import WSDetailsPage
from fbdl_e2e.auc.uimap.shared import MainPage
from cliacore import CLIRunner
from robot.api import logger
import os
import subprocess, shlex
from threading import Timer


class AddAsset(BaseUseCase):
    def setUp(self):

        AddAssetContext.validate()
        self._target_VM = AddAssetContext.get('dac_cli_address')
        self._username = AddAssetContext.get('dac_cli_username')
        self._password = AddAssetContext.get('dac_cli_password')
        self.__set_asset_info()

        self._ws_name = AddAssetContext.get('created_workspace_names')[-1]

        self.detail_page = WSDetailsPage()
        if not self.detail_page.btnDeleteWS.enabled:
            self.__navigate_to_workspace_details_page(self._ws_name)
        self._ws_id = self.detail_page.workspace_id

    def test_add_asset(self):
        _data_type_list = ['.csv']
        _app_type_list = ['.rpm']
        _tempate_type_list = ['.yaml']
        import sys
        cur_system = sys.platform
        if 'win' not in cur_system:
            self.__copy_asset_to_workbench_VM_in_linux()
        else:
            self.__copy_asset_to_workbench_VM_in_windows()

        flag = AddAssetContext.get('add_asset_to_hadoop')
        if flag:
            self.__set_hadoop_info()
            self.__copy_asset_from_workbench_to_hadoop()
            self._hdfs_path = "hdfs://{name_node_host}:{port}/{dir}".format(
                name_node_host=self._named_node_host, port='8020', dir=self._hadoop_dir)
        if self._extension in _tempate_type_list:
            _asset_key = 'register_template_format'
            _asset_type = 'template'
            _asset_category = 'template'
            _asset_class = 'template'
            _to_register_asset = self.__set_to_register_asset(_asset_key, _asset_category, _asset_class, _asset_type)
            AddAssetContext.set('to_register_templates', [_to_register_asset])
        else:
            _asset_key = 'register_asset_format'
            _asset_type = str(self._extension).strip('.')
            if self._extension in _data_type_list:
                _asset_category = 'data'
                _asset_class = 'file'
            elif self._extension in _app_type_list:
                _asset_category = 'app'
                _asset_class = 'installer'
            else:
                _asset_category = 'data'
                _asset_class = 'directory'
                _asset_type = 'localdirectory'

            _to_register_asset = self.__set_to_register_asset(_asset_key, _asset_category, _asset_class, _asset_type)
            if flag:
                _to_register_asset['hdfs_path'] = self._hdfs_path
                _to_register_asset['path'] = '/' + self._hadoop_dir
                if _to_register_asset['type'] == 'localdirectory':
                    _to_register_asset['type'] = 'hdfsdirectory'

            AddAssetContext.set('to_register_assets', [_to_register_asset])

        _assets_info_list = AddAssetContext.get('assets_info')
        _assets_info_list = _assets_info_list.pop(-1)
        AddAssetContext.set('assets_info', _assets_info_list)

    def runTest(self):
        self.test_add_asset()

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

    def __run_command(self, cmd, timeout):
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kill_proc = lambda p: p.kill()
        timer = Timer(timeout, kill_proc, [proc])
        try:
            timer.start()
            stdout, stderr = proc.communicate()
        finally:
            timer.cancel()
            return proc.returncode, stdout, stderr

    def __set_asset_info(self):

        _asset_info = None
        _asset_info_list = AddAssetContext.get('assets_info', False)
        if _asset_info_list:
            _asset_info = _asset_info_list[-1]

        self.assertTrue(bool(_asset_info), msg='No asset info provided')

        self._local_path = _asset_info['local_path']
        self._remote_path = _asset_info['remote_path']
        self._file_name = _asset_info['file_name']
        self._extension = os.path.splitext(self._file_name)[-1]
        _file_prefix = os.path.splitext(self._file_name)[0]
        from datetime import datetime
        self._new_file_name = _file_prefix + \
                              datetime.now().strftime('%y%m%d%H%M') +\
                              self._extension
        # self._new_file_name = _asset_info['file_name']

        self._asset_prefix = _asset_info['visible_name']
        self._local_file = os.path.join(self._local_path, self._file_name)
        self._remote_file = os.path.join(self._remote_path, self._new_file_name)

    def __set_to_register_asset(self, format_key, asset_category, asset_class, asset_type):
        _to_register_asset = AddAssetContext.get(format_key)
        _to_register_asset['type'] = asset_type
        _to_register_asset['category'] = asset_category
        _to_register_asset['class'] = asset_class
        _to_register_asset['path'] = self._remote_path
        _to_register_asset['file_name'] = self._new_file_name
        _to_register_asset['manifest_entry']['WorkspaceId'] = self._ws_id
        from datetime import datetime
        _to_register_asset['visible_name'] = self._asset_prefix + \
                                             datetime.now().strftime('%y%m%d%H%M')
        return _to_register_asset

    def __copy_asset_to_workbench_VM_in_linux(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.assertTrue(os.path.exists(self._local_file),
                        msg=_formatter(step='Check asset file exists'))

        scp_command = 'sshpass -p "{password}" scp -r -o StrictHostKeyChecking=no {local_file} ' \
                      '{username}@{target_address}:{remote_file}'.format(username=self._username,
                                                                         password=self._password,
                                                                         local_file=self._local_file,
                                                                         remote_file=self._remote_file,
                                                                         target_address=self._target_VM
                                                                         )
        logger.debug(scp_command,False)
        response, stdout, stderr = self.__run_command(scp_command, 60)
        logger.debug(stdout, False)
        logger.debug(stderr, False)
        self.assertEqual(response, 0,
                         msg=_formatter(step='Copy local file to workbench VM through SCP'))

        check_file_command = 'sshpass -p "{password}" ssh -o StrictHostKeyChecking=no {username}@{host} ' \
                             'test -e {remote_file}'.format(username=self._username,
                                                            password=self._password,
                                                            host=self._target_VM,
                                                            remote_file=self._remote_file)
        logger.debug(check_file_command, False)

        response, stdout, stderr = self.__run_command(check_file_command, 60)
        logger.debug(stdout, False)
        logger.debug(stderr, False)
        self.assertEqual(response, 0,
                         msg=_formatter(step='Validate file successfully transferred'))

    def __copy_asset_to_workbench_VM_in_windows(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        # hostname = '172.16.180.248'
        # self._ssh = CLIRunner(hostname=hostname, username='root',
        #                       password='pancake')
        hostname = '172.50.2.56'
        self._ssh = CLIRunner(hostname=hostname, username='root',
                              password='1q2W3e4R5t')

        self.assertIsNotNone(self._ssh,
                             msg=_formatter(step='SSH connection was not established.'))
        # self._ssh.run_command("sed -i -e 's/Defaults    requiretty.*/ #Defaults    requiretty/g' /etc/sudoers")
        response = self._ssh.run_command(
            'sshpass -p "{password}" scp -r -o StrictHostKeyChecking=no {local_file} '
            '{username}@{target_address}:{remote_file}'.format(username=self._username,
                                                       password=self._password,
                                                       local_file=self._local_file,
                                                       target_address=self._target_VM,
                                                       remote_file=self._remote_file)
        )

        logger.debug(response, False)

    def __set_hadoop_info(self):
        _hadoop_info = AddAssetContext.get('hadoop_info')
        self._hadoop_ip = _hadoop_info.get('name_node_ip')
        self._hadoop_user = _hadoop_info.get('user')
        self._hadoop_password = _hadoop_info.get('password')
        self._hadoop_dir = 'auto'
        self._named_node_host = _hadoop_info.get('host')

    def __copy_asset_from_workbench_to_hadoop(self):
        self._ssh = CLIRunner(hostname=self._target_VM,
                              username=self._username,
                              password=self._password)
        _temp_file = os.path.join('/tmp/', self._new_file_name)
        scp_command = 'sshpass -p "{password}" scp -r -o StrictHostKeyChecking=no {local_file} ' \
                      '{username}@{target_address}:{remote_file}'.format(username=self._hadoop_user,
                                                                         password=self._hadoop_password,
                                                                         local_file=self._remote_file,
                                                                         remote_file=_temp_file,
                                                                         target_address=self._hadoop_ip
                                                                         )
        logger.debug('Running command -- {}'.format(scp_command))
        response = self._ssh.run_command(scp_command)

        self.assertFalse(
            response.strip() and (
                '\n0' not in response) and (
                self._hadoop_dir not in response),
            msg='Unable to copy file to name node: {hadoop_ip}\r\n Reason: {err}'.format(
                hadoop_ip=self._hadoop_ip, err=response))

        check_file_command = 'sshpass -p "{password}" ssh -tt -o StrictHostKeyChecking=no {username}@{host} ' \
                             'test -e {remote_file} && echo $?'.format(username=self._hadoop_user,
                                                                       password=self._hadoop_password,
                                                                       host=self._hadoop_ip,
                                                                       remote_file=_temp_file)
        logger.debug('Running command -- {}'.format(check_file_command))
        response = self._ssh.run_command(check_file_command)

        self.assertFalse(
            response.strip() and ('\n0' not in response),
            msg='Unable to copy file to name node: {hadoop_ip}\r\n Reason: {err}'.format(
                hadoop_ip=self._hadoop_ip, err=response))

        create_dir_command = 'sshpass -p "{password}" ssh -tt -o StrictHostKeyChecking=no {username}@{host} ' \
                             'sudo -u hdfs hadoop fs -mkdir /{dir}'.format(
            username=self._hadoop_user, password=self._hadoop_password,
            host=self._hadoop_ip, dir=self._hadoop_dir)
        logger.debug('Running command -- {}'.format(create_dir_command))
        response = self._ssh.run_command(create_dir_command)

        self.assertFalse(
            response.strip() and (
                '\n0' not in response) and (
                self._hadoop_ip not in response) and (
                'File exists' not in response),
            msg='Creating directory: "{dir}" in Hadoop was failed.\r\n Reason: {err}'.format(
                dir=self._hadoop_dir, err=response))

        put_file_command = 'sshpass -p "{password}" ssh -tt -o StrictHostKeyChecking=no {username}@{host} ' \
                             'sudo -u hdfs hadoop fs -put {remote_file} /{dir}'.format(
            username=self._hadoop_user, password=self._hadoop_password,
            host=self._hadoop_ip, remote_file=_temp_file, dir=self._hadoop_dir)

        logger.debug('Running command -- {}'.format(put_file_command))
        response = self._ssh.run_command(put_file_command)

        self.assertFalse(
            response.strip() and (
                self._hadoop_ip not in response) and (
                'File exists' not in response),
            msg='Failed to put file into Hadoop file system '
                '(name node: {hadoop_ip}). \r\n Reason: {err}'.format(
                hadoop_ip=self._hadoop_ip, err=response))

        # Remove the local file on name node to bypass an issue of publishing dataset
        self._ssh.run_command(
            'sshpass -p "{password}" ssh -tt -o StrictHostKeyChecking=no '
            '{username}@{host} sudo rm -fr {remote_file}'.format(
                username=self._hadoop_user, password=self._hadoop_password,
                host=self._hadoop_ip, remote_file=_temp_file))

        check_file_command = 'sshpass -p "{password}" ssh -tt -o StrictHostKeyChecking=no {username}@{host} ' \
                             'sudo -u hdfs hadoop fs -test -e /{dir}/{file_name} && echo $?'.format(
            username=self._hadoop_user, password=self._hadoop_password,
            host=self._hadoop_ip, dir=self._hadoop_dir,
            file_name=self._new_file_name)

        logger.debug('Running command -- {}'.format(check_file_command))
        response = self._ssh.run_command(check_file_command)

        self.assertFalse(
            response.strip() and ('\n0' not in response),
            msg='Validating file in Hadoop file system '
                '(name node: {hadoop_ip}) was failed. \r\n Reason: {err}'.format(
                hadoop_ip=self._hadoop_ip, err=response))
