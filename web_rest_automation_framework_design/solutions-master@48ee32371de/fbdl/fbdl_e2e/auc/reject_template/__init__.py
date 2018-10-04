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
from fbdl_e2e.auc.reject_template.reject_template_context import RejectTemplateContext
from fbdl_e2e.auc.baseusecase import BaseUseCase
from fbdl_e2e.entity.dac_cli_response import DACCLIResponse
from fbdl_e2e.entity.dac_rest_query import DACRESTQuery
from robot.api import logger
from cliacore import CLIRunner


class RejectTemplate(BaseUseCase):
    """
    Data scientist rejects template
    """

    def setUp(self):
        RejectTemplateContext.validate()
        self._dac_cli_address = RejectTemplateContext.get('dac_cli_address')
        self._dac_cli_username = RejectTemplateContext.get('dac_cli_username')
        self._dac_cli_password = RejectTemplateContext.get('dac_cli_password')
        self._ssh = CLIRunner(hostname=self._dac_cli_address, username=self._dac_cli_username,
                              password=self._dac_cli_password)
        self._submitted_templates = RejectTemplateContext.get('submitted_templates')
        self._dac_service = RejectTemplateContext.get('dac_service')

    def test_reject_templates(self):
        outputs = []
        for template_obj in self._submitted_templates:
            if template_obj.code == '0':
                new_guid = self.__get_template_guid(template_obj)
                submit_asset_cli = 'dac-cli reject -i {} -t -m \'gse automation\''.format(new_guid)
                response = DACCLIResponse(self._ssh.run_command(submit_asset_cli))
                self.assertTrue(response.message=='Success', msg='Template reject operation failed:{}'.format(response.raw_message))
                response.guid = new_guid
                response.workspace = template_obj.workspace
                logger.info('Return code: {}, Status: {}, Message: {}'.format(response.code,response.message, response.message_description), False, False)
                outputs.append(response)
            else:
                logger.error('Template reject operation failed as no valid GUID...', False)
                continue
        RejectTemplateContext.set('rejected_templates', outputs)

    def runTest(self):
        self.test_reject_templates()

    def __get_template_guid(self, template_obj):
        filter = template_obj.guid if template_obj.guid!='' else template_obj.name
        list_template_cli = 'dac-cli list -c {} -a -e pendingPublication | grep {}'.format(template_obj.category, filter)
        logger.debug(list_template_cli, True)
        import time
        time.sleep(5)
        cli_response = self._ssh.run_command(list_template_cli)
        logger.debug('Search the pending publication template by original GUID...', True)
        logger.debug(cli_response, True)
        fields = cli_response.split('|')
        if len(fields) < 33:
            logger.error('Publication GUID was not found!', False)
            raise AssertionError('Publication GUID was not found! ')
        else:
            return fields[20].strip()

    def __is_template_rejected(self, template_obj):
        filter = template_obj.guid if template_obj.guid!='' else template_obj.name
        list_published_template_cli = 'dac-cli list -c {} -a | grep \'{}\''.format(template_obj.category, filter)
        logger.debug(list_published_template_cli, True)
        cli_response = self._ssh.run_command(list_published_template_cli)
        logger.debug('Search the published template by original GUID...', True)
        logger.debug(cli_response, True)
        if cli_response is not None and cli_response!='':
            logger.info('Template {} is still found!'.format(template_obj.name))
            return False
        else:
            return True

    def __wait_for_completion(self, template_obj):
        query = DACRESTQuery('http://{}/dac/rest/1.0/asset/process/status''?workspaceId={}&assetGUID={}'\
            .format(self._dac_service,template_obj.workspace, template_obj.guid))
        # No REST call will be developed for template status query