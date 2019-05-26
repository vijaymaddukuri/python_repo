from django.test import TestCase
from django.test import Client
from mock import patch
from mock import MagicMock
from django.urls import reverse


def mock_raise_exception(vm_hostname, unix_policy, win_policy):
    raise Exception("Dummy exception!!")


class TestEnable(TestCase):
    def setUp(self):
        self.mock_enable_security_success_response = \
            {'status': True}
        self.mock_enable_security_fail_response = \
            {'status': False,
             'comment': 'Execution failed.'}
        self.client = Client()

    @patch('security.views.enable.TrendMicroAPI')
    def test_post_negative_blank_data(self, mock_tm_api):
        instance_tm = mock_tm_api.return_value
        # test req method POST with invalid data
        url = reverse('enableSecurity')
        req_data = {'VirtualMachineHostName': '',
                    'VirtualMachineIPAddress': '',
                    'LinuxPolicyID': '',
                    'WindowsPolicyID': '',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        expected_json_out = {'WindowsPolicyID': ['This field may not be blank.'],
                             'LinuxPolicyID': ['This field may not be blank.'],
                             'VirtualMachineHostName': ['This field may not be blank.'],
                             'VirtualMachineIPAddress': ['This field may not be blank.']}

        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_json_out)


    @patch('security.views.enable.TrendMicroAPI')
    def test_post_negative_wrong_ip(self, mock_tm_api):
        url = reverse('enableSecurity')
        instance_tm = mock_tm_api.return_value
        # test req method POST with valid data
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '333.444.55.666',
                    'LinuxPolicyID': '0',
                    'WindowsPolicyID': '1',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        expected_json_out = {'VirtualMachineIPAddress': ['Enter a valid IPv4 address.']}
        instance_tm.enable_security.return_value = self.mock_enable_security_fail_response
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_json_out)

    @patch('security.views.enable.TrendMicroAPI')
    def test_post_negative_minion_status_false(self, mock_tm_api):
        url = reverse('enableSecurity')
        instance_tm = mock_tm_api.return_value
        # test req when fetch minion status is false
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '1.2.3.4',
                    'LinuxPolicyID': '0',
                    'WindowsPolicyID': '1',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_tm.check_minion_status.return_value = False
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 500)

    @patch('security.views.enable.TrendMicroAPI')
    def test_post_negative_fail_response(self, mock_tm_api):
        url = reverse('enableSecurity')
        instance_tm = mock_tm_api.return_value
        instance_tm.check_minion_status.return_value = True

        # test req method POST with valid data
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '1.2.3.4',
                    'LinuxPolicyID': '0',
                    'WindowsPolicyID': '1',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_tm.enable_security.return_value = self.mock_enable_security_fail_response
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 500)

    @patch('security.views.enable.TrendMicroAPI')
    def test_post_negative_fail_response(self, mock_tm_api):
        url = reverse('enableSecurity')
        instance_tm = mock_tm_api.return_value
        instance_tm.check_minion_status.return_value = True
        instance_tm.enable_security.side_effect = mock_raise_exception

        # test req method POST with valid data
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '1.2.3.4',
                    'LinuxPolicyID': '0',
                    'WindowsPolicyID': '1',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 500)

    @patch('security.views.enable.TrendMicroAPI')
    def test_post_positive(self, mock_tm_api):
        instance_tm = mock_tm_api.return_value

        # test req method POST with valid data
        url = reverse('enableSecurity')
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '1.2.3.4',
                    'LinuxPolicyID': '1',
                    'WindowsPolicyID': '2',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }

        instance_tm.enable_security.return_value = self.mock_enable_security_success_response
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 200)
