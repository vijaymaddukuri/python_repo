from django.test import Client
from django.urls import reverse
from mock import patch
import unittest
import json
from backup.constants import BACKUP_ERRORS


def mock_raise_exception(vm_hostname):
    raise Exception("Dummy exception!!")


def mock_raise_exception_pause(vm_hostname, task_id):
    raise Exception("Dummy exception!!")


def mock_get_config(key, attribute):
    data_dict = \
        {"networker_server_details":
            {"NETWORKER_SERVERS":
                [{"password": "password",
                  "pg15": "Bronze-Filesystem15",
                  "pg30": "Bronze-Filesystem30",
                  "url": "https://example.com",
                  "username": "test",
                  "nw_hostname": "test",
                  "minionid": "minionid"}],
             "DATADOMAIN_SERVERS":
                 [{"dd_hostname": "",
                   "dd_ip": ""}],
             "NETWORKER_SERVER_COUNT": "1",
             "NETWORKER_MAX_CLIENTS": "",
             "NETWORKER_MAX_JOBS": "",
             "ADD_HOSTNAME_SCRIPT_PATH": "networker/add_hosts",
             "DOMAIN_NAME": "example.com"}}
    return data_dict[key][attribute]


class TestViews(unittest.TestCase):
    def setUp(self):
        self.mock_install_networker_agent_success_response = \
            {'status': True,
             'comment': 'Execution succeeded.'}
        self.mock_install_networker_agent_fail_response = \
            {'status': False,
             'comment': 'Execution failed.'}
        self.mock_enable_backup_on_client_fail = \
            {'status': False}
        self.mock_enable_backup_on_client_success = \
            {'status': True}
        self.mock_get_minion_ip_failed = \
            {'status': False,
             'comment': 'Not able to fetch IP address of Minion id.'}
        self.mock_get_minion_ip_success = \
            {'status': True}
        self.mock_get_minion_name_success = \
            {'minion_name': "test.12sef-323fef-23rf",
             'status': True}
        self.mock_get_fqdn_from_minion_id_success = \
            {'fqdn': 'dummy',
             'status': True}
        self.get_minion_ip_success = \
            {'status': True,
             'minion_ipaddress': '10.10.10.10'}
        self.add_dns_entry_success = \
            {'status': True,
             'comment': 'adding dns entry is successful'}
        self.add_host_entry_on_minion_success = \
            {'status': True,
             'comment': 'adding host entry on minion is successful'}
        self.req_data = \
            {
                'VirtualMachineHostName': 'test',
                'retentionPeriod': 15,
                'retentionPeriodType': 'Day',
                'VirtualMachineID': '8E87A82F-D40C-4200-A62E-A8E12291B0BD',
                'VirtualMachineIPAddress': '10.10.10.10',
                'VirtualMachineRID': 'vmrid',
                'TaskID': 'task123'
            }
        self.mock_pause_backup_client_fail = \
            {'status': False,
             'comment': "Name 'Dummy' is not a valid host name as it cannot "
                        "be resolved in DNS. Please add it to DNS or the hosts file.",
             'err_code': 400}
        self.mock_pause_backup_client_success = {'status': True}
        self.mock_pause_backup_client_fail_404 = \
            {'err_code': 404,
             'comment': 'HTTP 404 Not Found',
             'status': False}
        self.mock_resume_backup_client_fail = \
            {'status': False,
             'comment': "Name 'Dummy' is not a valid host name as it cannot "
                        "be resolved in DNS.\nPlease add it to DNS or the hosts file.",
             'err_code': 400}
        self.mock_resume_backup_client_success = \
            {'status': True}
        self.mock_resume_backup_client_fail_404 = \
            {'err_code': 404,
             'comment': 'HTTP 404 Not Found',
             'status': False}
        self.mock_disable_backup_client_fail = \
            {'status': False,
             'comment': "Name 'Dummy' is not a valid host name as it cannot "
                        "be resolved in DNS.\nPlease add it to DNS or the hosts file.",
             'err_code': 400}
        self.mock_disable_backup_client_success = \
            {'status': True}
        self.mock_disable_backup_client_fail_404 = \
            {'err_code': 404,
             'comment': 'HTTP 404 Not Found',
             'status': False}
        self.mock_decommission_backup_client_fail = \
            {'status': False,
             'comment': "Name 'Dummy' is not a valid host name as it cannot "
                        "be resolved in DNS.\nPlease add it to DNS or the hosts file.",
             'err_code': 400}
        self.mock_decommission_backup_client_success = \
            {'status': True}
        self.mock_decommission_backup_client_fail_404 = \
            {'err_code': 404,
             'comment': 'HTTP 404 Not Found',
             'status': False}
        self.enable_backup_url = reverse('enableBackup')
        self.disable_backup_url = reverse('disableBackup')
        self.decommission_backup_url = reverse('decommissionBackup')
        self.pause_backup_url = reverse('pauseBackup')
        self.resume_backup_url = reverse('resumeBackup')
        self.client = Client()

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_invalid_data(self, mock_nw_api):
        req_data = {'VirtualMachineHostName': '',
                    'retentionPeriod': 0,
                    'retentionPeriodType': '',
                    'VirtualMachineID': '',
                    'VirtualMachineIPAddress': '',
                    'VirtualMachineRID': '',
                    'TaskID': ''
                    }
        response = self.client.post(self.enable_backup_url, req_data)
        tmp = response.content.decode()
        tmp_dict = json.loads(tmp)
        expected_output = {'VirtualMachineRID': ['This field may not be blank.'],
                           'VirtualMachineHostName': ['This field may not be blank.'],
                           'VirtualMachineID': ['"" is not a valid UUID.'],
                           'VirtualMachineIPAddress': ['This field may not be blank.'],
                           'retentionPeriodType': ['This field may not be blank.'],
                           'TaskID': ['This field may not be blank.']}
        self.assertEqual(expected_output, tmp_dict)
        self.assertEqual(response.status_code, 400)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_no_VirtualMachineHostName(self, mock_nw_api):
        req_data = {'VirtualMachineHostName': '',
                    'retentionPeriod': 15,
                    'retentionPeriodType': 'Day',
                    'VirtualMachineID': '8E87A82F-D40C-4200-A62E-A8E12291B0BD',
                    'VirtualMachineIPAddress': '10.10.10.10',
                    'VirtualMachineRID': 'vmrid',
                    'TaskID': 'task123'
                    }
        response = self.client.post(self.enable_backup_url, req_data)
        tmp = response.content.decode()
        tmp_dict = json.loads(tmp)
        expected_output = {"VirtualMachineHostName": ["This field may not be blank."]}
        self.assertEqual(tmp_dict['VirtualMachineHostName'],
                         expected_output['VirtualMachineHostName'])
        self.assertEqual(response.status_code, 400)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_no_retention_period(self, mock_nw_api):
        req_data = {'VirtualMachineHostName': 'test',
                    'retentionPeriod': '',
                    'retentionPeriodType': 'Day',
                    'VirtualMachineID': '8E87A82F-D40C-4200-A62E-A8E12291B0BD',
                    'VirtualMachineIPAddress': '10.10.10.10',
                    'VirtualMachineRID': 'vmrid',
                    'TaskID': 'task123'
                    }
        response = self.client.post(self.enable_backup_url, req_data)
        tmp = response.content.decode()
        tmp_dict = json.loads(tmp)
        expected_output = {"retentionPeriod": ['A valid integer is required.']}
        self.assertEqual(tmp_dict['retentionPeriod'],
                         expected_output['retentionPeriod'])
        self.assertEqual(response.status_code, 400)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_no_retention_period_type(self, mock_nw_api):
        req_data = {'VirtualMachineHostName': 'test',
                    'retentionPeriod': 15,
                    'retentionPeriodType': '',
                    'VirtualMachineID': '8E87A82F-D40C-4200-A62E-A8E12291B0BD',
                    'VirtualMachineIPAddress': '10.10.10.10',
                    'VirtualMachineRID': 'vmrid',
                    'TaskID': 'task123'
                    }
        response = self.client.post(self.enable_backup_url, req_data)
        tmp = response.content.decode()
        tmp_dict = json.loads(tmp)
        expected_output = {"retentionPeriodType": ["This field may not be blank."]}
        self.assertEqual(tmp_dict['retentionPeriodType'],
                         expected_output['retentionPeriodType'])
        self.assertEqual(response.status_code, 400)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_invalid_host_name(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = False
        req_data = {'VirtualMachineHostName': 'test one',
                    'retentionPeriod': 15,
                    'retentionPeriodType': 'Day',
                    'VirtualMachineID': '8E87A82F-D40C-4200-A62E-A8E12291B0BD',
                    'VirtualMachineIPAddress': '10.10.10.10',
                    'VirtualMachineRID': 'vmrid',
                    'TaskID': 'task123'
                    }
        response = self.client.post(self.enable_backup_url, req_data)
        tmp = response.content.decode()
        tmp_dict = json.loads(tmp)
        expected_output = "Please check the hostname you have entered. " \
                          "In case the hostname is correct, please " \
                          "contact your administrator"
        self.assertEqual(tmp_dict, expected_output)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_invalid_retention_period(self, mock_nw_api):
        req_data = {'VirtualMachineHostName': 'test',
                    'retentionPeriod': 20,
                    'retentionPeriodType': 'Day',
                    'VirtualMachineID': '8E87A82F-D40C-4200-A62E-A8E12291B0BD',
                    'VirtualMachineIPAddress': '10.10.10.10',
                    'VirtualMachineRID': 'vmrid',
                    'TaskID': 'task123'
                    }
        response = self.client.post(self.enable_backup_url, req_data)
        expected_output = '"Invalid retention period. Currently the supported ' \
                          'values are \'15 Day\' and \'30 Day\'"'
        self.assertEqual(response.content.decode(), expected_output)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_invalid_retention_period_type(self, mock_nw_api):
        req_data = {'VirtualMachineHostName': 'test',
                    'retentionPeriod': 15,
                    'retentionPeriodType': 'invalid',
                    'VirtualMachineID': '8E87A82F-D40C-4200-A62E-A8E12291B0BD',
                    'VirtualMachineIPAddress': '10.10.10.10',
                    'VirtualMachineRID': 'vmrid',
                    'TaskID': 'task123'
                    }
        response = self.client.post(self.enable_backup_url, req_data)
        expected_output = '"Invalid retention period type. Currently ' \
                          'the supported value is \'Day\'"'
        self.assertEqual(response.content.decode(), expected_output)
        self.assertEqual(response.status_code, 400)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_no_networker(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = None
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_minion_status_false(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = False
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_fetch_minion_hostname_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            {'comment': 'unable to fetch minion name', "status": False}
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_get_fqdn_minion_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            self.mock_get_minion_name_success
        instance_nw.get_fqdn_from_minion_id.return_value = \
            {'comment': 'unable to fetch fqdn', 'status': False}
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_networker_agent_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            self.mock_get_minion_name_success
        instance_nw.get_fqdn_from_minion_id.return_value = self.mock_get_fqdn_from_minion_id_success
        instance_nw.install_networker_agent.return_value = self.mock_install_networker_agent_fail_response
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_add_dns_entry_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            self.mock_get_minion_name_success
        instance_nw.get_fqdn_from_minion_id.return_value = self.mock_get_fqdn_from_minion_id_success
        instance_nw.install_networker_agent.return_value = self.mock_install_networker_agent_success_response
        instance_nw.add_entry_to_host_file.return_value = \
            {'status': False, 'comment': 'adding dns entry is failed'}
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    def test_enable_backup_add_host_entry_on_minion_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            self.mock_get_minion_name_success
        instance_nw.get_fqdn_from_minion_id.return_value = self.mock_get_fqdn_from_minion_id_success
        instance_nw.install_networker_agent.return_value = self.mock_install_networker_agent_success_response
        instance_nw.add_entry_to_host_file.return_value = self.add_dns_entry_success
        instance_nw.add_host_entry_on_minion.return_value = \
            {'status': False, 'comment': 'adding host entry on minion failed'}
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    @patch('backup.views.get_pg_for_retention_time')
    def test_enable_backup_protection_group_not_found(self, pg_mock, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        pg_mock.return_value = ""
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            self.mock_get_minion_name_success
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    @patch('backup.views.get_pg_for_retention_time')
    def test_enable_backup_protection_group_invalid(self, pg_mock, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        pg_mock.return_value = "Invalid type"
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            self.mock_get_minion_name_success
        instance_nw.get_fqdn_from_minion_id.return_value = self.mock_get_fqdn_from_minion_id_success
        instance_nw.install_networker_agent.return_value = self.mock_install_networker_agent_success_response
        instance_nw.add_entry_to_host_file.return_value = self.add_dns_entry_success
        instance_nw.add_host_entry_on_minion.return_value = self.add_host_entry_on_minion_success
        req_data = {'VirtualMachineHostName': 'test',
                    'retentionPeriod': 15,
                    'retentionPeriodType': 'month'
                    }
        response = self.client.post(self.enable_backup_url, req_data)
        self.assertEqual(response.status_code, 400)

    @patch('backup.views.NetworkerAPI')
    @patch('backup.views.get_pg_for_retention_time')
    def test_enable_backup_fail(self, pg_mock, mock_nw_api):
        pg_mock.return_value = "Bronze-Filesystem15"
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            self.mock_get_minion_name_success
        instance_nw.get_fqdn_from_minion_id.return_value = self.mock_get_fqdn_from_minion_id_success
        instance_nw.install_networker_agent.return_value = self.mock_install_networker_agent_success_response
        instance_nw.add_entry_to_host_file.return_value = self.add_dns_entry_success
        instance_nw.add_host_entry_on_minion.return_value = self.add_host_entry_on_minion_success
        instance_nw.enable_backup_on_client.return_value = self.mock_enable_backup_on_client_fail
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 500)

    @patch('backup.views.NetworkerAPI')
    @patch('backup.views.get_pg_for_retention_time')
    def test_enable_backup_success(self, pg_mock, mock_nw_api):
        pg_mock.return_value = "Bronze-Filesystem15"
        instance_nw = mock_nw_api.return_value
        instance_nw.pick_networker.return_value = mock_get_config(
            "networker_server_details", "NETWORKER_SERVERS")[0]
        instance_nw.check_minion_status.return_value = True
        instance_nw.get_minion_name.return_value = \
            self.mock_get_minion_name_success
        instance_nw.get_fqdn_from_minion_id.return_value = self.mock_get_fqdn_from_minion_id_success
        instance_nw.install_networker_agent.return_value = self.mock_install_networker_agent_success_response
        instance_nw.add_entry_to_host_file.return_value = self.add_dns_entry_success
        instance_nw.add_host_entry_on_minion.return_value = self.add_host_entry_on_minion_success
        instance_nw.enable_backup_on_client.return_value = self.mock_enable_backup_on_client_success
        response = self.client.post(self.enable_backup_url, self.req_data)
        self.assertEqual(response.status_code, 200)

    def test_pause_backup_invalid_data(self):
        req_data = {'VirtualMachineHostName': ''
                    }
        response = self.client.post(self.pause_backup_url, req_data)
        self.assertEqual(response.status_code, 400)
        expected_output = 'This field may not be blank.'
        output = response.json()
        self.assertEqual(expected_output, output['VirtualMachineHostName'][0])

    @patch('backup.views.NetworkerAPI')
    def test_pause_backup_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.pause_vm_backup_service.return_value = self.mock_pause_backup_client_fail
        response = self.client.post(self.pause_backup_url, req_data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(BACKUP_ERRORS["BACKUP017_PAUSE_SERVICE_FAILURE"] in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_pause_backup_fail_404(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.pause_vm_backup_service.return_value = \
            self.mock_pause_backup_client_fail_404
        response = self.client.post(self.pause_backup_url, req_data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(BACKUP_ERRORS["BACKUP017_PAUSE_SERVICE_FAILURE"] in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_pause_backup_fail_with_exception(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.pause_vm_backup_service.side_effect = mock_raise_exception_pause
        response = self.client.post(self.pause_backup_url, req_data)
        expected_output = 'Unexpected error occurred. Please contact administrator.'
        self.assertEqual(response.status_code, 500)
        self.assertTrue(expected_output in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_pause_backup_success(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.pause_vm_backup_service.return_value = self.mock_pause_backup_client_success
        response = self.client.post(self.pause_backup_url, req_data)
        self.assertEqual(response.status_code, 200)

    def test_resume_backup_handle_invalid_data(self):
        req_data = {'VirtualMachineHostName': ''
                    }
        response = self.client.post(self.resume_backup_url, req_data)
        self.assertEqual(response.status_code, 400)
        expected_output = 'This field may not be blank.'
        output = response.json()
        self.assertEqual(expected_output, output['VirtualMachineHostName'][0])

    @patch('backup.views.NetworkerAPI')
    def test_resume_backup_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.resume_vm_backup_service.return_value = self.mock_resume_backup_client_fail
        response = self.client.post(self.resume_backup_url, req_data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(BACKUP_ERRORS["BACKUP018_RESUME_SERVICE_FAILURE"] in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_resume_backup_fail_404(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.resume_vm_backup_service.return_value = self.mock_resume_backup_client_fail_404
        response = self.client.post(self.resume_backup_url, req_data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(BACKUP_ERRORS["BACKUP018_RESUME_SERVICE_FAILURE"] in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_resume_backup_fail_with_exception(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.resume_vm_backup_service.side_effect = mock_raise_exception
        response = self.client.post(self.resume_backup_url, req_data)
        expected_output = 'Unexpected error occurred. Please contact administrator.'
        self.assertEqual(response.status_code, 500)
        self.assertTrue(expected_output in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_resume_backup_success(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.resume_vm_backup_service.return_value = self.mock_resume_backup_client_success
        response = self.client.post(self.resume_backup_url, req_data)
        self.assertEqual(response.status_code, 200)

    def test_disable_backup_handle_invalid_data(self):
        req_data = {'VirtualMachineHostName': ''}
        response = self.client.post(self.disable_backup_url, req_data)
        self.assertEqual(response.status_code, 400)
        expected_output = 'This field may not be blank.'
        output = response.json()
        self.assertEqual(expected_output, output['VirtualMachineHostName'][0])

    @patch('backup.views.NetworkerAPI')
    def test_disable_backup_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.disable_vm_backup_service.return_value = self.mock_disable_backup_client_fail
        response = self.client.post(self.disable_backup_url, req_data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(BACKUP_ERRORS["BACKUP019_DISABLE_SERVICE_FAILURE"] in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_disable_backup_fail_404(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.disable_vm_backup_service.return_value = self.mock_disable_backup_client_fail_404
        response = self.client.post(self.disable_backup_url, req_data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(BACKUP_ERRORS["BACKUP019_DISABLE_SERVICE_FAILURE"] in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_disable_backup_fail_with_exception(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.disable_vm_backup_service.side_effect = mock_raise_exception
        response = self.client.post(self.disable_backup_url, req_data)
        expected_output = 'Unexpected error occurred. Please contact administrator.'
        self.assertEqual(response.status_code, 500)
        self.assertTrue(expected_output in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_disable_backup_success(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.disable_vm_backup_service.return_value = self.mock_disable_backup_client_success
        response = self.client.post(self.disable_backup_url, req_data)
        self.assertEqual(response.status_code, 200)

    def test_decommission_backup_handle_invalid_data(self):
        req_data = {'VirtualMachineHostName': ''}
        response = self.client.post(self.decommission_backup_url, req_data)
        self.assertEqual(response.status_code, 400)
        expected_output = 'This field may not be blank.'
        output = response.json()
        self.assertEqual(expected_output, output['VirtualMachineHostName'][0])

    @patch('backup.views.NetworkerAPI')
    def test_decommission_backup_fail(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.decommission_vm_backup_service.return_value = self.mock_decommission_backup_client_fail
        response = self.client.post(self.decommission_backup_url, req_data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(BACKUP_ERRORS["BACKUP020_DECOMMISSION_SERVICE_FAILURE"] in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_decommission_backup_fail_404(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.decommission_vm_backup_service.return_value = \
            self.mock_decommission_backup_client_fail_404
        response = self.client.post(self.decommission_backup_url, req_data)
        self.assertEqual(response.status_code, 500)
        self.assertTrue(BACKUP_ERRORS["BACKUP020_DECOMMISSION_SERVICE_FAILURE"] in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_decommission_backup_fail_with_exception(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.decommission_vm_backup_service.side_effect = mock_raise_exception
        response = self.client.post(self.decommission_backup_url, req_data)
        expected_output = 'Unexpected error occurred. Please contact administrator.'
        self.assertEqual(response.status_code, 500)
        self.assertTrue(expected_output in response.json())

    @patch('backup.views.NetworkerAPI')
    def test_decommission_backup_success(self, mock_nw_api):
        instance_nw = mock_nw_api.return_value
        req_data = {"VirtualMachineHostName": "rhel",
                    "VirtualMachineIPAddress": "1.1.2.11",
                    "VirtualMachineID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "VirtualMachineRID": "7a035d02-150a-4545-8dba-4cc696ed3394",
                    "TaskID": "7a035d02-150a-4545-8dba-4cc696ed3394"
                    }
        instance_nw.decommission_vm_backup_service.return_value = self.mock_decommission_backup_client_success
        response = self.client.post(self.decommission_backup_url, req_data)
        self.assertEqual(response.status_code, 200)
