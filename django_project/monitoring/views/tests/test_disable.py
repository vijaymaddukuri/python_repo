from django.test import TestCase
from django.test import Client
from mock import patch
from django.urls import reverse


def mock_raise_tas_exception(vm_hostname, vm_ip):
    raise Exception("Dummy exception!!")


def mock_get_config(key, attribute):
    data_dict = {"nimsoft_client_details": {"INSTALLER_AGENT_SCRIPT_PATH": "nimsoft"},
                 "nimsoft_server_details": {"NIMSOFT_HUB_IP": "1.2.3.4",
                                            "NIMSOFT_HUB_NAME": "win-test-hub",
                                            "NIMSOFT_DOMAIN": "domain",
                                            "NIMSOFT_HUB_ROBOT_NAME": "win",
                                            "NIMSOFT_HUB_USERNAME": "username",
                                            "NIMSOFT_HUB_PASSWORD": "passwd"

                                            },
                 "salt_master_details":
                                             {"MASTER_IP": "1.2.3.4",
                                              "MASTER_API_PORT": "8000",
                                              "MASTER_API_USERNAME": "master_user",
                                              "MASTER_API_PASSWORD": "master_pwd",
                                              "MASTER_SALT_BASE_LOCATION": "/etc/salt",
                                              "SSH_PORT_NUMBER": 22}
                 }

    return data_dict[key][attribute]


class TestDisableMonitoring(TestCase):
    def setUp(self):
            self.mock_uninstall_nimsoft_success_response = \
                {'status': True,
                 'comment': 'Execution succeeded.'}
            self.mock_uninstall_monitoring_failure = \
                {'status': False,
                 'comment': 'Execution failed.'}
            self.client = Client()

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.views.disable.NimsoftAPI')
    def test_disable_post_positive(self, mock_nimsoft_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance_nimsoft = mock_nimsoft_api.return_value
        # test req method POST with valid data, disable monitoring on VM success
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "test.local",
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        url = reverse('disable_monitoring')
        instance_nimsoft.uninstall_nimsoft_agent.return_value = self.mock_uninstall_nimsoft_success_response
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 200)

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.views.disable.NimsoftAPI')
    def test_disable_monitoring_post_invalid_host_name(self, mock_nimsoft_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance_nimsoft = mock_nimsoft_api.return_value

        # test req method POST with invalid data
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        url = reverse('disable_monitoring')
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.views.disable.NimsoftAPI')
    def test_disable_monitoring_post_invalid_ip(self, mock_nimsoft_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance_nimsoft = mock_nimsoft_api.return_value

        # test req method POST with invalid data
        req_data = {"VirtualMachineIPAddress": "1111.0.0.0",
                    "VirtualMachineHostName": "test_host",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        url = reverse('disable_monitoring')
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

    @patch('monitoring.nimsoftmanager.get_config')
    @patch('monitoring.views.disable.NimsoftAPI')
    @patch('saltmanager.salt_utils.SaltNetAPI')
    def test_disable_monitoring_uninstallation_failed(self, mock_salt_api, mock_nimsoft_api, mock_config):
        mock_config.side_effect = mock_get_config
        instance_nimsoft = mock_nimsoft_api.return_value

        req_data = {"VirtualMachineIPAddress": "111.0.0.0",
                    "VirtualMachineHostName": "test_host",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        url = reverse('disable_monitoring')
        mock_salt_api.check_minion_status = False
        instance_nimsoft.uninstall_nimsoft_agent.side_effect = mock_raise_tas_exception
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 500)

