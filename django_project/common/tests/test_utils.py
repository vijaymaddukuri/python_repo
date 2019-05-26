from common.utils import RestClient
from mock import patch,MagicMock
import unittest
from common.exceptions import APIException

def mock_get_config(key, attribute):
    data_dict = {"request_timeout_details": {"timeout": 30},
                 }

    return data_dict[key][attribute]

class TestRestClient(unittest.TestCase):

    def test_getFromDict(self):
        dataDict = {
                    "a":{
                        "r": 1,
                        "s": 2,
                        "t": 3
                        },
                    "b":{
                        "u": 1,
                        "v": {
                            "x": 1,
                            "y": 2,
                            "z": 3
                        },
                        "w": 3
                        }
                   }
        result = RestClient.getFromDict(dataDict, ["a", "r"])
        self.assertEqual(result, 1)

        expected_output = {
                           "x": 1,
                           "y": 2,
                           "z": 3
                          }
        result = RestClient.getFromDict(dataDict, ["b", "v"])
        self.assertEqual(result, expected_output)

    def test_get_http_url(self):
        result = RestClient.get_url('1.1.1.1', '123', 'test')
        expected_output = 'http://1.1.1.1:123/test'
        self.assertEqual(result, expected_output)

    def test_get_https_url(self):
        result = RestClient.get_https_url('1.1.1.1', '123', 'test')
        expected_output = 'https://1.1.1.1:123/test'
        self.assertEqual(result, expected_output)

    def test_result_success_200(self):
        result = RestClient.result_success(200)
        self.assertTrue(result)

    def test_result_success_400(self):
        result = RestClient.result_success(400)
        self.assertFalse(result)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_make_post_json_postive(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {'computers':[{'hostName': 'test.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        mock_requests.post.return_value = response_instance

        result = RestClient.make_post_request('url', json_data={'test': 'test'})
        self.assertEqual(result.status_code, 200)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_make_post_data_postive(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {'computers':[{'hostName': 'test.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        mock_requests.post.return_value = response_instance

        result = RestClient.make_post_request('url', data={'test': 'test'})
        self.assertEqual(result.status_code, 200)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_make_post_data_exception(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {}
        response_instance = MagicMock()
        response_instance.status_code = 400
        expected_msg = "Unauthorized access"
        response_instance.text = "Unauthorized access"
        response_instance.json.return_value = output
        mock_requests.post.return_value = response_instance
        try:
            result = RestClient.make_post_request('url', data={'test': 'test'})
        except APIException as e:
            self.assertEqual(e.received_message, expected_msg)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_post_json(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {'computers':[{'hostName': 'test.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        mock_requests.post.return_value = response_instance

        result = RestClient.post_JSON('url', {'accept':''}, {'test': 'test'})
        self.assertEqual(result.status_code, 200)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_post_form(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {'computers':[{'hostName': 'test.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        mock_requests.post.return_value = response_instance

        result = RestClient.post_form('url', {'accept':''}, {'test': 'test'})
        self.assertEqual(result.status_code, 200)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_make_get_postive(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {'computers':[{'hostName': 'test.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        mock_requests.get.return_value = response_instance

        result = RestClient.make_get_request('url')
        self.assertEqual(result.status_code, 200)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_make_get_exception(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {}
        response_instance = MagicMock()
        response_instance.status_code = 400
        expected_msg = "Unauthorized access"
        response_instance.text = "Unauthorized access"
        response_instance.json.return_value = output
        mock_requests.get.return_value = response_instance
        try:
            result = RestClient.make_get_request('url')
        except APIException as e:
            self.assertEqual(e.received_message, expected_msg)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_make_delete_postive(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {'computers':[{'hostName': 'test.xd'}]}
        response_instance = MagicMock()
        response_instance.status_code = 200
        response_instance.json.return_value = output
        mock_requests.delete.return_value = response_instance

        result = RestClient.make_delete_request('url')
        self.assertEqual(result.status_code, 200)

    @patch('common.utils.requests')
    @patch('common.utils.get_config')
    def test_make_delete_exception(self, mock_config, mock_requests):
        mock_config.side_effect = mock_get_config

        output = {}
        response_instance = MagicMock()
        response_instance.status_code = 400
        expected_msg = "Unauthorized access"
        response_instance.text = "Unauthorized access"
        response_instance.json.return_value = output
        mock_requests.delete.return_value = response_instance
        try:
            result = RestClient.make_delete_request('url')
        except APIException as e:
            self.assertEqual(e.received_message, expected_msg)
