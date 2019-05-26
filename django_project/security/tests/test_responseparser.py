import security.responseparser as responseparser
from security.constants import SECURITY_ERRORS
from common.exceptions import TASException
import unittest


class TestResponseParser(unittest.TestCase):

    def test_parse_security_salt_script_response_succeeded(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_security_salt_script_response(self.mock_enable_security_succeeded)
        expected_output = {'status': True, 'comment': ''}
        self.assertEqual(actual_output, expected_output)

    def test_parse_security_salt_script_response_handle_null_response(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "SEC005_UNKNOWN_SALT_API_RESPONSE",
                           'err_message': SECURITY_ERRORS["SEC005_UNKNOWN_SALT_API_RESPONSE"],
                           'err_trace': {}}
        try:
            resp_instance.parse_security_salt_script_response({})
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_security_salt_script_response_handle_script_execution_failed(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "SEC006_SALT_CONFIGURATION_ISSUE",
                           'err_message': SECURITY_ERRORS["SEC006_SALT_CONFIGURATION_ISSUE"],
                           'err_trace': ["unable to execute script"]}
        try:
            resp_instance.parse_security_salt_script_response(self.mock_script_execution_failed)
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_security_salt_script_response_handle_unknown_response_format(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "SEC005_UNKNOWN_SALT_API_RESPONSE",
                           'err_message': SECURITY_ERRORS["SEC005_UNKNOWN_SALT_API_RESPONSE"],
                           'err_trace': self.mock_script_execution_response_unknown_format}
        try:
            resp_instance.parse_security_salt_script_response(self.mock_script_execution_response_unknown_format)
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_security_salt_script_response_handle_copy_script_file_failed_windows(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "SEC007_AGENT_DEPLOY_SCRIPT_COPY_FAILED",
                           'err_message': SECURITY_ERRORS["SEC007_AGENT_DEPLOY_SCRIPT_COPY_FAILED"],
                           'err_trace': 'File C:\\salt\\var\\agentDeploymentScript.ps1 transfer failed'}
        try:
            resp_instance.parse_security_salt_script_response(self.mock_windows_agentdeploymetscript_copy_failed)
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_security_salt_script_response_handle_download_agent_failed_windows(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "SEC002_TREND_MICRO_AGENT_DOWNLOAD_FAILURE",
                           'err_message': SECURITY_ERRORS["SEC002_TREND_MICRO_AGENT_DOWNLOAD_FAILURE"],
                           'err_trace': 'Downloading deep security agent failed'}
        try:
            resp_instance.parse_security_salt_script_response(self.mock_windows_agent_download_failed_response)
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_security_salt_script_response_handle_install_agent_failed(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE",
                           'err_message': SECURITY_ERRORS["SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE"],
                           'err_trace': '/tmp/tmplyHli1.sh: line 15: Download_Install_Agent: '
                                        'command not found /tmp/tmplyHli1.sh: line 27: '
                                        '/opt/ds_agent/dsa_control: No such file or directory'}
        try:
            resp_instance.parse_security_salt_script_response(self.mock_agent_install_Agent_fail_response)
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_security_salt_script_response_handle_activation_security_failed(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {'err_code': "SEC004_ENABLE_SECURITY_FAILED",
                           'err_message': SECURITY_ERRORS["SEC004_ENABLE_SECURITY_FAILED"],
                           'err_trace': '.dsm_ip, https://a0jdus042dsm001:4119, Downloading agent package ... '
                                        'curl https://A0JDUS042DSM001.vs-secops.cloud:4119/software/agent/'
                                        'RedHat_EL6/x86_64/ -o /tmp/agent.rpm --insecure --silent --tlsv1.2 '
                                        'Installing agent package ..., Preparing..., Host platform - '
                                        'Distributor ID: CentOS, ds_agent, Starting ds_agent: [  OK  ] '
                                        'HTTP Status: 200 - OK, Activation will be re-attempted 30 time(s) '
                                        'in case of failure, HTTP Status: 400 - OK, Response: '
                                        'Attempting to connect to https://a0jdus042dsm002:4120/, '
                                        'Error: activation was not successful. The manager may not be '
                                        'configured to allow agent-initiated activation, or the manager '
                                        'may not be configured to allow re-activation of existing hosts.'}
        try:
            resp_instance.parse_security_salt_script_response(self.mock_activation_Security_fail_response)
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_security_salt_script_response_handle_re_enable_security(self):
        resp_instance = responseparser.ResponseParser()
        err_msg = 'Security is already enabled, but DSM does not have entry of the VM.'\
                   ' Please contact your administrator.'
        try:
            actual_output = resp_instance.parse_security_salt_script_response(self.mock_re_enable_security_response)
        except TASException as e:
            self.assertEqual(e.err_code, 'SEC010_SECURITY_ENABLED')
            self.assertEqual(e.err_message, err_msg)
            self.assertEqual(e.err_trace,'')

    def test_parse_security_salt_script_response_handle_runtime_exception(self):
        resp_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            resp_instance.parse_security_salt_script_response(None)
            self.assertTrue('Unknown exception' in str(context.exception))

    def setUp(self):
        self.mock_enable_security_succeeded = \
            {'return': [
                     {'security_vm.xstest.local': {
                         'cmd_|-trend_latest_script_|-salt://trend/files/agentDeploymentScript.sh_|-script':
                             {'__run_num__': 0,
                              'comment': 'Command "salt://trend/files/agentDeploymentScript.sh" run',
                              'start_time': '04:46:22.937984',
                              'duration': 16689.437,
                              'name': 'salt://trend/files/agentDeploymentScript.sh',
                              'changes': {'pid': 25549, 'retcode': 0, 'stderr': '/tmp/tmpJM1PC1.sh: line 1: {%-: command not found',
                                          'stdout': '.dsm_ip, https://a0jdus042dsm001:4119, Downloading agent package ...'\
                                          'curl https://A0JDUS042DSM001.vs-secops.cloud:4119/software/agent/RedHat_EL6/x86_64/ -o /tmp/agent.rpm --insecure --silent --tlsv1.2'\
                                          'Installing agent package ..., Preparing..., Host platform - Distributor ID: CentOS, ds_agent, Starting ds_agent: [  OK  ]'\
                                          'HTTP Status: 200 - OK, Activation will be re-attempted 30 time(s) in case of failure, HTTP Status: 200 - OK,'},
                              'result': True,
                              }
                     }
                     }]}

        self.mock_script_execution_failed = \
            {'return': [
                {'security_vm.xstest.local': ["unable to execute script"]}
                ]}

        self.mock_script_execution_response_unknown_format = \
            {'return': [
                {'security_vm.xstest.local': {
                    'cmd_|-trend_latest_script_|-salt://trend/files/agentDeploymentScript.sh_|-script':
                        {'__run_num__': 0,
                         'comment': 'Command "salt://trend/files/agentDeploymentScript.sh" run',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': 'salt://trend/files/agentDeploymentScript.sh',
                         'result': True,
                         }
                }
                }]}

        self.mock_windows_agentdeploymetscript_copy_failed = \
            {'return': [
                {'security_vm.xstest.local':
                     {'file_|-trend_latest_copy_script_|-C:\\salt\\var\\agentDeploymentScript.ps1_|-managed':
                          {'__run_num__': 0, 'result': False, '__sls__': 'trend/latest',
                           'comment': 'File C:\\salt\\var\\agentDeploymentScript.ps1 transfer failed',
                           'name': 'C:\\salt\\var\\agentDeploymentScript.ps1', 'pchanges': {}, 'duration': 94.0,
                           'start_time': '23:55:32.864000', 'changes': {'diff': 'New file'},
                           '__id__': 'trend_latest_copy_script'},
                      }}]}
        self.mock_windows_agent_download_failed_response = \
            {'return': [
                     {'security_vm.xstest.local':
                         {'file_|-trend_latest_copy_script_|-C:\\salt\\var\\agentDeploymentScript.ps1_|-managed':
                               {'__run_num__': 0, 'result': True, '__sls__': 'trend/latest',
                                'comment': 'File C:\\salt\\var\\agentDeploymentScript.ps1 updated',
                                'name': 'C:\\salt\\var\\agentDeploymentScript.ps1', 'pchanges': {}, 'duration': 94.0,
                                'start_time': '23:55:32.864000', 'changes': {'diff': 'New file'},
                                '__id__': 'trend_latest_copy_script'},
                          'cmd_|-trend_latest_script_|-salt://trend/files/agentDeploymentScript.sh_|-script': {
                              '__run_num__': 1, 'result': False, '__sls__': 'trend/latest',
                              'comment': 'Command "C:\\salt\\var\\agentDeploymentScript.ps1" run',
                              'name': 'C:\\salt\\var\\agentDeploymentScript.ps1', 'start_time': '23:55:32.958000',
                              'changes': {
                                  'stderr': 'Downloading deep security agent failed',
                                  'stdout': 'Transcript started, output file is C:\\Users\\Administrator\\'
                                            'AppData\\Roaming\\Trend Micro\\Deep Security Agent\\installer\\'
                                            'dsa_deploy.log\r\n11:55:33 PM - DSA download started\r\n11:55:33 '
                                            'PM - Download Deep Security Agent Package\r\nhttps://100.64.103.'
                                            '17:4119/software/agent/Windows/i386/\r\nFailed to download the '
                                            'Deep Security Agent installation script. Please check if the '
                                            'package is imported into the Deep Security Manager.',
                                  'retcode': 1, 'pid': 2692},
                              'duration': 1752.0, '__id__': 'trend_latest_script_run'}}}]}

        self.mock_agent_install_Agent_fail_response = \
            {'return': [
                {'security_vm.xstest.local': {
                     'cmd_|-trend_latest_script_|-salt://trend/files/agentDeploymentScript.sh_|-script':
                         {'__run_num__': 0,
                          'comment': 'Command "salt://trend/files/agentDeploymentScript.sh" run',
                          'start_time': '04:46:22.937984',
                          'duration': 16689.437,
                          'name': 'salt://trend/files/agentDeploymentScript.sh',
                          'changes': {'pid': 25549, 'retcode': 0,
                                      'stderr': '',
                                      'stdout': '/tmp/tmplyHli1.sh: line 15: Download_Install_Agent: '
                                                'command not found /tmp/tmplyHli1.sh: line 27: '
                                                '/opt/ds_agent/dsa_control: No such file or directory'
                                      },
                          'result': True,
                          }
                 }}]}

        self.mock_activation_Security_fail_response = \
         {'return':
             [
                 {'security_vm.xstest.local': {
                     'cmd_|-trend_latest_script_|-salt://trend/files/agentDeploymentScript.sh_|-script':
                         {'__run_num__': 0,
                          'comment': 'Command "salt://trend/files/agentDeploymentScript.sh" run',
                          'start_time': '04:46:22.937984',
                          'duration': 16689.437,
                          'name': 'salt://trend/files/agentDeploymentScript.sh',
                          'changes': {'pid': 25549, 'retcode': 0,
                                      'stderr': '',
                                      'stdout': '.dsm_ip, https://a0jdus042dsm001:4119, Downloading agent package ... '
                                                'curl https://A0JDUS042DSM001.vs-secops.cloud:4119/software/agent/'
                                                'RedHat_EL6/x86_64/ -o /tmp/agent.rpm --insecure --silent --tlsv1.2 '
                                                'Installing agent package ..., Preparing..., Host platform - '
                                                'Distributor ID: CentOS, ds_agent, Starting ds_agent: [  OK  ] '
                                                'HTTP Status: 200 - OK, Activation will be re-attempted 30 time(s) '
                                                'in case of failure, HTTP Status: 400 - OK, Response: '
                                                'Attempting to connect to https://a0jdus042dsm002:4120/, '
                                                'Error: activation was not successful. The manager may not be '
                                                'configured to allow agent-initiated activation, or the manager '
                                                'may not be configured to allow re-activation of existing hosts.'},
                          'result': True,
                          }
                 }}]}

        self.mock_re_enable_security_response = \
            {'return':
             [
                 {'security_vm.xstest.local': {
                     'cmd_|-trend_latest_script_|-salt://trend/files/agentDeploymentScript.sh_|-script':
                         {'comment': 'unless execution succeeded',
                          'name': 'salt://trend/files/agentDeploymentScript.sh',
                          'start_time': '05:23:31.576262', 'skip_watch': True, '__id__': 'trend_latest_script',
                          'duration': 24.485,
                          '__run_num__': 0, 'changes': {}, 'result': True}
                 }}]}

