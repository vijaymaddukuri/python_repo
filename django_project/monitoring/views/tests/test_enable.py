from django.test import TestCase
from django.test import Client
from mock import patch
from django.urls import reverse


def mock_raise_exception(vm_hostname, vm_ip):
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


class TestEnableMonitoring(TestCase):
    def setUp(self):
        self.mock_install_nimsoft_success_response = \
            {'status': True,
             'comment': 'Execution succeeded.'}
        self.mock_install_monitoring_failure = \
            {'status': False,
             'comment': 'Execution failed.'}
        self.client = Client()

    @patch('monitoring.views.enable.NimsoftAPI')
    @patch('saltmanager.salt_utils.SaltNetAPI')
    def test_enable_monitoring_post_negative(self, mock_salt_api, mock_nimsoft_api):
        instance_nimsoft = mock_nimsoft_api.return_value

        # test req method POST with invalid data
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        url = reverse('enable_monitoring')

        # test req method POST with empty data
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

        # test req method POST with invalid VM id
        req_data = {"VirtualMachineIPAddress": "1110.0.0.0",
                    "VirtualMachineHostName": "efsefesf",
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }

        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

        # test req when fetching minion from ip failed
        
        url = reverse('enable_monitoring')
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "efsefesf",
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        mock_salt_api.check_minion_status.return_value = True
        mock_salt_api.get_minion_name_from_ip.return_value = {'comment': 'unable to fetch minion name',
                                                                 'status': False}
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 200)

        mock_salt_api.get_minion_name_from_ip.return_value = True

        # test req method POST with valid data, Monitoring pkg installation falied
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "test.local",
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }

        instance_nimsoft.install_nimsoft_agent.side_effect = mock_raise_exception
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 500)

    @patch('monitoring.views.enable.NimsoftAPI')
    def test_enable_post_positive(self, mock_nimsoft_api):
        instance_nimsoft = mock_nimsoft_api.return_value
        # test req method POST with valid data, enable monitoring on VM success
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "test.local",
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        url = reverse('enable_monitoring')
        instance_nimsoft.install_nimsoft_agent.return_value = self.mock_install_nimsoft_success_response
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 200)
