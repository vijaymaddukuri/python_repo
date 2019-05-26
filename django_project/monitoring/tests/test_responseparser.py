import monitoring.responseparser as responseparser
from monitoring.constants import MONITORING_ERRORS
from common.exceptions import TASException
import unittest


class TestResponseParser(unittest.TestCase):

    def test_parse_salt_script_response_is_success_for_windows(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_salt_script_response(self.mock_enable_monitoring_succeeded_windows,
                                                                 kernel_type='windows')
        expected_output = {'status': True, 'err_code': '', 'comment': ''}
        self.assertEqual(actual_output, expected_output['status'])

    def test_parse_salt_script_response_is_success_for_linux(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_salt_script_response(self.mock_enable_monitoring_succeeded_linux,
                                                                 kernel_type='linux')
        expected_output = {'status': True, 'err_code': '', 'comment': ''}
        self.assertEqual(actual_output, expected_output['status'])

    def test_parse_salt_script_response_handle_null_response(self):
        response_instance = responseparser.ResponseParser()
        expected_output = {'err_code': 'MON008_UNKNOWN_SALT_API_RESPONSE',
                           'err_message': MONITORING_ERRORS['MON008_UNKNOWN_SALT_API_RESPONSE'],
                           'err_trace': {}}
        try:
            response_instance.parse_salt_script_response({}, kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_script_execution_failed(self):
        response_instance = responseparser.ResponseParser()

        expected_output = {'err_code': 'MON010_SALT_CONFIGURATION_ISSUE',
                           'err_message': 'unable to apply states on VM. '
                                          'check salt-master configurations.',
                           'err_trace': ["unable to execute script"]}
        try:
            response_instance.parse_salt_script_response(self.mock_script_execution_failed,
                                                         kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_download_agent_failed_windows(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'MON003_PKG_COPY_FAILED_ERROR',
            'err_message': MONITORING_ERRORS['MON003_PKG_COPY_FAILED_ERROR'],
            'err_trace': 'File C:\\nimsoft-robot-x64.exe updated failed'}
        try:
            resp_instance.parse_salt_script_response(self.mock_windows_agent_download_failed_response,
                                                     kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_download_agent_failed_linux(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'MON003_PKG_COPY_FAILED_ERROR',
            'err_message': MONITORING_ERRORS['MON003_PKG_COPY_FAILED_ERROR'],
            'err_trace': 'Source file salt://REPO/Nimsoft-install/nimldr/agent/nimldr-7.93.tar.Z not found'}
        try:
            resp_instance.parse_salt_script_response(self.mock_linux_agent_download_failed_response,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_install_agent_failed_windows(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'MON004_INSTALLATION_PROCESS_FAILED',
            'err_message': MONITORING_ERRORS['MON004_INSTALLATION_PROCESS_FAILED'],
            'err_trace': 'Command "salt://trend/files/agentDeploymentScript.sh" run'}
        try:
            resp_instance.parse_salt_script_response(self.mock_agent_install_Agent_fail_response_windows,
                                                     kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_install_agent_failed_linux(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': 'MON004_INSTALLATION_PROCESS_FAILED',
            'err_message': MONITORING_ERRORS['MON004_INSTALLATION_PROCESS_FAILED'],
            'err_trace': 'onlyif execution failed'}
        try:
            resp_instance.parse_salt_script_response(self.mock_agent_install_Agent_fail_response_linux,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_network_check_failed_linux(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': "MON005_HUB_CONNECTION_FAILED",
            'err_message': MONITORING_ERRORS["MON005_HUB_CONNECTION_FAILED"],
            'err_trace': 'Module function network.connect executed'
        }
        try:
            resp_instance.parse_salt_script_response(self.mock_agent_network_check_fail_response_linux,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_network_check_failed_windows(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': "MON005_HUB_CONNECTION_FAILED",
            'err_message': MONITORING_ERRORS["MON005_HUB_CONNECTION_FAILED"],
            'err_trace': 'Module function network.connect executed'
        }
        try:
            resp_instance.parse_salt_script_response(
                self.mock_agent_network_check_fail_response_windows,
                kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_probe_failed_windows(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': "MON011_PROBE_CONFIG_ERROR",
            'err_message': MONITORING_ERRORS["MON011_PROBE_CONFIG_ERROR"],
            'err_trace': 'Parent directory not present'}

        try:
            resp_instance.parse_salt_script_response(self.mock_probe_monitoring_fail_response_windows,
                                                     kernel_type='windows')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_probe_failed_linux(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': "MON011_PROBE_CONFIG_ERROR",
            'err_message': MONITORING_ERRORS["MON011_PROBE_CONFIG_ERROR"],
            'err_trace': 'Parent directory not present'}
        try:
            resp_instance.parse_salt_script_response(self.mock_probe_monitoring_fail_response_linux,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_service_start_failed_linux(self):
        resp_instance = responseparser.ResponseParser()
        expected_output = {
            'err_code': "MON007_SERVICE_START_ERROR",
            'err_message': MONITORING_ERRORS["MON007_SERVICE_START_ERROR"],
            'err_trace': 'The service nimbus is not running'}
        try:
            resp_instance.parse_salt_script_response(self.mock_service_start_monitoring_fail_response_linux,
                                                     kernel_type='linux')
        except TASException as e:
            self.assertEqual(e.err_code, expected_output['err_code'])
            self.assertEqual(e.err_message, expected_output['err_message'])
            self.assertEqual(e.err_trace, expected_output['err_trace'])

    def test_parse_salt_script_response_handle_service_start_success_linux(self):
        resp_instance = responseparser.ResponseParser()
        actual_output = resp_instance.parse_salt_script_response(self.mock_service_start_monitoring_succeeded_linux,
                                                                 kernel_type='linux')
        expected_output = {'status': True, 'err_code': '', 'comment': ''}
        self.assertEqual(actual_output, expected_output['status'])

    def test_parse_salt_script_response_handle_runtime_exception(self):
        resp_instance = responseparser.ResponseParser()
        with self.assertRaises(Exception) as context:
            resp_instance.parse_salt_script_response(None, kernel_type='linux')
            self.assertTrue('Unknown exception' in str(context.exception))

    def setUp(self):
        self.mock_enable_monitoring_succeeded_windows = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    'cmd_|-install_nim_robot_|-C:\\nimsoft-robot-x64.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART_|-run':
                        {'__sls__': 'nimsoft.nimldr.install',
                         '__run_num__': 2,
                         'comment': 'Command "C:\\nimsoft-robot-x64.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART" run',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': 'C:\\nimsoft-robot-x64.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART',
                         'changes': {'pid': 4868, 'retcode': 1,
                                     'stderr': "This version of C:\\nimsoft-robot-x64.exe is installed"},
                         'result': True,

                         }
                }
                }]}
        self.mock_enable_monitoring_succeeded_linux = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    "cmd_|-nimsoft_nimldr_install_2_|-/opt/nimldr/LINUX_23_64/nimldr -E -R ['10.100.249.95']'"
                    "'-I 10.100.249.110 -r -U administrator -S xStream2018! -f install_LINUX_23_64_|-run":
                        {'__run_num__': 4,
                         'comment': 'onlyif execution failed',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': "'opt/nimldr/LINUX_23_64/nimldr -E -R ['10.100.249.95']'"
                                 "' -I 10.100.249.110 -r -U administrator -S xStream2018! -f install_LINUX_23_64'",
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "", 'pid': 3156},
                         'result': True,
                         }
                }}]}

        self.mock_script_execution_failed = \
            {'return': [
                {'monitoring_vm.xstest.local': ["unable to execute script"]}
            ]}
        self.mock_service_start_monitoring_succeeded_linux = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    'service_|-nimbus_|-nimbus_|-running':
                        {'__run_num__': 6,
                         'comment': 'The service nimbus is already running',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': 'nimbus',
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "",
                                     'pid': 3156},
                         'result': True,
                         }
                }}]

            }

        self.mock_script_execution_response_unknown_format = \
            {'return': [
                {'monitoring_vm.xstest.local': {
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

        self.mock_windows_agent_download_failed_response = \
            {'return': [
                {'monitoring_vm.xstest.local':
                     {'file_|-nimsoft_nimldr_download_copy_|-C:\\nimsoft-robot-x64.exe_|-managed':
                          {'__run_num__': 0, 'result': False, '__sls__': 'nimsoft.nimldr.download',
                           'comment': 'File C:\\nimsoft-robot-x64.exe updated failed',
                           'name': 'C:\\nimsoft-robot-x64.exe', 'pchanges': {}, 'duration': 94.0,
                           'start_time': '23:55:32.864000', 'changes': {'diff': 'New file'},
                           '__id__': 'nimsoft_nimldr_download_copy'},
                      }}]}

        self.mock_linux_agent_download_failed_response = \
            {'return': [
                {'monitoring_vm.xstest.local':
                     {'file-managed':
                          {'__run_num__': 0, 'result': False, '__sls__': 'nimsoft.nimldr.download',
                           'comment': 'Source file salt://REPO/Nimsoft-install/nimldr/agent/nimldr-7.93.tar.Z not found',
                           'name': '/opt//nimldr/nimldr-7.93.tar.Z', 'pchanges': {}, 'duration': 94.0,
                           'start_time': '23:55:32.864000', 'changes': {'diff': 'New file'},
                           '__id__': 'nimsoft_nimldr_download_nimldr.tar'},
                      }}]}

        self.mock_agent_install_Agent_fail_response_windows = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    'cmd_|-install_nim_robot_|-C:\\nimsoft-robot-x64.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART_|-run':
                        {'__run_num__': 2,
                         'comment': 'Command "salt://trend/files/agentDeploymentScript.sh" run',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': 'C:\\nimsoft-robot-x64.exe /VERYSILENTUPPRESSMSGBOXES /NORESTART',
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "This version of C:\\nimsoft-robot-x64.exe is not compatible with the version of "
                                               "Windows you're running. Check your computer's system information and then"
                                               " contact the software publisher.", 'pid': 3156},
                         'result': False,
                         }
                }}]}
        self.mock_agent_install_Agent_fail_response_linux = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    "cmd_|-nimsoft_nimldr_install_2_|-/opt/nimldr/LINUX_23_64/nimldr -E -R ['10.100.249.95']'"
                    "'-I 10.100.249.110 -r -U administrator -S xStream2018! -f install_LINUX_23_64_|-run":
                        {'__run_num__': 4,
                         'comment': 'onlyif execution failed',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': "'opt/nimldr/LINUX_23_64/nimldr -E -R ['10.100.249.95']'"
                                 "' -I 10.100.249.110 -r -U administrator -S xStream2018! -f install_LINUX_23_64'",
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "", 'pid': 3156},
                         'result': False,
                         }
                }}]}
        self.mock_agent_network_check_fail_response_linux = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    'module_|-nimsoft_nimldr_install_check_port_|-network.connect_|-run':
                        {'__run_num__': 2,
                         'comment': 'Module function network.connect executed',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': 'network.connect',
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "Unable to connect to 10.100.249.110 (10.100.249.110) on tcp port 48000",
                                     'pid': 3156},
                         'result': False,
                         }
                }}]}
        self.mock_agent_network_check_fail_response_windows = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    'module_|-nimsoft_nimldr_install_check_port_|-network.connect_|-run':
                        {'__run_num__': 1,
                         'comment': 'Module function network.connect executed',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': 'network.connect',
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "Unable to connect to 10.100.249.110 (10.100.249.110) on tcp port 48000",
                                     'pid': 3156},
                         'result': False,
                         }
                }}]}
        self.mock_probe_monitoring_fail_response_windows = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    'file_|-C:\\Program Files\\Nimsoft\\request.cfg_|-C:\\Program Files\\Nimsoft\\request.cfg_|-managed':
                        {'__run_num__': 3,
                         'comment': 'Parent directory not present',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': 'C:\\Program Files\\Nimsoft\\request.cfg',
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "",
                                     'pid': 3156},
                         'result': False,
                         }
                }}]}

        self.mock_service_start_monitoring_fail_response_linux = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    'service_|-nimbus_|-nimbus_|-running':
                        {'__run_num__': 6,
                         'comment': 'The service nimbus is not running',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': 'nimbus',
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "",
                                     'pid': 3156},
                         'result': False,
                         }
                }}]}

        self.mock_probe_monitoring_fail_response_linux = \
            {'return': [
                {'monitoring_vm.xstest.local': {
                    'file_|-/opt/nimsoft/request.cfg_|-/opt/nimsoft/request.cfg_|-managed':
                        {'__run_num__': 5,
                         'comment': 'Parent directory not present',
                         'start_time': '04:46:22.937984',
                         'duration': 16689.437,
                         'name': '/opt/nimsoft/request.cfg',
                         'changes': {'retcode': 1,
                                     'stdout': '',
                                     'stderr': "",
                                     'pid': 3156},
                         'result': False,
                         }
                }}]}
