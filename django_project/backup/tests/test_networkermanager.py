import backup.networkermanager as networkermanager
from mock import patch
import unittest
from backup.constants import BACKUP_ERRORS

networker_dict = {"password": "",
                  "pg15": "Bronze-Filesystem15",
                  "pg30": "Bronze-Filesystem30",
                  "url": "",
                  "username": ""}


def mock_exception(self):
    raise Exception("Unknown Exception - Message")


def mock_raise_exception(vm_hostname):
    raise Exception("Dummy exception!!")


def mock_raise_exception_pause(vm_hostname, task_id, state):
    raise Exception("Dummy exception!!")


def mock_raise_exception_minion_ip(vm_hostname):
    raise Exception("Unknown exception")


def mock_get_config(key, attribute):
    data_dict = \
        {"networker_server_details":
             {"NETWORKER_SERVERS":
                  [{"password": "password",
                    "pg15": "Bronze-Filesystem15",
                    "pg30": "Bronze-Filesystem30",
                    "url": "https://1.1.1.1:9090",
                    "username": "test",
                    "hostname": "nw1",
                    "minionid": "minionid"}],
              "DATADOMAIN_SERVERS":
                  [{"hostname": "ddhostname",
                    "ip": "1.2.1.1"}],
              "DOMAIN_NAME": "example.com",
              "NETWORKER_SERVER_COUNT": "1",
              "NETWORKER_MAX_CLIENTS": "2",
              "NETWORKER_MAX_JOBS": "1",
              "ADD_HOSTNAME_SCRIPT_PATH": "networker/add_hosts"},
         "networker_client_details":
             {"INSTALLER_AGENT_SCRIPT_PATH": "networker/unix_client",
              "ENABLE_BACKUP_SCRIPT_PATH": "networker/enable_backup",
              "DISABLE_BACKUP_SCRIPT_PATH": "networker/disable_backup",
              "HOST_ENTRY_SCRIPT_PATH": "networker/etchosts"},
         "salt_master_details":
             {"MASTER_IP": "",
              "MASTER_API_PORT": "",
              "MASTER_API_USERNAME": "",
              "MASTER_API_PASSWORD": "",
              "MASTER_SALT_BASE_LOCATION": "",
              "SSH_PORT_NUMBER": 22},
         "salt_retries_config_values":
             {"SALT_JOB_RUNNING_RETRIES": 1, "SALT_JOB_RETRIES_TIMEOUT": 0,
              "SALT_PING_NO_OF_RETRIES": 1, "SALT_PING_RETRIES_TIMEOUT": 0}}

    return data_dict[key][attribute]


def mock_get_config_for_multiple_networker(key, attribute):
    data_dict = \
        {"networker_server_details":
            {"NETWORKER_SERVERS":
                [{"password": "password1",
                  "pg15": "Bronze-Filesystem15",
                  "pg30": "Bronze-Filesystem30",
                  "url": "https://1.1.1.1:9090",
                  "username": "test1",
                  "hostname": "nw1",
                  "minionid": "minionid1"},
                 {"password": "password2",
                  "pg15": "Bronze-Filesystem15",
                  "pg30": "Bronze-Filesystem30",
                  "url": "https://1.1.1.2:9090",
                  "username": "test2",
                  "hostname": "nw2",
                  "minionid": "minionid2"}],
             "DOMAIN_NAME": "example.com",
             "NETWORKER_SERVER_COUNT": "1",
             "NETWORKER_MAX_CLIENTS": "2",
             "NETWORKER_MAX_JOBS": "1",
             "ADD_HOSTNAME_SCRIPT_PATH": "networker/add_hosts"}}
    return data_dict[key][attribute]


class TestNetworkerManager(unittest.TestCase):

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pick_networker_handle_no_networker_selected(self, mock_nw, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_nw.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.get_client.return_value = {}
        instance.is_full.return_value = True
        actual_output = networkerapi.pick_networker("dummy")
        self.assertEqual(actual_output, None)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pick_networker_handle_unable_to_reach_networker(self, mock_nw, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_nw.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.get_client.return_value = self.mock_get_client_unreachable_nw
        instance.is_full.return_value = True
        actual_output = networkerapi.pick_networker("dummy")
        self.assertEqual(actual_output, None)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pick_networker_handle_some_networker_unreachable(self, mock_nw, mock_config):
        mock_config.side_effect = mock_get_config_for_multiple_networker
        instance = mock_nw.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.get_client.side_effect = [self.mock_get_client_unreachable_nw, {}]
        instance.is_full.side_effect = [True, False]
        actual_output = networkerapi.pick_networker("dummy")
        expected_output = mock_get_config_for_multiple_networker(
            "networker_server_details", "NETWORKER_SERVERS")[1]
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pick_networker_handle_already_configured_networker(self, mock_nw, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_nw.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.get_client.return_value = self.mock_get_client
        actual_output = networkerapi.pick_networker("NVE-1")
        expected_output = mock_get_config("networker_server_details", "NETWORKER_SERVERS")[0]
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pick_networker_handle_networker_selected(self, mock_nw, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_nw.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.get_client.return_value = {}
        instance.is_full.return_value = False
        actual_output = networkerapi.pick_networker("dummy")
        expected_output = mock_get_config("networker_server_details", "NETWORKER_SERVERS")[0]
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.SaltNetAPI')
    def test_get_minion_name_success(self, mock_salt_api):
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.get_minion_name.return_value = {'status': True, 'minion_name': 'minion'}
        result = networkerapi.get_minion_name("1.1.1.1")
        expected_output = {'status': True, 'minion_name': 'minion'}
        self.assertEqual(result, expected_output)

    @patch('backup.networkermanager.SaltNetAPI')
    def test_get_minion_name_failed(self, mock_salt_api):
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.get_minion_name.return_value = {'status': False, 'comment': 'unable to fetch minion name'}
        result = networkerapi.get_minion_name("1.1.1.1")
        expected_output = {'status': False, 'comment': 'unable to fetch minion name'}
        self.assertEqual(result, expected_output)

    @patch('backup.networkermanager.SaltNetAPI')
    def test_get_fqdn_from_minion_id_success(self, mock_salt_api):
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.get_fqdn_from_minion_id.return_value = {'status': True, 'fqdn': 'dummy.xstest.local'}
        result = networkerapi.get_fqdn_from_minion_id("dummy")
        expected_output = {'status': True, 'fqdn': 'dummy.xstest.local'}
        self.assertEqual(result, expected_output)

    @patch('backup.networkermanager.SaltNetAPI')
    def test_get_fqdn_from_minion_id_failed(self, mock_salt_api):
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.get_fqdn_from_minion_id.return_value = {'status': False, 'comment': 'unable to fetch fqdn'}
        result = networkerapi.get_fqdn_from_minion_id("dummy")
        expected_output = {'status': False, 'comment': 'unable to fetch fqdn'}
        self.assertEqual(result, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_add_host_entry_on_minion_success(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        instance.execute_command.return_value = self.mock_agent_positive_response
        networkerapi = networkermanager.NetworkerAPI()

        actual_output = networkerapi.add_host_entry_on_minion(vm_minion_id="dummy")
        expected_output = {'status': True, 'comment': ''}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_add_host_entry_on_minion_handle_null_response(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.execute_command.return_value = None
        actual_output = networkerapi.add_host_entry_on_minion(vm_minion_id="dummy")
        expected_output = {'status': False,
                           'comment': 'Unable to add host entry on VM'}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_add_host_entry_on_minion_handle_response_in_improper_format(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.execute_command.return_value = {'status': False}
        actual_output = networkerapi.add_host_entry_on_minion(vm_minion_id="dummy")
        expected_output = {'status': False, 'comment':
                           'Response received after executing the salt '
                           'add host entry api command is not proper'}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_add_host_entry_on_minion_handle_adding_entry_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.execute_command.return_value = self.mock_dns_entry_on_minion_failed_response
        actual_output = networkerapi.add_host_entry_on_minion(vm_minion_id="dummy")
        expected_output = {'status': False,
                           'comment': 'Failed to add host entry on minion '
                                      'vm at step 1 due to : etchosts.sls execution failed'}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_add_host_entry_on_minion_handle_execution_of_script_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = {'status': False,
                                                 'comment': "Not able to run script properly"}
        actual_output = networkerapi.add_host_entry_on_minion(vm_minion_id="dummy")
        expected_output = {'status': False, 'comment': "Not able to run script properly"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_add_host_entry_on_minion_handle_runtime_exception(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.execute_command.return_value = {'status': True, 'comment': {}}
        with self.assertRaises(Exception) as context:
            networkerapi.add_host_entry_on_minion(vm_minion_id="dummy")
            self.assertTrue('Unknown exception' in str(context.exception))

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_install_networker_agent_positive(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        instance.execute_command.return_value = self.mock_agent_positive_response
        networkerapi = networkermanager.NetworkerAPI()

        actual_output = networkerapi.install_networker_agent(vm_hostname="dummy", vm_minion_id="dummy")
        expected_output = {'status': True, 'comment': ''}
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_install_networker_agent_handle_null_response(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        instance.execute_command.return_value = None
        networkerapi = networkermanager.NetworkerAPI()

        actual_output = networkerapi.install_networker_agent(vm_hostname="dummy", vm_minion_id="dummy")
        expected_output = {'status': False, 'comment': 'Unable to install networker agent on VM'}
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_install_networker_agent_handle_improper_format_response(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        instance.execute_command.return_value = {'status': False}
        networkerapi = networkermanager.NetworkerAPI()

        actual_output = networkerapi.install_networker_agent(vm_hostname="dummy", vm_minion_id="dummy")
        expected_output = {'status': False, 'comment': 'Response received after executing the '
                                                       'salt net api command is not proper'}
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_install_networker_agent_handle_rpm_copy_to_minion_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_0
        actual_output = networkerapi.install_networker_agent(vm_hostname="dummy", vm_minion_id="dummy")
        expected_output = {'status': False,
                           'comment': 'Process to copy networker agent'
                                      'package on the VM failed due to :'
                                      'File /opt/lgtoclnt.rpm is not in the correct state'}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_install_networker_agent_handle_agent_install_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_1
        actual_output = networkerapi.install_networker_agent(vm_hostname="dummy", vm_minion_id="dummy")
        expected_output = {'status': False,
                           'comment': 'Process to install networker agent '
                                      'package on the VM failed due to :'
                                      'All specified packages installation failed'}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_install_networker_agent_handle_start_networker_service_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = self.mock_agent_negative_response_run_num_2
        actual_output = networkerapi.install_networker_agent(vm_hostname="dummy", vm_minion_id="dummy")
        expected_output = {'status': False,
                           'comment': 'Process to start the networker service on the VM failed '
                                      'due to : Command "/etc/init.d/networker start" run'}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_install_networker_agent_handle_script_execution_failed(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = {'status': False,
                                                 'comment': "Not able to run script properly"}
        actual_output = networkerapi.install_networker_agent(vm_hostname="dummy",
                                                             vm_minion_id="dummy")
        expected_output = {'status': False,
                           'comment': "Not able to run script properly"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_install_networker_agent_handle_runtime_exception(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = {'status': True, 'comment': {}}
        with self.assertRaises(Exception) as context:
            networkerapi.install_networker_agent(vm_hostname="dummy", vm_minion_id="dummy")
            self.assertTrue('Unknown exception' in str(context.exception))

    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.get_config')
    def test_add_entry_to_networker_positive(self, mock_config, mock_salt_api):
        mock_config.return_value = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = self.mock_add_entry_to_networker_positive_reponse
        actual_output = networkerapi.add_entry_to_host_file("dummy", "10.20.30.40", "dummy", "dummy")
        expected_output = {'status': True, 'comment': ''}
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.get_config')
    def test_add_entry_to_networker_status_false(self, mock_config, mock_salt_api):
        mock_config.return_value = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = {'status': False,
                                                 'comment': "Adding dns entry in networker failed"}
        actual_output = networkerapi.add_entry_to_host_file("dummy", "10.20.30.40", "dummy", "dummy")
        expected_output = {'status': False, 'comment': "Adding dns entry in networker failed",
                           'err_code': 'SALT ERROR', 'err_trace': None}
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.get_config')
    def test_add_entry_to_networker_response_not_proper(self, mock_config, mock_salt_api):
        mock_config.return_value = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = {'status': False}
        actual_output = networkerapi.add_entry_to_host_file("dummy", "10.20.30.40", "dummy", "dummy")
        expected_output = {'status': False,
                           'comment': "Response received after executing the salt "
                                      "net api command is not proper",
                           'err_code': 'BACKUP015_SALT_EXECUTION_ERROR', 'err_trace': None}
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.get_config')
    def test_add_entry_to_networker_response_none(self, mock_config, mock_salt_api):
        mock_config.return_value = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.return_value = None
        actual_output = networkerapi.add_entry_to_host_file("dummy", "10.20.30.40", "dummy", "dummy")
        expected_output = {'status': False, 'comment': 'Unable to add DNS entry',
                           'err_code': 'BACKUP014_DNS_ENTRY_FAILURE', 'err_trace': None}
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.get_config')
    def test_add_entry_to_networker_exception_test(self, mock_config, mock_salt_api):
        mock_config.return_value = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()
        instance.execute_command.side_effect = mock_raise_exception
        with self.assertRaises(Exception) as context:
            networkerapi.add_entry_to_host_file("dummy", "10.20.30.40", "dummy", "dummy")
            self.assertTrue('Unknown exception' in str(context.exception))

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_enable_backup_success(self, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.enable_backup.return_value = self.mock_backup_positive_response
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.enable_backup_on_client("dummy", ["All"],
                                                             "Bronze-Filesystem", networker_dict)
        expected_output = {'status': True,
                           'comment': 'Client created with Resource ID 83.0.243'
                                      ' Client added to the protection group.'
                                      ' The response is <Response [204]>', 'target_vm': 'dummy'}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_enable_backup_handle_failed_response(self, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.enable_backup.return_value = {}
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.enable_backup_on_client("dummy", ["All"],
                                                             "Bronze-Filesystem", networker_dict)
        expected_output = {'status': False,
                           'comment': 'Unable to fulfill the request. Response is '
                                      'not in proper format.', 'target_vm': 'dummy',
                           'error_code': 500}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_enable_backup_handle_runtime_exception(self, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.enable_backup.return_value = {}
        networkerapi = networkermanager.NetworkerAPI()

        with self.assertRaises(Exception) as context:
            instance.enable_backup.return_value = mock_raise_exception
            networkerapi.enable_backup_on_client("dummy", ["All"],
                                                 "Bronze-Filesystem", networker_dict)
            self.assertTrue('Unknown exception' in str(context.exception))

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_check_minion_status_success(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.get_vm_minion_status.return_value = {'status': True}
        result = networkerapi.check_minion_status('1.1.1.1')
        self.assertTrue(result, True)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_check_minion_status_handle_failed_response(self, mock_salt_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance = mock_salt_api.return_value
        networkerapi = networkermanager.NetworkerAPI()

        instance.get_vm_minion_status.return_value = {'status': False}
        result = networkerapi.check_minion_status("1.1.1.1")
        self.assertFalse(result, False)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pause_backup_success(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.get_client.return_value = client_resp
        instance.change_backup_state.return_value.ok = True
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.pause_vm_backup_service("dummy", "task_id")
        expected_output = {'status': True}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pause_backup_failure_at_api(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.get_client.return_value = client_resp
        err_response = {'error_code': '400', 'error_message': 'Failed'}
        instance.change_backup_state.return_value = err_response
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.pause_vm_backup_service("dummy", "task_id")
        expected_output = {'status': False}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pause_backup_failure_with_error_code(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.get_client.return_value = client_resp
        instance.change_backup_state.return_value.ok = False
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.pause_vm_backup_service("dummy", "task_id")
        expected_output = {'status': False}
        self.assertTrue(actual_output, expected_output)
        self.assertEqual("BACKUP500_INTERNAL_SERVER_ERROR", actual_output['err_code'])

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pause_backup_failure_no_clients(self, mock_networker, mock_config):
        client_resp = {}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.get_client.return_value = client_resp
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.pause_vm_backup_service("dummy", "task_id")
        expected_output = {'status': False}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_pause_backup_handle_runtime_exception(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        with self.assertRaises(Exception) as context:
            instance.get_client.return_value = client_resp
            instance.change_backup_state.return_value = mock_raise_exception_pause
            networkerapi = networkermanager.NetworkerAPI()
            networkerapi.pause_vm_backup_service("dummy", "task_id")
            self.assertTrue('Unknown exception' in str(context.exception))

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_disable_backup_set_vm_maintainence_mode_in_networker_fails(
            self, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_fail
        actual_output = mock_netmgr.disable_vm_backup_service("dummy", "task_id")
        expected_output = {"err_code": 123, "err_trace": "", "comment": "error_occurred"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @ patch('backup.networkermanager.SaltNetAPI')
    def test_disable_backup_check_minion_fails(
            self, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_pass
        mock_netmgr.check_minion_status.return_value = False

        actual_output = mock_netmgr.disable_vm_backup_service("dummy", "task_id")
        expected_output = {"err_code": "BACKUP010_CHECK_HOSTNAME", "err_trace": "",
                           "comment": "Please check the hostname you have entered. "
                                      "In case the hostname is correct, please contact "
                                      "your administrator"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_disable_backup_get_minion_id_fails(self, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_pass
        mock_netmgr.check_minion_status.return_value = True
        mock_netmgr.get_minion_name_from_hostname.return_value = self.mock_minion_id

        actual_output = mock_netmgr.disable_vm_backup_service("dummy", "task_id")
        expected_output = {"err_code": "MINION_ID_ERROR", "err_trace": "",
                           "comment": "Couldn't fetch minion ID"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.ResponseParser')
    def test_disable_backup_cleanup_fails_with_False_status(
            self, mock_parser, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_pass
        mock_netmgr.check_minion_status.return_value = True
        mock_netmgr.get_minion_name_from_hostname.return_value = self.mock_minion_id_pass
        mock_salt.execute_command.return_value = self.mock_agent_positive_response
        mock_parser.parse_minion_backup_cleanup_salt_response.return_value = self.mock_cleanup_parse_fail

        actual_output = mock_netmgr.disable_vm_backup_service("dummy", "task_id")
        expected_output = {"err_code": 123, "err_trace": "", "comment": "error_occurred"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.ResponseParser')
    def test_disable_backup_comment_fails_with_False_status(
            self, mock_parser, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_pass
        mock_netmgr.check_minion_status.return_value = True
        mock_netmgr.get_minion_name_from_hostname.return_value = self.mock_minion_id_pass
        mock_salt.execute_command.return_value = self.mock_agent_positive_response
        mock_parser.parse_minion_backup_cleanup_salt_response.return_value = {"status": True}
        mock_netmgr.get_minion_name_from_hostname.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        mock_parser.parse_networker_minion_host_comment_salt_response.return_value = \
            self.mock_cleanup_parse_fail

        actual_output = mock_netmgr.disable_vm_backup_service("dummy", "task_id")
        expected_output = {"err_code": 123, "err_trace": "", "comment": "error_occurred"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_disable_backup_handle_runtime_exception(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        with self.assertRaises(Exception) as context:
            instance.get_client.return_value = client_resp
            instance.change_backup_state.return_value = mock_raise_exception
            networkerapi = networkermanager.NetworkerAPI()
            networkerapi.disable_vm_backup_service("dummy", "task_id")
            self.assertTrue('Unknown exception' in str(context.exception))

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.ResponseParser')
    def test_disable_backup_success(
            self, mock_parser, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_pass
        mock_netmgr.check_minion_status.return_value = True
        mock_netmgr.get_minion_name_from_hostname.return_value = self.mock_minion_id_pass
        mock_salt.execute_command.return_value = self.mock_agent_positive_response
        mock_parser.parse_minion_backup_cleanup_salt_response.return_value = {"status": True}
        mock_netmgr.get_minion_name_from_hostname.return_value = \
            mock_get_config("networker_server_details", "NETWORKER_SERVERS")[0]
        mock_parser.parse_networker_minion_host_comment_salt_response.return_value = {"status": True}

        actual_output = mock_netmgr.disable_vm_backup_service("dummy", "task_id")
        expected_output = {"status": True}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_decommission_backup_set_vm_maintainence_mode_in_networker_fails(
            self, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_fail
        actual_output = mock_netmgr.decommission_vm_backup_service("dummy", "task_id")
        expected_output = {"err_code": 123, "err_trace": "", "comment": "error_occurred"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    def test_decommission_backup_networker_fetch_fail(
            self, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_pass
        mock_netmgr.find_networker.return_value = None
        actual_output = mock_netmgr.decommission_vm_backup_service("dummy", "task_id")
        expected_output = {"err_code": "BACKUP011_CLIENT_NOT_CONFIGURED",
                           "err_trace": "", "comment": "Backup is not enabled for this VM"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_decommission_backup_handle_runtime_exception(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        with self.assertRaises(Exception) as context:
            instance.get_client.return_value = client_resp
            instance.change_backup_state.return_value = mock_raise_exception
            networkerapi = networkermanager.NetworkerAPI()
            networkerapi.decommission_vm_backup_service("dummy", "task_id")
            self.assertTrue('Unknown exception' in str(context.exception))

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.ResponseParser')
    def test_decommission_backup_parse_fail(
            self, mock_parser, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_pass
        mock_netmgr.find_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        mock_salt.execute_command.return_value = self.mock_agent_positive_response
        mock_parser.parse_minion_backup_cleanup_salt_response.return_value = self.mock_cleanup_parse_fail

        actual_output = mock_netmgr.decommission_vm_backup_service("dummy", "task_id")
        expected_output = {"err_code": 123, "err_trace": "", "comment": "error_occurred"}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    @patch('backup.networkermanager')
    @patch('backup.networkermanager.SaltNetAPI')
    @patch('backup.networkermanager.ResponseParser')
    def test_decommission_backup_success(
            self, mock_parser, mock_salt, mock_netmgr, mock_networker, mock_config):
        mock_config.side_effect = mock_get_config
        mock_netmgr.pause_vm_backup_service.return_value = self.mock_pause_pass
        mock_netmgr.find_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        mock_salt.execute_command.return_value = self.mock_agent_positive_response
        mock_parser.parse_minion_backup_cleanup_salt_response.return_value = {"status": True}
        mock_parser.parse_networker_minion_host_comment_salt_response.return_value = {"status": True}
        actual_output = mock_netmgr.decommission_vm_backup_service("dummy", "task_id")
        expected_output = {"status": True}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_resume_backup_success(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.get_client.return_value = client_resp
        instance.change_backup_state.return_value.ok = True
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.resume_vm_backup_service("dummy", "task_id")
        expected_output = {'status': True}
        self.assertTrue(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_resume_backup_handle_failure_at_api(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.get_client.return_value = client_resp
        err_response = {'error_code': '400', 'error_message': 'Failed'}
        instance.change_backup_state.return_value = err_response
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.resume_vm_backup_service("dummy", "task_id")
        expected_output = {'status': False, 'comment': 'Failed', 'err_code': '400'}
        self.assertEqual(actual_output, expected_output)

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_resume_backup_failure_with_error_code(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.get_client.return_value = client_resp
        instance.change_backup_state.return_value.ok = False
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.resume_vm_backup_service("dummy", "task_id")
        expected_output = {'status': False, 'err_code': "BACKUP500_INTERNAL_SERVER_ERROR",
                           'comment': BACKUP_ERRORS["BACKUP500_INTERNAL_SERVER_ERROR"]}
        self.assertEqual(actual_output['status'], expected_output['status'])
        self.assertEqual(expected_output['err_code'], actual_output['err_code'])
        self.assertEqual(expected_output['comment'], actual_output['comment'])

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_resume_backup_failure_no_clients(self, mock_networker, mock_config):
        client_resp = {}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        instance.get_client.return_value = client_resp
        networkerapi = networkermanager.NetworkerAPI()
        actual_output = networkerapi.resume_vm_backup_service("dummy", "task_id")
        expected_output = {'status': False, 'err_code': "BACKUP011_CLIENT_NOT_CONFIGURED",
                           'comment': BACKUP_ERRORS["BACKUP011_CLIENT_NOT_CONFIGURED"]}
        self.assertEqual(actual_output['status'], expected_output['status'])
        self.assertEqual(expected_output['err_code'], actual_output['err_code'])
        self.assertEqual(expected_output['comment'], actual_output['comment'])

    @patch('backup.networkermanager.get_config')
    @patch('backup.networkermanager.Networker')
    def test_resume_backup_handle_runtime_exception(self, mock_networker, mock_config):
        client_resp = {'hostname': 'dummy', 'resourceId': {'id': '123'}, 'aliases': ['dummy']}
        mock_config.side_effect = mock_get_config
        instance = mock_networker.return_value
        with self.assertRaises(Exception) as context:
            instance.get_client.return_value = client_resp
            instance.change_backup_state.return_value = mock_raise_exception
            networkerapi = networkermanager.NetworkerAPI()
            networkerapi.resume_vm_backup_service("dummy", "task_id")
            self.assertTrue('Unknown exception' in str(context.exception))

    def setUp(self):
        self.mock_pause_fail = {"err_code": 123, "err_trace": "", "comment": "error_occurred"}
        self.mock_pause_pass = {"status": True}
        self.mock_minion_id = {"status": False, "comment": "Couldn't fetch minion ID"}
        self.mock_minion_id_pass = {"status": True, "minion_name": "mini"}
        self.mock_cleanup_parse_fail = {"status": False, "err_code": 123,
                                        "err_trace": "", "comment": "error_occurred"}
        self.mock_agent_positive_response = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'backup_vm.xstest.local': {
                            'file_|-/opt/lgtoclnt.rpm_|-managed': {
                                '__sls__': 'networker/unix_client', '__run_num__': 0,
                                'comment': 'File /opt/lgtoclnt.rpm is in the correct state',
                                'start_time': '04:35:10.057890', 'duration': 859.522,
                                'name': '/opt/lgtoclnt.rpm', 'changes': {}, 'pchanges': {},
                                '__id__': '/opt/lgtoclnt-1.x86_64.rpm', 'result': True},
                            'cmd_|-start_networker_|-/etc/init.d/networker start1_|-run':
                                {'__run_num__': 2,
                                 'comment': 'Command "/etc/init.d/networker start" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': '/etc/init.d/networker start',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': 'networker/unix_client',
                                 '__id__': 'start_networker', 'result': True},
                            'pkg_|-install_lgtoclnt.rpm_|-installed': {
                                '__run_num__': 1, 'comment': 'All specified packages are already installed',
                                'start_time': '04:35:11.528557', 'duration': 384.186,
                                'name': 'install_lgtoclnt.rpm', 'changes': {},
                                '__sls__': 'networker/unix_client',
                                '__id__': 'install_lgtoclnt.rpm', 'result': True}}}]}}

        self.mock_agent_negative_response_run_num_2 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'backup_vm.xstest.local': {
                            'file_|-/opt/lgtoclnt.rpm_|-managed': {
                                '__sls__': 'networker/unix_client', '__run_num__': 0,
                                'comment': 'File /opt/lgtoclnt.rpm is in the correct state',
                                'start_time': '04:35:10.057890', 'duration': 859.522,
                                'name': '/opt/lgtoclnt.rpm', 'changes': {}, 'pchanges': {},
                                '__id__': '/opt/lgtoclnt-1.x86_64.rpm', 'result': True},
                            'pkg_|-install_lgtoclnt.rpm_|-installed': {
                                '__run_num__': 1, 'comment': 'All specified packages are already installed',
                                'start_time': '04:35:11.528557', 'duration': 384.186,
                                'name': 'install_lgtoclnt.rpm', 'changes': {},
                                '__sls__': 'networker/unix_client',
                                '__id__': 'install_lgtoclnt.rpm', 'result': True},
                            'cmd_|-start_networker_|-/etc/init.d/networker start1_|-run':
                                {'__run_num__': 2,
                                 'comment': 'Command "/etc/init.d/networker start" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': '/etc/init.d/networker start',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': 'networker/unix_client',
                                 '__id__': 'start_networker', 'result': False}}}]}}

        self.mock_agent_negative_response_run_num_0 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'backup_vm.xstest.local': {
                            'file_|-/opt/lgtoclnt.rpm_|-managed': {
                                '__sls__': 'networker/unix_client', '__run_num__': 0,
                                'comment': 'File /opt/lgtoclnt.rpm is not in the correct state',
                                'start_time': '04:35:10.057890', 'duration': 859.522,
                                'name': '/opt/lgtoclnt.rpm', 'changes': {}, 'pchanges': {},
                                '__id__': '/opt/lgtoclnt-1.x86_64.rpm', 'result': False},
                            'pkg_|-install_lgtoclnt.rpm_|-installed': {
                                '__run_num__': 1, 'comment': 'All specified packages are already installed',
                                'start_time': '04:35:11.528557', 'duration': 384.186,
                                'name': 'install_lgtoclnt.rpm', 'changes': {},
                                '__sls__': 'networker/unix_client',
                                '__id__': 'install_lgtoclnt.rpm', 'result': True},
                            'cmd_|-start_networker_|-/etc/init.d/networker start1_|-run':
                                {'__run_num__': 2,
                                 'comment': 'Command "/etc/init.d/networker start" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': '/etc/init.d/networker start',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': 'networker/unix_client',
                                 '__id__': 'start_networker', 'result': True}}}]}}

        self.mock_agent_negative_response_run_num_1 = \
            {'status': True,
             'comment':
                {'return':
                    [
                        {'backup_vm.xstest.local': {
                            'file_|-/opt/lgtoclnt.rpm_|-managed': {
                                '__sls__': 'networker/unix_client', '__run_num__': 0,
                                'comment': 'File /opt/lgtoclnt.rpm is not in the correct state',
                                'start_time': '04:35:10.057890', 'duration': 859.522,
                                'name': '/opt/lgtoclnt.rpm', 'changes': {}, 'pchanges': {},
                                '__id__': '/opt/lgtoclnt-1.x86_64.rpm', 'result': True},
                            'pkg_|-install_lgtoclnt.rpm_|-installed': {
                                '__run_num__': 1, 'comment': 'All specified packages installation failed',
                                'start_time': '04:35:11.528557', 'duration': 384.186,
                                'name': 'install_lgtoclnt.rpm', 'changes': {},
                                '__sls__': 'networker/unix_client',
                                '__id__': 'install_lgtoclnt.rpm', 'result': False},
                            'cmd_|-start_networker_|-/etc/init.d/networker start1_|-run':
                                {'__run_num__': 2,
                                 'comment': 'Command "/etc/init.d/networker start" run',
                                 'start_time': '04:35:11.914480', 'duration': 7.474,
                                 'name': '/etc/init.d/networker start',
                                 'changes': {'pid': 18283, 'retcode': 0,
                                             'stderr': '', 'stdout': ''},
                                 '__sls__': 'networker/unix_client',
                                 '__id__': 'start_networker', 'result': True}}}]}}

        self.mock_backup_positive_response = \
            [
                {'step': 1, 'description': 'Create the client',
                 'error': {}, 'result': 'Client created with Resource ID 83.0.243'},
                {'step': 2, 'description': 'Add the client to the Protection Group', 'error': {},
                 'result': 'Client added to the protection group.'
                 ' The response is <Response [204]>'}
            ]

        self.mock_backup_negative_response = \
            [
                {'step': 1, 'description': 'Create the client',
                 'error': {}, 'result': 'Client created with Resource ID 83.0.243'},
                {"step": 2,
                 "description": "Add the client to the Protection Group",
                 "result": "An error occurred",
                 "error": {"error_message": "error occured while adding client to protection group",
                           "error_code": 500}}
            ]

        self.mock_disable_backup_positive_response = \
            [
                {"step": 1,
                 "description": "Fetch resource ID",
                 "result": "Client found",
                 "error": {}},
                {"step": 2,
                 "description": "Delete Client",
                 "result": "Client successfully Deleted. ",
                 "error": {}
                 }]

        self.mock_add_entry_to_networker_positive_reponse = \
            {
                'status': True,
                'comment':
                    {'return':
                        [
                            {'backup_vm.xstest.local': {
                                'cmd_|-start_networker_|-/etc/init.d/networker start1_|-run':
                                    {'__run_num__': 2,
                                     'comment': 'Command "/etc/init.d/networker start" run',
                                     'start_time': '04:35:11.914480', 'duration': 7.474,
                                     'name': '/etc/init.d/networker start',
                                     'changes': {'pid': 18283, 'retcode': 0,
                                                 'stderr': '', 'stdout': ''},
                                     '__sls__': 'networker/unix_client',
                                     '__id__': 'start_networker', 'result': True}}}]}}

        self.mock_add_entry_to_networker_negative_reponse = \
            {
                'status': True,
                'comment':
                    {'return':
                        [
                            {'backup_vm.xstest.local': {"unable to execute script"}}]}}
        self.mock_dns_entry_on_minion_failed_response = \
            {
                'status': True,
                'comment':
                    {'return':
                        [
                            {'backup_vm.xstest.local': {
                                'cmd_|-start_networker_|-/etc/init.d/networker start1_|-run':
                                    {'__run_num__': 2,
                                     'comment': 'etchosts.sls execution failed',
                                     'start_time': '04:35:11.914480', 'duration': 7.474,
                                     'name': '/etc/init.d/networker start',
                                     'changes': {'pid': 18283, 'retcode': 0,
                                                 'stderr': '', 'stdout': ''},
                                     '__sls__': 'networker/unix_client',
                                     '__id__': 'start_networker', 'result': False}}}]}}

        self.mock_get_client = \
            {
                "aliases": [
                    "NVE-1",
                    "NVE-1.7",
                    "nve-1.7.xstest.local"
                ],
                "applicationInformation": [],
                "blockBasedBackup": False,
                "checkpointEnabled": False,
                "clientId": "15922ad4-00000004-5b582e6d-5b582e6c-00015000-91868456",
                "hostname": "nve-1.7.xstest.local",
                "indexBackupContent": False,
                "links": [
                    {
                        "href": "https://10.100.249.48:9090/nwrestapi/v2/global/"
                                "sclients/82.0.227.11.0.0.0.0.90.46.88.91.10.100.249.48",
                        "rel": "item"
                    }]}

        self.mock_get_client_unreachable_nw = \
            {"error_code": "connection-timeout",
             "error_message": "Connection Timeout occurred, "
                              "Please Check whether Backup Server is "
                              "running and details are correct"}


if __name__ == '__main__':
    unittest.main()
