import monitoring.nimsoftmanager as nimsoftmanager
from mock import patch
import unittest
from common.exceptions import TASException 


def mock_get_config(key, attribute):
    data_dict = {"nimsoft_client_details": {"INSTALLER_AGENT_SCRIPT_PATH": "nimsoft",
                                            "UNINSTALLER_AGENT_SCRIPT_PATH":"nimsoft/nimldr/uninstall",
                                            "CLEANUP_SCRIPT_PATH":"nimsoft/nimldr/cleanup"},
                 "nimsoft_server_details": {"NIMSOFT_HUB_IP": "1.2.3.4",
                                            "NIMSOFT_HUB_NAME": "win-test-hub",
                                            "NIMSOFT_DOMAIN": "domain",
                                            "NIMSOFT_HUB_ROBOT_NAME": "win",
                                            "NIMSOFT_HUB_USERNAME": "username",
                                            "NIMSOFT_HUB_PASSWORD": "passwd"

                                            },
                 "salt_retries_config_values": {"SALT_JOB_RUNNING_RETRIES": 1, "SALT_JOB_RETRIES_TIMEOUT": 1,
                                                "SALT_PING_NO_OF_RETRIES": 1, "SALT_PING_RETRIES_TIMEOUT": 1}
                 }

    return data_dict[key][attribute]

class TestNimsoftManager(unittest.TestCase):

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_install_nimsoft_agent_positive(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        instance.execute_command.return_value = self.mock_agent_positive_response
        nimsoftapi = nimsoftmanager.NimsoftAPI()

        actual_output = nimsoftapi.install_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
        expected_output = {'status': True, 'comment': ''}
        self.assertTrue(actual_output, expected_output)

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_install_monitoring_extract_tar_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_1
        try:
          actual_output = nimsoftapi.install_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON002_EXTRACT_TAR_FAILED"}
        except TASException as e:
        	#self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON002_EXTRACT_TAR_FAILED')

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_install_monitoring_package_copy_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_0
        try:
          actual_output = nimsoftapi.install_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON003_PKG_COPY_FAILED_ERROR"}
        except TASException as e:
                #self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON003_PKG_COPY_FAILED_ERROR')

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_install_monitoring_hub_connection_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_2
        try:
          actual_output = nimsoftapi.install_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON005_HUB_CONNECTION_FAILED"}
        except TASException as e:
                #self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON005_HUB_CONNECTION_FAILED')
   
    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_install_monitoring_set_permission_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_3
        try:
          actual_output = nimsoftapi.install_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON006_SET_PERMISSION_FAILED"}
        except TASException as e:
                #self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON006_SET_PERMISSION_FAILED')

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_install_monitoring_installation_process_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_4
        try:
          actual_output = nimsoftapi.install_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON004_INSTALLATION_PROCESS_FAILED"}
        except TASException as e:
                #self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON004_INSTALLATION_PROCESS_FAILED')
 
    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_install_monitoring_probe_configuration_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_5
        try:
          actual_output = nimsoftapi.install_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON011_PROBE_CONFIG_ERROR"}
        except TASException as e:
                #self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON011_PROBE_CONFIG_ERROR')

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_install_monitoring_service_start_error(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_6
        try:
          actual_output = nimsoftapi.install_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON007_SERVICE_START_ERROR"}
        except TASException as e:
                #self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON007_SERVICE_START_ERROR')


    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')
    def test_uninstall_monitoring_unable_to_stop_service(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_1
        try:
          actual_output = nimsoftapi.uninstall_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON0016_SERVICE_STOP_ERROR",
                           'status': False, 'comment':
                           'Process to install monitoring agent '
                           'package on the VM failed due to :'
                           'All specified packages installation failed'}
        except TASException as e:
                #self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON0016_SERVICE_STOP_ERROR')

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.nimsoftmanager.SaltNetAPI')

    def test_uninstall_monitoring_unable_to_uninstall(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        nimsoftapi = nimsoftmanager.NimsoftAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_0
        try:
          actual_output = nimsoftapi.uninstall_nimsoft_agent(vm_hostname="dummy", vm_ip="0.0.0.0")
          expected_output = { 'err_code': "MON0015_UNINSTALLATION_PROCESS_FAILED",
                           'status': False, 'comment':
                           'Process to install monitoring agent '
                           'package on the VM failed due to :'
                           'All specified packages installation failed'}
        except TASException as e:
                #self.assertTrue(actual_output, expected_output)
          self.assertEquals(e.err_code, 'MON0015_UNINSTALLATION_PROCESS_FAILED')


    def setUp(self):
        self.mock_agent_positive_response = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                                
                              },
                              "name": "/opt/nms-robot-vars.cfg",
                              "start_time": "01:49:03.522591",
                              "result": True,
                              "duration": 28.615,
                              "__run_num__": 0,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            },
                            "file_|-/opt/nimsoft-robot.x86_64.rpm_|-/opt/nimsoft-robot.x86_64.rpm_|-managed": {
                                  "comment": "File /opt/nimsoft-robot.x86_64.rpm updated",
                                  "pchanges": {
                                    
                                  },
                                  "name": "/opt/nimsoft-robot.x86_64.rpm",
                                  "start_time": "01:49:03.551511",
                                  "result": True,
                                  "duration": 66.254,
                                  "__run_num__": 1,
                                  "changes": {
                                    "diff": "New file",
                                    "mode": "0644"
                                  },
                                  "__id__": "/opt/nimsoft-robot.x86_64.rpm"
                              },
                            'cmd_|-start_monitoring|-/etc/init.d/monitoring start1_|-run':
                                {'__run_num__': 2,
                                 'comment': 'Command "/etc/init.d/monitoring start" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': '/etc/init.d/monitoring start',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': 'monitoring/unix_client',
                                 '__id__': 'start_monitoring', 'result': True},
                            "cmd_|-install_nim_robot_|-rpm -Uvh /opt/nimsoft-robot.x86_64.rpm_|-run": {
                              "comment": "Command \"rpm -Uvh /opt/nimsoft-robot.x86_64.rpm\" run",
                              "name": "rpm -Uvh /opt/nimsoft-robot.x86_64.rpm",
                              "start_time": "01:49:03.618593",
                              "result": True,
                              "duration": 1090.287,
                              "__run_num__": 2,
                              "changes": {
                                "pid": 5191,
                                "retcode": 0,
                                "stderr": "\nNote: This output shows SysV services only and does not include native\nsystemd services. SysV configuration data might be overridden by native\nsystemd configuration.\n\nIf you want to list systemd services use 'systVIJAYtl list-unit-files'.\nTo see services enabled on particular target use\n'systVIJAYtl list-dependencies [target]'.",
                                "stdout": "Preparing...                          ########################################\nUpdating / installing...\nnimsoft-robot-7.80-1                  ########################################\nnimbus                    0:off  1:off  2:off  3:on   4:on   5:on   6:off"
                              },
                              "__id__": "install_nim_robot"}}}]}}

        self.mock_agent_negative_response_run_num_2 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "name": "/opt/nms-robot-vars.cfg",
                              "start_time": "01:49:03.522591",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 2,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_agent_negative_response_run_num_3 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "result": False,
                              "__run_num__": 3,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_agent_negative_response_run_num_4 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "result": False,
                              "__run_num__": 4,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_agent_negative_response_run_num_5 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "result": False,
                              "__run_num__": 5,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "name": "test",
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_agent_negative_response_run_num_6 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "result": False,
                              "__run_num__": 6,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_agent_negative_response_run_num_0 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "name": "/opt/nms-robot-vars.cfg",
                              "start_time": "01:49:03.522591",
                              "result": False,
                              "duration": 28.615,
                              "__run_num__": 0,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_agent_negative_response_run_num_1 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "result": False,
                              "__run_num__": 1,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_agent_negative_response_status_false = \
            {'status': False,
             'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "result": False,
                              "__run_num__": 1,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_agent_negative_response_no_status = \
            {'comment':
                {'return':
                    [
                        {'test.local': {
                            "file_|-/opt/nms-robot-vars.cfg_|-/opt/nms-robot-vars.cfg_|-managed": {
                              "comment": "File /opt/nms-robot-vars.cfg updated",
                              "pchanges": {
                              },
                              "result": False,
                              "__run_num__": 1,
                              "changes": {
                                "diff": "New file",
                                "mode": "0644"
                              },
                              "__id__": "/opt/nms-robot-vars.cfg"
                            }}}]}}

        self.mock_monitoring_positive_response = \
            [
                {'step': 1, 'description': 'Create the client',
                 'error': {}, 'result': 'Client created with Resource ID '
                  '83.0.243'
                },
                {'step': 2, 'description': 'Add the client to the Protection Group', 'error': {},
                 'result': 'Client added to the protection group.'
                 ' The response is <Response [204]>'
                }
            ]

        self.mock_monitoring_negative_response = \
            [
                {'step': 1, 'description': 'Create the client',
                 'error': {}, 'result': 'Client created with Resource ID '
                  '83.0.243'
                },
                {"step": 2,
                 "description": "Add the client to the Protection Group",
                 "result": "An error occurred",
                 "error": {"error_message": "error occured while adding client to protection group",
                           "error_code": 500}
                }
            ]

        self.mock_disable_monitoring_positive_response = \
            [
                {"step": 1,
                 "description": "Fetch resource ID",
                 "result": "Client found",
                 "error": {}
                },
                {"step": 2,
                 "description": "Delete Client",
                 "result": "Client successfully Deleted. ",
                 "error": {}
                 }
             ]

        self.mock_uninstall_nimsoft_agent_positive_response_run_num_1 = \
            {
                'status': False,
                'comment': {
                    'return': [
                        {'test.local':
                            {
                                'cmd_|-nimsoft/nimldr/uninstall_|-/opt/nimsoft/bin/inst_init.sh remove_|-run': {
                                    'comment': 'Command "/opt/nimsoft/bin/inst_init.sh remove" run',
                                    'name': '/opt/nimsoft/bin/inst_init.sh remove',
                                    'start_time': '06:43:27.858759',
                                    'result': True,
                                    'duration': 5099.457,
                                    '__run_num__': 1,
                                    '__sls__': 'nimsoft/nimldr/uninstall'},
                                    'changes': {
                                        'pid': 26123,
                                        'retcode': 0,
                                        'stderr': '/opt/nimsoft/bin/inst_init.sh: line 376: [-e: command not found',
                                        'stdout': 'Stopping NimBUS...'
                                    },
                                    '__id__': 'nimsoftnimldruninstall'
                                }
                            }
                        ]
                }
            }

        self.mock_uninstall_nimsoft_agent_positive_response_run_num_0 = \
            {
                'status': True,
                'comment': {
                    'return': [
                        {'test.local':
                            {
                                'service_|-nimbus_|-nimbus_|-dead': {
                                    'comment': 'Service nimbus was killed',
                                    'name': 'nimbus',
                                    'start_time': '06:43:12.695799',
                                    'result': True,
                                    'duration': 15161.118,
                                    '__run_num__': 0,
                                    '__sls__': 'nimsoft.stop',
                                    'changes': {
                                        'nimbus': False
                                    },
                                    '__id__': 'nimbus'
                                }
                            }
                        }
                    ]
                }
            }
        self.mock_uninstall_nimsoft_agent_negative_response_run_num_0 = \
            {
                'status': False,
                'comment': {
                    'return': [
                        {'test.local':
                            {
                                'service_|-nimbus_|-nimbus_|-dead': {
                                    'comment': 'Unable to killService nimbus ',
                                    'name': 'nimbus',
                                    'start_time': '06:43:12.695799',
                                    'result': True,
                                    'duration': 15161.118,
                                    '__run_num__': 0,
                                    '__sls__': 'nimsoft.stop',
                                    'changes': {
                                        'nimbus': False
                                    },
                                    '__id__': 'nimbus'
                                }
                            }
                        }
                    ]
                }
            }
        self.mock_uninstall_nimsoft_agent_negative_response_run_num_1 = \
            {
                'status': False,
                'comment': {
                    'return': [
                        {'test.local':
                            {
                                'cmd_|-nimsoft/nimldr/uninstall_|-/opt/nimsoft/bin/inst_init.sh remove_|-run': {
                                    'comment': 'Command "/opt/nimsoft/bin/inst_init.sh remove" run',
                                    'name': '/opt/nimsoft/bin/inst_init.sh remove',
                                    'start_time': '06:43:27.858759',
                                    'result': True,
                                    'duration': 5099.457,
                                    '__run_num__': 1,
                                    '__sls__': 'nimsoft/nimldr/uninstall'},
                                    'changes': {
                                        'pid': 26123,
                                        'retcode': 0,
                                        'stderr': '/opt/nimsoft/bin/inst_init.sh: line 376: [-e: command not found',
                                        'stdout': 'Unable to Stop NimBUS...'
                                    },
                                    '__id__': 'nimsoftnimldruninstall'
                                }
                            }
                        ]
                }
            }



if __name__ == '__main__':
    unittest.main()
