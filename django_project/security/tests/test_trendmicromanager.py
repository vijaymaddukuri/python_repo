import security.trendmicromanager as trendmicromanager
from security.constants import SECURITY_ERRORS
from mock import patch, MagicMock
import unittest
from common.exceptions import APIException

def mock_raise_exception():
    raise Exception("Dummy exception!!")

def mock_raise_api_exception(*args, **kwarg):
    err_msg = 'Error_test'
    exception_trace = 'Trace'
    raise APIException(err_msg, exception_trace)


def mock_get_config(key, attribute):
    data_dict = {"trendmicro_client_details": {"INSTALLER_AGENT_SCRIPT_PATH": "trend/enable_security"},
                 "trendmicro_server_details": {"DSM_IP": "1.1.1.1",
                                               "DSM_TENANT_ID": "D8E97581-AAEC-3635-63F3-4C611E4E53FB",
                                               "DSM_TENANT_PWD": "8B490C84-DB66-EDED-EE0D-CCFF486EE628",
                                               "DSM_PORT": "4119",
                                               "DSM_API_SECRET_KEY": "THIS-IS-NOTREAL-SECRET-KEY"
                                               },
                 "salt_retries_config_values": {"SALT_JOB_RUNNING_RETRIES": 1, "SALT_JOB_RETRIES_TIMEOUT": 1,
                                                "SALT_PING_NO_OF_RETRIES": 1, "SALT_PING_RETRIES_TIMEOUT": 1}
                 }
    return data_dict[key][attribute]


class TestTrendMicroManager(unittest.TestCase):

    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_check_minion_status_success(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        trendmicroapi = trendmicromanager.TrendMicroAPI()
        instance.get_vm_minion_status.return_value = {'status': True}
        result = trendmicroapi.check_minion_status("1.1.1.1")
        self.assertTrue(result, True)

    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_check_minion_status_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        trendmicroapi = trendmicromanager.TrendMicroAPI()
        instance.get_vm_minion_status.return_value = {'status': False}
        result = trendmicroapi.check_minion_status("1.1.1.1")
        self.assertFalse(result, False)

    @patch('security.trendmicromanager.SaltNetAPI')
    def test_get_fqdn_from_vm_ip_success(self, mock_salt_api ):
        instance = mock_salt_api.return_value
        trendmicroapi = trendmicromanager.TrendMicroAPI()
        instance.get_minion_name.return_value = {'status': True, 'minion_name': 'test'}
        instance.get_fqdn_from_minion_id.return_value = {'status': True, 'fqdn': 'test.xd'}
        result = trendmicroapi.get_fqdn_from_vm_ip("1.1.1.1")
        self.assertTrue( 'fqdn' in result )

    @patch('security.trendmicromanager.SaltNetAPI')
    def test_get_fqdn_from_vm_ip_fail(self, mock_salt_api ):
        instance = mock_salt_api.return_value
        trendmicroapi = trendmicromanager.TrendMicroAPI()
        instance.get_minion_name.return_value = {'status': False, 'comment': 'Minion not found'}
        instance.get_fqdn_from_minion_id.return_value = {'status': True, 'fqdn': 'test.xd'}
        result = trendmicroapi.get_fqdn_from_vm_ip("1.1.1.1")
        self.assertFalse( result['status'])

    @patch('security.trendmicromanager.TrendMicroAPI.get_fqdn_from_vm_ip')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.RestClient')
    def test_get_dsm_response(self, mock_rest, mock_config, mock_fqdn):
        mock_config.side_effect = mock_get_config
        mock_fqdn.return_value = {'status': True, 'fqdn': 'test.xd'}
        mock_rest.get_https_url.return_value = 'https://example.com/some/path'

        output = {'computers':[{'hostName': 'test.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        mock_rest.post_JSON.return_value = response_instance

        trendmicroapi = trendmicromanager.TrendMicroAPI()
        actual_output = trendmicroapi.get_dsm_response(vm_ip="1.1.1.1")
        self.assertEqual(actual_output[0], "test.xd")
        self.assertEqual(actual_output[1].status_code, 200)

    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.RestClient')
    def test_delete_computer_positive_1(self, rest_mock, mock_config):
        trendmicroapi = trendmicromanager.TrendMicroAPI()
        mock_config.side_effect = mock_get_config

        response_instance = MagicMock()
        response_instance.status_code = 204
        rest_mock.make_delete_request.return_value = response_instance
        actual_output = trendmicroapi.delete_computer("2")
        self.assertEqual(actual_output.status_code, 204)

    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.RestClient')
    def test_delete_computer_positive_2(self, rest_mock, mock_config):
        trendmicroapi = trendmicromanager.TrendMicroAPI()
        mock_config.side_effect = mock_get_config

        response_instance = MagicMock()
        response_instance.status_code = 500
        rest_mock.make_delete_request.return_value = response_instance
        actual_output = trendmicroapi.delete_computer("2")
        self.assertNotEqual(actual_output.status_code, 204)



    @patch('security.trendmicromanager.TrendMicroAPI.get_dsm_response')
    def test_is_security_enabled_for_vm_positive_true(self, dsm_resp_mock):
        trendmicroapi = trendmicromanager.TrendMicroAPI()

        output = {'computers':[{'hostName': 'test.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        dsm_resp_mock.return_value = ('test.xd', response_instance)

        actual_output = trendmicroapi.is_security_enabled_for_vm(vm_ip="1.1.1.1")
        self.assertTrue(actual_output)

    @patch('security.trendmicromanager.TrendMicroAPI.get_dsm_response')
    def test_is_security_enabled_for_vm_positive_false_1(self, dsm_resp_mock):
        trendmicroapi = trendmicromanager.TrendMicroAPI()
        # when req hostname and resp hostname is not same.
        output = {'computers':[{'hostName': 'test123.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        dsm_resp_mock.return_value = ('test.xd', response_instance)

        actual_output = trendmicroapi.is_security_enabled_for_vm(vm_ip="1.1.1.1")
        self.assertFalse(actual_output)

    @patch('security.trendmicromanager.TrendMicroAPI.get_dsm_response')
    def test_is_security_enabled_for_vm_positive_false_2(self, dsm_resp_mock):
        trendmicroapi = trendmicromanager.TrendMicroAPI()

        # When req hostname not found.
        output = {'computers':[]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        dsm_resp_mock.return_value = ('test.xd', response_instance)

        actual_output = trendmicroapi.is_security_enabled_for_vm(vm_ip="1.1.1.1")
        self.assertFalse(actual_output)

    @patch('security.trendmicromanager.TrendMicroAPI.get_fqdn_from_vm_ip')
    @patch('security.trendmicromanager.get_config')
    def test_is_security_enabled_for_vm_negative(self, mock_config, mock_fqdn):
        mock_config.side_effect = mock_get_config
        
        # When salt connection is not established.
        mock_fqdn.return_value = {'status': False, 'comment': 'not found'}
        trendmicroapi = trendmicromanager.TrendMicroAPI()
        with self.assertRaises(Exception) as context:
            trendmicroapi.is_security_enabled_for_vm(vm_ip="1.1.1.1")
        self.assertTrue('SEC001_SALT_CONNECTION_ERROR' in str(context.exception))

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_enable_security_positive(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value

        mock_security.return_value = False

        trendmicroapi = trendmicromanager.TrendMicroAPI()

        instance.execute_command_with_minion_ip.return_value = self.mock_agent_positive_response
        actual_output = trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                                      WindowsPolicyID="2")
        expected_output = {'status': True, 'comment': ''}
        self.assertEqual(actual_output, expected_output)

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_already_enable_security(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value

        mock_security.return_value = True

        trendmicroapi = trendmicromanager.TrendMicroAPI()

        instance.execute_command_with_minion_ip.return_value = self.mock_agent_positive_response
        actual_output = trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                                      WindowsPolicyID="2")
        self.assertTrue('already enabled' in actual_output['comment'])

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_enable_security_handle_salt_connection_error(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value

        mock_security.return_value = False

        trendmicroapi = trendmicromanager.TrendMicroAPI()

        # Installation of Trend Micro Agent Failed due to salt error
        instance.execute_command_with_minion_ip.return_value = self.mock_agent_salt_error_response
        actual_output = trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                                      WindowsPolicyID="2")
        expected_output = {'status': False, 'comment': "Error occured at salt-master side",
                           'err_code': "SEC001_SALT_CONNECTION_ERROR"}
        self.assertEqual(actual_output, expected_output)

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_enable_security_handle_improper_salt_response(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value

        mock_security.return_value = False

        trendmicroapi = trendmicromanager.TrendMicroAPI()

        # Improper response from saltutil class
        instance.execute_command_with_minion_ip.return_value = self.mock_agent_Improper_response
        actual_output = trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                                      WindowsPolicyID="2")
        expected_output = {'status': False, 'comment': SECURITY_ERRORS["SEC005_UNKNOWN_SALT_API_RESPONSE"],
                           'err_code': "SEC005_UNKNOWN_SALT_API_RESPONSE"}
        self.assertEqual(actual_output, expected_output)

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_enable_security_api_exception(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value

        mock_security.return_value = False 

        trendmicroapi = trendmicromanager.TrendMicroAPI()

        instance.execute_command_with_minion_ip.side_effect = mock_raise_api_exception
        actual_output = trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                                      WindowsPolicyID="2")
        self.assertTrue('SEC009_DSM_API' in actual_output['err_code'])

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_enable_security_handle_null_response(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        trendmicroapi = trendmicromanager.TrendMicroAPI()

        mock_security.return_value = False
        # No response from saltutil class
        instance.execute_command_with_minion_ip.return_value = self.mock_NO_response
        actual_output = trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                                      WindowsPolicyID="2")
        expected_output = {'status': False,
                           'comment': SECURITY_ERRORS["SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE"],
                           'err_code': "SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE"}
        self.assertEqual(actual_output, expected_output)

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_enable_security_handle_agent_install_failure(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value

        mock_security.return_value = False

        trendmicroapi = trendmicromanager.TrendMicroAPI()

        # Install Trend micro agent on VM failed
        instance.execute_command_with_minion_ip.return_value = self.mock_agent_install_Agent_fail_response
        actual_output = trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                                      WindowsPolicyID="2")
        expected_output = {'status': False, 'comment': SECURITY_ERRORS["SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE"],
                           'err_code': "SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE",
                           'err_trace': '/tmp/tmplyHli1.sh: line 15: Download_Install_Agent: command not found '
                                        '/tmp/tmplyHli1.sh: line 27: /opt/ds_agent/dsa_control: '
                                        'No such file or directory'}
        self.assertEqual(actual_output, expected_output)

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_enable_security_handle_activation_security_failed(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value

        mock_security.return_value = False

        trendmicroapi = trendmicromanager.TrendMicroAPI()

        # Enable security on VM failed
        instance.execute_command_with_minion_ip.return_value = self.mock_agent_enable_Security_fail_response
        actual_output = trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                                      WindowsPolicyID="2")
        expected_output = {'status': False, 'comment': SECURITY_ERRORS["SEC004_ENABLE_SECURITY_FAILED"],
                           'err_code': "SEC004_ENABLE_SECURITY_FAILED",
                           'err_trace': '.dsm_ip, https://a0jdus042dsm001:4119, Downloading agent package ... '
                                        'curl https://A0JDUS042DSM001.vs-secops.cloud:4119/software/agent/'
                                        'RedHat_EL6/x86_64/ -o /tmp/agent.rpm --insecure --silent --tlsv1.2 '
                                        'Installing agent package ..., Preparing..., Host platform - Distributor '
                                        'ID: CentOS, ds_agent, Starting ds_agent: [  OK  ] '
                                        'HTTP Status: 200 - OK, Activation will be re-attempted 30 time(s) '
                                        'in case of failure, HTTP Status: 400 - OK, Response: '
                                        'Attempting to connect to https://a0jdus042dsm002:4120/, '
                                        'Error: activation was not successful. '
                                        'The manager may not be configured to allow agent-initiated activation, '
                                        'or the manager may not be configured to allow re-activation of existing hosts.'}
        self.assertEqual(actual_output, expected_output)

    @patch('security.trendmicromanager.TrendMicroAPI.is_security_enabled_for_vm')
    @patch('security.trendmicromanager.get_config')
    @patch('security.trendmicromanager.SaltNetAPI')
    def test_enable_security_handle_runtime_exception(self, mock_salt_api, mock_config, mock_security):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        trendmicroapi = trendmicromanager.TrendMicroAPI()

        mock_security.return_value = False
        instance.execute_command_with_minion_ip.side_effect = mock_raise_exception
        with self.assertRaises(Exception) as context:
            trendmicroapi.enable_security(vm_hostname="dummy", vm_ip="1.1.1.1", LinuxPolicyID="1",
                                          WindowsPolicyID="2")
            self.assertTrue('Unknown exception' in str(context.exception))

    def setUp(self):
        self.mock_agent_positive_response = \
            {'status': True,
             'comment':
                 {'return':
                         [
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
                             }
                         ]
                 }
             }

        self.mock_agent_salt_error_response = {'status': False,
                                               'comment': "Error occured at salt-master side"}

        self.mock_agent_Improper_response = {'status': False}
        self.mock_NO_response = None

        self.mock_agent_install_Agent_fail_response = \
            {'status': True,
             'comment':
                 {'return': [{'security_vm.xstest.local': {
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
                         }
                         }
                     ]
                 }
             }

        self.mock_agent_enable_Security_fail_response = \
            {'status': True,
             'comment':
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
                                                        'curl https://A0JDUS042DSM001.vs-secops.cloud:4119/software/agent/RedHat_EL6/x86_64/ -o /tmp/agent.rpm --insecure --silent --tlsv1.2 '
                                                        'Installing agent package ..., Preparing..., Host platform - Distributor ID: CentOS, ds_agent, Starting ds_agent: [  OK  ] '
                                                        'HTTP Status: 200 - OK, Activation will be re-attempted 30 time(s) in case of failure, HTTP Status: 400 - OK, Response: '
                                                        'Attempting to connect to https://a0jdus042dsm002:4120/, '
                                                        'Error: activation was not successful. The manager may not be configured to allow agent-initiated activation, '
                                                        'or the manager may not be configured to allow re-activation of existing hosts.' },
                                  'result': True,
                                  }
                         }
                         }
                     ]
                 }
             }
