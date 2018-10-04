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

import re

from cliacore import CLIRunner
from robot.api import logger

from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.auc.uimap.shared import MainPage, WSDetailsPage, ToolsPage
from fbdl_e2e.workflow import Context


class RetrieveWorkBenchVM(BaseUseCase):
    """
    Retrieve VM info from a  workbench
    """

    def setUp(self):
        """
        Make sure data scientist is now on the Workspace Details page
        """
        self.details_page = WSDetailsPage()
        key = 'created_workspace_names'
        Context.validate([key])
        self._ws_name = list(Context.get(key))[-1]

        if not self.details_page.btnAddServices.enabled:
            self.__navigate_to_workspace_details_page(self._ws_name)

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

    def test_retrieve_workbench_vm(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        import time
        _now = time.time()
        _timeout = 10 * 60

        needrefresh = False
        while (_timeout > (time.time() - _now)) \
                and (len(self.details_page.get_deployed_workbenches()) < 1):
            time.sleep(30)
            needrefresh = True

        if needrefresh:
            self.__navigate_to_workspace_details_page(self._ws_name)

        self.__get_workbench_vm_container()

        if self.details_page.btnShowSVCDetails.exists():
            self.assertTrue(
                self.details_page.btnShowSVCDetails.exists(),
                msg=_formatter(
                    step='Show Detailed List'))

        _workbenches = self.details_page.get_deployed_workbenches()

        self.assertNotEqual(
            len(_workbenches), 0,
            msg=_formatter(step='Validate default workbench'))

        vm_dict = self.__get_default_workbench_vm_info(_workbenches[0])  # only one workbench vm currently
        self.assertIsNotNone(
            vm_dict.get('user'),
            msg=_formatter(step='User of workbench through SSH'))
        self.assertIsNotNone(
            vm_dict.get('host'),
            msg=_formatter(step='Host of workbench through SSH'))
        logger.info('VM: {0}    SSH {1}@{2}'.format(
            _workbenches[0], vm_dict.get('user'), vm_dict.get('host')), also_console=True)

        deployed_svcs = self.details_page.get_deployed_services()
        self.assertGreaterEqual(
            len(deployed_svcs),
            1,
            msg=_formatter(step='Deployed services for workbench'))

        # ip = deployed_svcs[-1] if deployed_svcs else ''
        # servics = Context.get('deployed_services')
        # workbench_vm = {'instance':ip,'name':'workbench'}
        # servics.append(workbench_vm)
        # Context.set('deployed_services', servics)


        try:

            Context.set('dac_cli_address', vm_dict['host'])
            Context.set('dac_cli_username', vm_dict['user'])

            _ssh = CLIRunner(hostname=vm_dict['host'], username=Context.get('dac_cli_username'),
                             password=Context.get('dac_cli_password'))

            dac_svc = Context.get('dac_service', True).replace('/', '\/')
            sed = r"sed -i 's/\(rest_server =\) .*/\1 {service}/' {confpath}".format(service=dac_svc,
                                                                                     confpath=r'/etc/dac-cli/bdldac.conf')
            _ssh.run_command('sudo -u root ' + sed)

            # _ssh.run_command('chown dacuser /var/dac/')
            # _ssh.run_command('chgrp dacuser /var/dac/')
        except:
            logger.error('Unable to SSH {0}@{1}'.format(vm_dict['user'], vm_dict['host']))
            raise ValueError('Error username or password to SSH')
        else:
            logger.info('Succeed to SSH {0}@{1}'.format(
                Context.get('dac_cli_username'), Context.get('dac_cli_address')), also_console=True)

    def runTest(self):
        self.test_retrieve_workbench_vm()

    def __get_workbench_vm_container(self):
        if self.details_page.btnShowSVCDetails.exists():
            self.details_page.btnShowSVCDetails.click()

        self.tool_page = ToolsPage()
        self.tool_page.page_down_to_the_bottom()
        tool_list = self.tool_page.tools_list
        tool_filter = filter(lambda tool: self._ws_name in tool.text.split('\n')[0], tool_list)
        container = ''
        if tool_filter:
            container = tool_filter[-1].text.split('\n')[0]

        servics = Context.get('deployed_services') or []
        workbench_vm = {'instance': container, 'name': 'workbench'}
        servics.append(workbench_vm)
        Context.set('deployed_services', servics)
        self.__navigate_to_workspace_details_page(self._ws_name)

    def __get_default_workbench_vm_info(self, vm_name=''):
        vm_str = ''

        if self.details_page.lblSSH and not self.details_page.lblSSH.exists():
            workbanches = self.details_page.get_deployed_workbenches_elements()
            if vm_name:
                workbanches = [w for w in workbanches if w.text == vm_name]
            if workbanches:
                workbanches[0].find_element_by_tag_name(
                    'a').click()  # click expand to show VM info, and get vm element agagin
            from time import sleep
            sleep(2)
            if self.details_page.lblSSH.exists():
                self.assertTrue(self.details_page.lblSSH.exists(), msg='Show workbench SSH info.')
            vm_str = self.details_page.lblSSH.value

        vm_dict = {}
        pattern_vm = '^\$ ssh (\w*)@((?:\d{1,3}\.?){4})$'
        match = re.search(pattern_vm, vm_str)
        if match:
            vm_dict['user'] = match.group(1)
            vm_dict['host'] = match.group(2)

        return vm_dict
