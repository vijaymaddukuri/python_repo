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

from urlparse import urlparse
from cliacore import CLIRunner

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, WorkingSetsPage
from fbdl_e2e.workflow import Context


class ValidateDeployedDataset(BaseUseCase):
    """
    Validate the deployed dataset for any specific data container
    """

    def setUp(self):
        """
        Make sure the current user is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()

        if not self.details_page.btnShowDSDetails.exists():
            key = 'created_workspace_names'
            Context.validate([key])
            self._ws_name = list(Context.get(key))[-1]

            self.__navigate_to_workspace_details_page(self._ws_name)

        key = 'deployed_datasets'
        Context.validate([key])
        self._lstDataSets = Context.get(key)

        self._ssh_info = {
            'hostname': 'dac_cli_address',
            'username': 'dac_cli_username',
            'password': 'dac_cli_password',
        }

        for key, value in self._ssh_info.iteritems():
            self._ssh_info[key] = Context.get(value)

        # if not self._ssh_info['hostname']:
        #     # Get workbench VM's IP address / ssh credential
        #     _workbench = self.details_page.get_deployed_workbenches_elements()[0]
        #     _workbench.find_element_by_tag_name('a').click()
        #
        #     ssh = self.details_page.lblSSH.value.split()[-1].split('@')
        #     self._ssh_info['hostname'] = ssh[-1]
        #     self._ssh_info['username'] = ssh[0]

    def test_deployed_dataset(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertGreater(
            len(self._lstDataSets), 0,
            msg=_formatter(step='Validate deployed datasets context'))

        self.ws_page = WorkingSetsPage()
        self.details_page.btnShowDSDetails.click()
        self.assertTrue(
            self.ws_page.datasets_container.exists(),
            msg=_formatter(step='Navigate to workingset page'))

        for ds in self._lstDataSets:
            _ws_name = ds.get('workingset')
            self.ws_page = WorkingSetsPage(_ws_name)

            self.__validate_deployed_dataset(name=_ws_name)

        self.ws_page.btnBackToWorkspaceDetails.click()

    def runTest(self):
        self.test_deployed_dataset()

    def __navigate_to_workspace_details_page(self, ws_name):
        self.main_page = MainPage(workspace_name=ws_name)

        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.assertTrue(
            self.main_page.lnkWorkspace.exists(),
            msg=_formatter(
                step='Navigate to My Workspace page'))
        self.main_page.lnkWorkspace.click()

        self.assertTrue(
            self.main_page.lnkTargetWorkspace.enabled,
            msg=_formatter(
                step='Navigate to Workspace Details page'))
        self.main_page.lnkTargetWorkspace.click()

    def __validate_deployed_dataset(self, name):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.ws_page.page_down_to_the_bottom()
        _datasets = [ds.text.split('\n')[0]
                     for ds in self.ws_page.deployed_datasets]

        self.assertIn(
            name,
            _datasets,
            msg=_formatter(step='Validate the specific deployed dataset'))

        _btnExpand = self.ws_page.btnExpand
        self.assertIsNotNone(
            _btnExpand,
            msg=_formatter(step='Show detailed information of the deployed dataset'))
        _btnExpand.click()

        _kvp = {
            'username': 'Container User Name',
            'password': 'Container Password',
            'url': 'Container URL', }

        for key, value in _kvp.iteritems():
            _kvp[key] = self.ws_page.get_dataset_info_by_key(value)

        _kvp['username'] = _kvp['username'] or self._ssh_info['username']
        _kvp['password'] = _kvp['password'] or self._ssh_info['password']

        _url = _kvp.pop('url')

        self.assertIsNotNone(
            _url, msg=_formatter(step='Retrieve Container URL'))

        if _url.startswith('/'):
            self.__validate_local_file_system(_url)
        elif '://' in _url:
            _url = urlparse(_url)

            _kvp['hostname'] = _url.hostname
            _kvp['port'] = _url.port
            _kvp['path'] = _url.path

            _validation_strategies = {
                'HDFS': self.__validate_info_in_hadoop_container,
                'MYSQL': self.__validate_info_in_mysql_container,
                'MONGO': self.__validate_info_in_mongodb_container,
            }

            _invoker = _validation_strategies.get(_url.scheme.upper(), None)

            self.assertIsNotNone(
                _invoker,
                msg=_formatter(step='Validating container of {}'.format(_url))
            )

            if callable(_invoker):
                _invoker(**_kvp)
        else:
            self.fail(msg='Failed to identify Container URL')

    def __validate_local_file_system(self, path):
        _ret = CLIRunner(**self._ssh_info).run_command(
            'test -e {} && echo $?'.format(path))

        self.assertTrue(
            '\n0\n' in _ret,
            msg='Validate the dataset within workbench VM was failed'
        )

    def __validate_info_in_hadoop_container(self, **kwargs):
        # _ssh_cmd = 'sshpass -p "{password}" ssh -tt -o StrictHostKeyChecking=no ' \
        #            '{username}@{hostname} sudo -u hdfs hadoop fs -ls {path}'.format(**kwargs)
        _key = 'deployed_tools'
        _tools = Context.get(_key)
        if _tools:
            _tool = _tools.pop()

            _key = 'Master Host'
            _hostname = _tool.get(_key)

            if _hostname:
                kwargs['hostname'] = _hostname

        _ssh_cmd = 'sshpass -p "{password}" ssh -tt -o StrictHostKeyChecking=no ' \
                   '{username}@{hostname} sudo -u hdfs hadoop fs -test -e {path} && echo $?'.format(**kwargs)

        _ret = CLIRunner(**self._ssh_info).run_command(_ssh_cmd)

        self.assertFalse(
            _ret.strip() and ('\n0' not in _ret),
            msg='Validating file in HDFS (name node: {hostname}) '
                'was failed. \r\n Reason: {err}'.format(
                hostname=kwargs.get('hostname'), err=_ret))

    def __validate_info_in_mysql_container(self, **kwargs):
        kwargs['db_name'] = kwargs.get('path').split('/')[-2]
        kwargs['tb_name'] = kwargs.get('path').split('/')[-1]

        _ssh_cmd = 'mysql -h{hostname} -P{port} -u{username}' \
                   ' -p{password} {db_name} -e "SELECT * FROM {tb_name};"'.format(**kwargs)

        _ret = CLIRunner(**self._ssh_info).run_command(_ssh_cmd)

        self.assertNotRegexpMatches(
            _ret, '^bash:.*|.*error.*',
            msg='Error issued in the returned result')

        # TODO: Probably need to move the regular expression to
        # TODO: configuration file so that the detailed content can be validated
        self.assertRegexpMatches(
            _ret, '^mysql:.*\n.*\t.*(.*\n.*)+\n$',
            msg='Validating table content in mysql database was failed')

    def __validate_info_in_mongodb_container(self, **kwargs):
        kwargs['db_name'] = kwargs.get('path').split('/')[-2]
        kwargs['coll_name'] = kwargs.get('path').split('/')[-1]

        _ssh_cmd = 'mongo {hostname}/{db_name} ' \
                   '--eval "db.{coll_name}.find()"'.format(**kwargs)

        _ret = CLIRunner(**self._ssh_info).run_command(_ssh_cmd)

        self.assertIsNotNone(
            _ret, msg='Executing MongoDB Shell was Failed')

        _table_content = _ret.strip().split('\n')[-1]
        self.assertNotIn(
            kwargs['db_name'],
            _table_content,
            msg='Validating Table Content in MongoDB was Failed')