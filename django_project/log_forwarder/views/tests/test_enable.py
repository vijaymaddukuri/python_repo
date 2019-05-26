from django.test import TestCase
from django.test import Client
from mock import patch
from django.urls import reverse
from common.exceptions import TASException

def mock_raise_tas_exception(vm_ip):
    err_code = "TEST"
    err_message = err_code
    err_trace = ""
    raise TASException(err_code, err_message, err_trace)

def mock_raise_exception(vm_hostname, vm_ip):
    raise Exception("Dummy exception!!")

class TestLogForwarder(TestCase):

    def setUp(self):
        self.req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                         "VirtualMachineHostName": "test.local",
                         "VirtualMachineID": "2a160f6920f14e57affa4d7148e41b4e",
                         "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                         "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                         }

    @patch('log_forwarder.views.enable.SplunkSaltManager')
    def test_log_forwarder_post_invalid_hostname(self, mock_splunk_api):
        instance_splunk = mock_splunk_api.return_value

        # test req method POST with invalid data
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        url = reverse('enable_log_forwarder')

        # test req method POST with empty data
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

    @patch('log_forwarder.views.enable.SplunkSaltManager')
    def test_log_forwarder_post_negative_ipaddress(self, mock_splunk_api):
        instance_splunk = mock_splunk_api.return_value

        # test req method POST with invalid VM ip 
        url = reverse('enable_log_forwarder')
        req_data = {"VirtualMachineIPAddress": "1110.0.0.0",
                    "VirtualMachineHostName": "efsefesf",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }

        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

    @patch('log_forwarder.views.enable.SplunkSaltManager')
    def test_log_forwarder_post_negative_vm_id(self, mock_splunk_api):
        instance_splunk = mock_splunk_api.return_value
        url = reverse('enable_log_forwarder')
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "efsefesf",
                    "VirtualMachineID": "",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

    @patch('log_forwarder.views.enable.SplunkSaltManager')
    def test_log_forwarder_post_negative_vm_rid(self, mock_splunk_api):
        instance_splunk = mock_splunk_api.return_value
        url = reverse('enable_log_forwarder')
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "efsefesf",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

    @patch('log_forwarder.views.enable.SplunkSaltManager')
    def test_log_forwarder_post_negative_task_id(self, mock_splunk_api):
        instance_splunk = mock_splunk_api.return_value
        url = reverse('enable_log_forwarder')
        req_data = {"VirtualMachineIPAddress": "0.0.0.0",
                    "VirtualMachineHostName": "efsefesf",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": ""
                    }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 400)

    @patch('log_forwarder.views.enable.SplunkSaltManager')
    def test_log_forwarder_post_exception(self, mock_splunk_api):
        instance_splunk = mock_splunk_api.return_value
        url = reverse('enable_log_forwarder')
        # test req method POST with valid data, Log Forwarder pkg installation falied

        instance_splunk.install_splunk_forwarder.side_effect = mock_raise_exception
        response = self.client.post(url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('log_forwarder.views.enable.SplunkSaltManager')
    def test_log_forwarder_post_tas_exception(self, mock_splunk_api):
        instance_splunk = mock_splunk_api.return_value
        url = reverse('enable_log_forwarder')
        # test req method POST with valid data, Log Forwarder pkg installation falied

        instance_splunk.install_splunk_forwarder.side_effect = mock_raise_tas_exception
        response = self.client.post(url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('log_forwarder.views.enable.SplunkSaltManager')
    def test_enable_splunk_forwarder_positive(self, mock_splunk_api):
        instance_splunk = mock_splunk_api.return_value
        # test req method POST with valid data, enable log forwarder on VM success
        url = reverse('enable_log_forwarder')
        instance_splunk.install_splunk_forwarder.return_value = True
        response = self.client.post(url, self.req_data)
        self.assertEqual(response.status_code, 200)
