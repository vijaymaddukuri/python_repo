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

from robot.api import logger


class Context(object):
    __context_repo = {'is_login': False,
                      'created_workspace_names': [],
                      'to_create_workspace_names': [],
                      'data_set_names': [],
                      'global_ui_address': '',
                      'login_username': '',
                      'login_password': '',
                      'config_file_path': '',
                      'login_role': 'admin',
                      'search_tools_name': {},
                      'services_to_be_deployed': {},
                      'tools_to_be_deployed': {},
                      'search_data_sets': {},
                      'tool_to_be_published': '',
                      'data_set_to_be_published': '',
                      'data_set_to_be_deleted': '',
                      'working_set_to_be_deleted': '',
                      'current_browser': None,
                      'vSphere_info': {},
                      'pcf_info': {},
                      'deployed_data_sets_guid': [],
                      'deployed_apps_guid': [],
                      'local_path': '',
                      'remote_path':''}
    __base_variables_to_validate = []

    @staticmethod
    def validate(additional_variables=[]):
        merged_list = Context.__base_variables_to_validate+additional_variables
        Context._base_validate(merged_list)

    @staticmethod
    def load(global_config_file, extended_config_files):
        logger.info('loading configurations from file...', False, False)
        Context.set('global_config_file_path', global_config_file)
        Context.set('extended_config_files', extended_config_files)
        import yaml
        with open(global_config_file, 'r') as yaml_file:
                cfg = yaml.load(yaml_file)
                for key, value in cfg.items():
                    Context.set(key, value, True)
        for config_file in extended_config_files:
            with open(config_file, 'r') as yaml_file:
                cfg = yaml.load(yaml_file)
                for key, value in cfg.items():
                    Context.set(key, value, True)

    @staticmethod
    def get(key, is_global=False):
        value = Context.__context_repo.get(key, None)

        if not is_global:
            __workflow_context = Context.__context_repo.get('workflow_context', None)

            if __workflow_context:
                value = __workflow_context.get(key, None) or value

        return value

    @staticmethod
    def set(key, value, is_global=False):
        if is_global:
            Context.__context_repo[key] = value
        else:
            _workflow_context = Context.__context_repo.get('workflow_context', None)

            if _workflow_context:
                _workflow_context.update(**{key: value})
            else:
                _workflow_context = {key: value}

            Context.__context_repo['workflow_context'] = _workflow_context

    @staticmethod
    def print_out():
        logger.debug('Context: ', True)
        logger.info(Context.__context_repo, False, True)

    @staticmethod
    def _base_validate(variables):
        is_valid = False
        for item in variables:
            logger.debug('validating variable {0}...'.format(item), True)
            value = Context.get(item)
            if value is None or value == '':
                Context._print_error_msg_by_key(item)
                raise ValueError('context variable {} is None or empty!'.format(item))
            elif type(value) is list and len(value) == 0:
                Context._print_error_msg_by_key(item)
                raise ValueError('context variable {} is None or empty!'.format(item))
            elif type(value) is dict and len(value) == 0:
                Context._print_error_msg_by_key(item)
            elif type(value) is bool and value is False:
                Context._print_error_msg_by_key(item)
                raise ValueError('context variable {} is None or empty!'.format(item))


    @staticmethod
    def _print_error_msg_by_key(key):
        if key is None:
            logger.error('Key provided is not valid key!', False)
        elif key == 'is_login':
            logger.error('User is still not logined!', False)
        elif key == 'current_browser':
            logger.error('There is no active browser opened!', False)
        elif key == 'global_ui_address':
            logger.error('The global UI address is not valid!', False)
        elif key == 'login_username':
            logger.error('The username provided is not valid!', False)
        elif key == 'login_password':
            logger.error('The password provided is not valid!', False)
        elif key in ['services_to_be_deployed', 'tools_to_be_deployed']:
            logger.error('The services provided are not valid!', False)
        else:
            logger.error('The value is not correct!', False)
