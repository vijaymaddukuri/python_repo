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
from fbdl_e2e.auc.register_template.register_template_context import RegisterTemplateContext
from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.entity.dac_cli_response import DACCLIResponse
from robot.api import logger
from cliacore import CLIRunner


class RegisterTemplate(BaseUseCase):
    """
    Data scientist registers template
    """

    def setUp(self):
        RegisterTemplateContext.validate()
        self._dac_cli_address = RegisterTemplateContext.get('dac_cli_address')
        self._dac_cli_username = RegisterTemplateContext.get('dac_cli_username')
        self._dac_cli_password = RegisterTemplateContext.get('dac_cli_password')
        self._ssh = CLIRunner(hostname=self._dac_cli_address, username=self._dac_cli_username,
                              password=self._dac_cli_password)
        self._templates = RegisterTemplateContext.get('to_register_templates')

    def __generate_manifest_str(self, manifest):
        manifest_dict = {}
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

    def test_register_templates(self):
        outputs = []
        for template_obj in self._templates:
            for key, value in template_obj.items():
                self.assertFalse( (template_obj[key] is None) or (template_obj[key]==''), msg='{} is not specified.'.format(key))
            manifest_str, workspace = self.__generate_manifest_str(template_obj['manifest_entry'])
            import time
            ts = int(time.time())
            new_template_file = 'template{}.yaml'.format(ts)
            self._ssh.run_command('cp -f {}/{} {}/{}'.format(template_obj['path'],template_obj['file_name'],template_obj['path'],
                                                          new_template_file))
            register_template_cli = 'dac-cli register -p \'{}\' -f {} -c {} -t {} -s {} \'{}\' -vn {} -sd \'{}\' -un {}' \
                .format(template_obj['path'], new_template_file, template_obj['category'], template_obj['type'],
                        'template', manifest_str, template_obj['visible_name'],template_obj['short_description'], template_obj['user_name'])
            self.assertIsNotNone(self._ssh, 'SSH connection was not established.')
            response = DACCLIResponse(self._ssh.run_command(register_template_cli))
            response.workspace = workspace
            response.category = template_obj['category']
            response.name = template_obj['visible_name']
            self.assertTrue(response.message=='Success', msg='Template register operation failed: {} '.format(response.raw_message))
            logger.debug('Return code: {}, Status: {}, Message: {}'.format(response.code,response.message,response.message_description), True)
            outputs.append(response)

        RegisterTemplateContext.set('registered_templates', outputs)

    def runTest(self):
        self.test_register_templates()
