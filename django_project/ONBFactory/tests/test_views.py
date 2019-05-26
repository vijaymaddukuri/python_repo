import unittest
from mock import patch
from mock import MagicMock
from django.test import Client
from django.urls import reverse
import json
from ONBFactory import VERSION

def mock_get_config(key, attribute):
    data_dict = {"nimsoft_server_details": {"NIMSOFT_HUB_USERNAME": "hub_user",
                                            "NIMSOFT_HUB_PASSWORD": "Password",
                                            "NIMSOFT_HUB_IP": "10.100.249.1",
                                            "NIMSOFT_HUB_NAME": "hub_name",
                                            "NIMSOFT_HUB_DOMAIN":"example.com",
                                            "NIMSOFT_HUB_ROBOT_NAME":"robot_name"
                                            
                                           }
               }
    return data_dict[key][attribute]


class TestTas_Healthcheck(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch('ONBFactory.views.get_service_status')
    @patch('ONBFactory.views.logging.Logger.exception')
    def test_health_check(self, exception_mock, service_status_mock):
        # Valid request.
        exception_mock.return_value = None
        service_status_mock.return_value = (True, {"key1": "val1"})
        url = reverse("tas_healthcheck")
        result = self.client.get(url, content_type="application/json")
        self.assertEqual(result.status_code, 200)

        # Invalid request.
        service_status_mock.return_value = (False, {"key1": "val1"})
        result = self.client.get(url, content_type="application/json")
        self.assertEqual(result.status_code, 500)

        # Exception case.
        service_status_mock.side_effect = Exception
        result = self.client.get(url, content_type="application/json")
        self.assertEqual(result.status_code, 500)

class TestTas_Version(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_version(self):
        url = reverse("tas_version")
        result = self.client.get(url, content_type="application/json")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, "v" + VERSION)

class Test_Tas_Configuration_Data(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch('ONBFactory.views.get_config')
    def test_configuration_data_positive(self, mock_config):
        mock_config.side_effect = mock_get_config
        req_data = {
            'params': 'NIMSOFT_HUB_NAME'
         }
        url = reverse("tas_configuration_data")
        result = self.client.get(url, req_data, content_type="application/json")
        self.assertEqual(result.status_code, 200)

    @patch('ONBFactory.views.get_config')
    def test_configuration_data_invalid_query_params(self, mock_config):
        mock_config.side_effect = mock_get_config
        req_data = {
            'params': 'NIMSOFT_HUB_PASSWORD'
         }
        url = reverse("tas_configuration_data")
        result = self.client.get(url, req_data, content_type="application/json")
        tmp = result.content.decode()
        tmp_dict = json.loads(tmp)
        expected_output = 'Key not supported'
        self.assertEqual(result.status_code, 500)
        self.assertEqual(tmp_dict, expected_output)
     
    @patch('ONBFactory.views.get_config')
    def test_configuration_data_no_query_params(self, mock_config):
        mock_config.side_effect = mock_get_config
        req_data = {
            'params': ''
         }
        url = reverse("tas_configuration_data")
        result = self.client.get(url, req_data, content_type="application/json")
        self.assertEqual(result.status_code, 500)

    @patch('ONBFactory.views.get_config')
    def test_configuration_data_when_return_value_null(self,mock_config):
        req_data = {
            'params': 'NIMSOFT_HUB_NAME'
         }
        mock_config.return_value = ''
        url = reverse("tas_configuration_data")
        result = self.client.get(url, req_data, content_type="application/json")
        tmp = result.content.decode()
        tmp_dict = json.loads(tmp)
        expected_output = 'Unable to get the value for the specified paramater'
        self.assertEqual(result.status_code, 404)

 
    @patch('ONBFactory.views.get_config')
    def test_configuration_data_when_exception(self,mock_config):
        mock_config.side_effect = mock_get_config
        req_data = {
            'params': 'NIMSOFT_HUB_NAME'
         }
        mock_config.side_effect = Exception
        url = reverse("tas_configuration_data")
        result = self.client.get(url, req_data, content_type="application/json")
        self.assertEqual(result.status_code, 500)

