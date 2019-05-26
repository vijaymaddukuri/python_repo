from log_forwarder.splunkmanager import SplunkSaltManager
from mock import patch
import unittest
from common.exceptions import TASException

def mock_get_config(key, attribute):
    data_dict = { "splunk_client_details": {"INSTALLER_AGENT_SCRIPT_PATH": "splunk",
                                            "SPLUNK_FORWARDER_ADMIN_PASSWORD": "test"
                                            },
                 "splunk_server_details": {"SPLUNK_DEPLOYMENT_SERVER_IP": "1.2.3.4",
                                            "SPLUNK_DEPLOYMENT_SERVER_PORT": "8089"
                                            },
                 "salt_retries_config_values": {"SALT_JOB_RUNNING_RETRIES": 1, "SALT_JOB_RETRIES_TIMEOUT": 1,
                                                "SALT_PING_NO_OF_RETRIES": 1, "SALT_PING_RETRIES_TIMEOUT": 1}
                 }

    return data_dict[key][attribute]

class TestSplunkManager(unittest.TestCase):

    @patch('log_forwarder.splunkmanager.get_config')
    @patch('log_forwarder.splunkmanager.SaltNetAPI')
    def test_install_splunk_forwarder_positive(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        instance.execute_command.return_value = self.mock_agent_positive_response
        instance.get_minion_name_from_ip.return_value = {'status': True, 'minion_name': 'dummy'}
        instance.get_os_kernel_from_minion_id.return_value = 'linux'
        instance.check_minion_status.return_value = True
        splunk_api = SplunkSaltManager()

        actual_output = splunk_api.install_splunk_forwarder(vm_ip="0.0.0.0")
        expected_output = {'status': True, 'comment': ''}
        self.assertTrue(actual_output, expected_output)

    @patch('log_forwarder.splunkmanager.get_config')
    @patch('log_forwarder.splunkmanager.SaltNetAPI')
    def test_install_splunk_forwarder_minion_status_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        splunk_api = SplunkSaltManager()

        instance.get_os_kernel_from_minion_id.return_value = 'linux'
        instance.check_minion_status.return_value = False
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_0
        try:
            actual_output = splunk_api.install_splunk_forwarder(vm_ip="0.0.0.0")
        except TASException as e:
            self.assertEqual(e.err_code, "LOG_FWRDR012_CHECK_VM_STATUS")

    @patch('log_forwarder.splunkmanager.get_config')
    @patch('log_forwarder.splunkmanager.SaltNetAPI')
    def test_install_splunk_forwarder_installation_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        splunk_api = SplunkSaltManager()

        instance.get_vm_minion_status.return_value = {'status': True}
        instance.get_minion_name_from_ip.return_value = {'status': True, 'minion_name': 'dummy'}
        instance.get_os_kernel_from_minion_id.return_value = 'linux'
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_0
        try:
            actual_output = splunk_api.install_splunk_forwarder(vm_ip="0.0.0.0")
        except Exception as e:
            self.assertEqual(e.err_code, 'LOG_FWRDR003_INSTALL_FAILED')

    @patch('log_forwarder.splunkmanager.get_config')
    @patch('log_forwarder.splunkmanager.SaltNetAPI')
    def test_install_splunk_forwarder_status_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        splunk_api = SplunkSaltManager()

        instance.get_vm_minion_status.return_value = {'status': True}
        instance.get_minion_name_from_ip.return_value = {'status': True, 'minion_name': 'dummy'}
        instance.get_os_kernel_from_minion_id.return_value = 'linux'
        instance.execute_command.return_value = self.mock_agent_negative_response_status_false
        try:
            actual_output = splunk_api.install_splunk_forwarder(vm_ip="0.0.0.0")
        except TASException as e:
            self.assertEqual(e.err_code, 'LOG_FWRDR000_SALT_SERVER_ERROR')

    @patch('log_forwarder.splunkmanager.get_config')
    @patch('log_forwarder.splunkmanager.SaltNetAPI')
    def test_install_splunk_forwarder_empty_response(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        splunk_api = SplunkSaltManager()

        instance.get_vm_minion_status.return_value = {'status': True}
        instance.get_minion_name_from_ip.return_value = {'status': True, 'minion_name': 'dummy'}
        instance.get_os_kernel_from_minion_id.return_value = 'linux'
        instance.execute_command.return_value = ''
        try:
            actual_output = splunk_api.install_splunk_forwarder(vm_ip="0.0.0.0")
        except TASException as e:
            self.assertEqual(e.err_code, 'LOG_FWRDR009_UNABLE_INSTALL')

    @patch('log_forwarder.splunkmanager.get_config')
    @patch('log_forwarder.splunkmanager.SaltNetAPI')
    def test_install_splunk_forwarder_status_not_found(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        splunk_api = SplunkSaltManager()

        instance.get_vm_minion_status.return_value = {'status': True}
        instance.get_minion_name_from_ip.return_value = {'status': True, 'minion_name': 'dummy'}
        instance.get_os_kernel_from_minion_id.return_value = 'linux'
        instance.execute_command.return_value = {'dummy_response': ''}
        try:
            actual_output = splunk_api.install_splunk_forwarder(vm_ip="0.0.0.0")
        except TASException as e:
            self.assertEqual(e.err_code, "LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE")

    @patch('log_forwarder.splunkmanager.get_config')
    @patch('log_forwarder.splunkmanager.SaltNetAPI')
    def test_install_splunk_forwarder_kernel_not_found(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        splunk_api = SplunkSaltManager()

        instance.get_vm_minion_status.return_value = {'status': True}
        instance.get_minion_name_from_ip.return_value = {'status': True, 'minion_name': 'dummy'}
        instance.get_os_kernel_from_minion_id.return_value = 'linux'
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_0
        try:
            actual_output = splunk_api.install_splunk_forwarder(vm_ip="0.0.0.0")
        except TASException as e:
            self.assertEqual(e.err_code, "LOG_FWRDR011_UNABLE_TO_FETCH_KERNEL_TYPE")

    def setUp(self):
        self.mock_agent_positive_response = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "start_time": "01:49:03.522591",
                              "result": True,
                              "duration": 28.615,
                              "__run_num__": 0,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "splunkuf_install_splunkuf"
                            },
                            "cmd_|-splunkuf_change_owner_before_firsttime_start|": {
                                  "comment": "Command '/bin/chown -R splunk.splunk /opt/splunkforwarder/bin/splunk'",
                                  "pchanges": {

                                  },
                                  "name": "splunkuf_change_owner_before_firsttime_start",
                                  "start_time": "01:49:03.551511",
                                  "result": True,
                                  "duration": 66.254,
                                  "__run_num__": 1,
                                  "changes": {
                                    "diff": "New file",
                                    "mode": "0644"
                                  },
                                  "__id__": "splunkuf_change_owner_before_firsttime_start"
                              },
                            'cmd_|-splunkuf_install_firsttime_start|-splunk start_|-run':
                                {'__run_num__': 2,
                                 'comment': 'Command "splunk start --accept-license --answer-yes --no-prompt --seed-passwd xStreamsplunk!" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': 'splunkuf_install_firsttime_start',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': '',
                                 '__id__': 'splunkuf_install_firsttime_start', 'result': True},

                            'cmd_|-splunkuf_deployserver_set|-splunkuf_deployserver_set_|-run':
                                {'__run_num__': 3,
                                 'comment': 'Command "splunk set deploy-poll" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': 'splunkuf_deployserver_set',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': '',
                                 '__id__': 'splunkuf_deployserver_set', 'result': True},
                            'cmd_|-splunkuf_change_owner_after_register|-splunk start_|-run':
                                {'__run_num__': 4,
                                 'comment': 'Command "chown -R splunk.splunk /splunk " run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': 'splunkuf_change_owner_after_register',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': '',
                                 '__id__': 'splunkuf_change_owner_after_register', 'result': True},
                            "cmd_|-splunkuf_restart_cmdrun|-rpm -Uvh /opt/nimsoft-robot.x86_64.rpm_|-run": {
                              "comment": "Command '/opt/splunkforwarder/bin/splunk restart' run",
                              "name": "splunkuf_restart_cmdrun",
                              "start_time": "01:49:03.618593",
                              "result": True,
                              "duration": 1090.287,
                              "__run_num__": 5,
                              "changes": {
                                "pid": 5191,
                                "retcode": 0,
                                "stderr": "",
                                "stdout": ""
                              },
                              "__id__": "splunkuf_restart_cmdrun"}}}]}}

        self.mock_agent_negative_response_false_status= \
            {'status': False,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "start_time": "01:49:03.522591",
                              "result": True,
                              "duration": 28.615,
                              "__run_num__": 0,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}}

        self.mock_agent_negative_response_run_num_0 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "start_time": "01:49:03.522591",
                              "result": True,
                              "duration": 28.615,
                              "__run_num__": 0,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}}

        self.mock_agent_negative_response_status_false = \
            {'status': False,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/splunkforwarder|-/opt/splunkforwarder|-managed": {
                              "comment": "File -/opt/splunkforwarder updated",
                              "pchanges": {

                              },
                              "name": "splunkuf_install_splunkuf",
                              "start_time": "01:49:03.522591",
                              "result": True,
                              "duration": 28.615,
                              "__run_num__": 0,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "splunkuf_install_splunkuf"
                            }}}]}}


if __name__ == '__main__':
    unittest.main()
