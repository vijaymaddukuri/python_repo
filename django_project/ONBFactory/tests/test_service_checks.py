import unittest
from mock import patch
from ONBFactory import service_checks
def mock_get_config(key, attribute):
    data_dict = {"rabbitmq": {"RABBIT_MQ_IP": "localhost",
                              "RABBIT_MQ_USERNAME": "mqadmin",
                              "RABBIT_MQ_PASSWORD": "mqadminpassword"},
                 "deadbolt": {"DEADBOLT_IP": "",
                              "DEADBOLT_PORT": 8080,
                              "DEADBOLT_CLIENT_ID": "",
                              "DEADBOLT_CLIENT_SECRET": ""},
                 "middleware_service_details": {"username": "test",
                                                "password": "test"},
                 "workers": {"no_of_proc": 3}}
    return data_dict[key][attribute]

class TestServiceChecks(unittest.TestCase):

    @patch('ONBFactory.service_checks.subprocess.check_output')
    def test_get_tas_status(self, subprocess_mock):
        subprocess_mock.return_value = b"active"
        result = service_checks.get_tas_status()
        self.assertEqual(result, "active")

    @patch('ONBFactory.service_checks.subprocess.check_output')
    def test_get_tas_processes_status(self, subprocess_mock):
        subprocess_mock.return_value = b"4"
        result = service_checks.get_tas_processes_status()
        self.assertEqual(result, "4")

    @patch('ONBFactory.service_checks.get_config')
    @patch('ONBFactory.service_checks.get_tas_status')
    @patch('ONBFactory.service_checks.get_tas_processes_status')
    def test_get_service_status(self, tas_processes_mock,
                                tas_status_mock,
                                config_mock):
        # All services are up.
        config_mock.side_effect = mock_get_config
        tas_status_mock.return_value = "active"
        tas_processes_mock.return_value = "4"
        result = service_checks.get_service_status()
        self.assertEqual(result[0], True)

        # some services are not up.
        tas_status_mock.return_value = "inactive"
        tas_processes_mock.return_value = "7"
        result = service_checks.get_service_status()
        self.assertEqual(result[0], False)
