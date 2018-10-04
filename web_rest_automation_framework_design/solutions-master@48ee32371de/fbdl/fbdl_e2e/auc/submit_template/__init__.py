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
from fbdl_e2e.auc.submit_template.submit_template_context import SubmitTemplateContext
from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.entity.dac_cli_response import DACCLIResponse
from fbdl_e2e.entity.dac_rest_query import DACRESTQuery
from robot.api import logger
from cliacore import CLIRunner
import requests
import time


class SubmitTemplate(BaseUseCase):
    """
    Data scientist submits template
    """

    def setUp(self):
        SubmitTemplateContext.validate()
        self._dac_cli_address = SubmitTemplateContext.get('dac_cli_address')
        self._dac_cli_username = SubmitTemplateContext.get('dac_cli_username')
        self._dac_cli_password = SubmitTemplateContext.get('dac_cli_password')
        self._ssh = CLIRunner(hostname=self._dac_cli_address, username=self._dac_cli_username,
                              password=self._dac_cli_password)
        self._registered_templates = SubmitTemplateContext.get('registered_templates')
        self._dac_service = SubmitTemplateContext.get('dac_service', True)

    def test_submit_templates(self):
        outputs = []
        for template_obj in self._registered_templates:
            if template_obj.code == '0':
                submit_template_cli = 'dac-cli submit -i {} -t '.format(template_obj.guid)
                response = DACCLIResponse(self._ssh.run_command(submit_template_cli))
                self.assertTrue(response.message=='Success', msg='Template submit operation failed: {} '.format(response.raw_message))
                logger.info('Return code: {}, Status: {}, Message: {}'.format(response.code,response.message, response.message_description), False, False)
                self.__wait_for_completion(template_obj)
                response.copy(template_obj)
                outputs.append(response)
            else:
                logger.error('template submit operation failed as no valid GUID...', False)
                continue

        SubmitTemplateContext.set('submitted_templates', outputs)

    def runTest(self):
        self.test_submit_templates()

    def __wait_for_completion(self, template_obj):
        import time
        time.sleep(5)



