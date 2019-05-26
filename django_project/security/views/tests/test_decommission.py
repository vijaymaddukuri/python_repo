from django.test import TestCase
from django.test import Client
from mock import patch
from mock import MagicMock
from django.urls import reverse


def mock_raise_exception(vm_hostname, unix_policy, win_policy):
    raise Exception("Dummy exception!!")


class TestDecommissionVMSecurity(TestCase):

    @patch('security.views.decommission.TrendMicroAPI')
    def test_decommission_post_positive(self, mock_tm_api):
        instance_tm = mock_tm_api.return_value

        # test req method POST with valid data
        url = reverse('decommissionSecurity')
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '1.2.3.4',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        delete_resp_inst = MagicMock()
        delete_resp_inst.status_code = 200
        instance_tm.check_minion_status.return_value = True
        dsm_resp_inst = MagicMock()
        dsm_resp_inst.json.return_value = {"computers":[{"ID": 2, "hostname": "abc"}]}
        instance_tm.get_dsm_response.return_value = dsm_resp_inst
        instance_tm.delete_computer.return_value = delete_resp_inst
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 200)

    @patch('security.views.decommission.TrendMicroAPI')
    def test_decommission_post_negative_blank_fields(self, mock_tm_api):
        url = reverse('decommissionSecurity')
        # test req method POST with invalid data
        req_data = {'VirtualMachineHostName': '',
                    'VirtualMachineIPAddress': '',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        expected_json_out = {'VirtualMachineHostName': ['This field may not be blank.'],
                             'VirtualMachineIPAddress': ['This field may not be blank.']}
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_json_out)

    @patch('security.views.decommission.TrendMicroAPI')
    def test_decommission_post_negative_minion_status_false(self, mock_tm_api):
        url = reverse('decommissionSecurity')

        # test req when fetch minion status is false
        instance_tm = mock_tm_api.return_value
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '1.2.3.4',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_tm.check_minion_status.return_value = False
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 500)

    @patch('security.views.decommission.TrendMicroAPI')
    def test_decommission_post_negative_exception(self, mock_tm_api):
        url = reverse('decommissionSecurity')

        # test req when one function raises the exception.
        instance_tm = mock_tm_api.return_value
        instance_tm.check_minion_status.return_value = True
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '1.2.3.4',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }

        instance_tm.delete_computer.side_effect = mock_raise_exception
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 500)

    @patch('security.views.decommission.TrendMicroAPI')
    def test_decommission_post_negative_computer_not_found(self, mock_tm_api):
        url = reverse('decommissionSecurity')

        instance_tm = mock_tm_api.return_value
        instance_tm.check_minion_status.return_value = True
        req_data = {'VirtualMachineHostName': 'test',
                    'VirtualMachineIPAddress': '1.2.3.4',
                    "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }

        response_instance = MagicMock()
        response_instance.json.return_value = {"computers": []}
        instance_tm.get_dsm_response.return_value = ("str1", response_instance)
        expected_msg = "No computer found with the hostname test"

        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_msg)
