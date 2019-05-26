import backup.RestApiTemplate as RestApiTemplate
from requests.exceptions import RequestException
from mock import patch
import unittest
import requests
import mock
import json


class TestRestApiTemplate(unittest.TestCase):

    def setUp(self):
        self.mock_response_get_positive = '<Response [200]>'
        self.mock_response_put_positive = '<Response [204]>'
        self.mock_response_post_positive = '<Response [204]>'
        self.mock_response_delete_positive = '<Response [204]>'
        self.mock_response_get_negative = '<Response [400]>'
        self.mock_response_put_negative = '<Response [500]>'
        self.mock_response_post_negative = '<Response [400]>'
        self.mock_response_delete_negative = '<Response [400]>'
        self.pg = {
                    "comment": "Default protection group for workflow Bronze/Filesystem",
                    "links": [
                        {
                            "href": "https://10.100.249.48:9090/nwrestapi/v2/global/protectiongroups/Bronze-Filesystem",
                            "rel": "item"
                        }
                    ],
                    "name": "Bronze-Filesystem",
                    "resourceId": {
                        "id": "152.0.227.11.0.0.0.0.90.46.88.91.10.100.249.48",
                        "sequence": 17
                    },
                    "workItemQueries": [],
                    "workItemSource": "Static",
                    "workItemSubType": "None",
                    "workItemType": "Client",
                    "workItems": ["47.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48", "47.0.234.6.0.0.0.0.164.48.88.91.10.100.249.48"]
                }                                
        
    @patch('backup.RestApiTemplate.requests.get')
    @patch('backup.RestApiTemplate.requests.put')
    @patch('backup.RestApiTemplate.requests.post')
    @patch('backup.RestApiTemplate.requests.delete')
    def test_send_request(self, mock_delete, mock_post, mock_put, mock_get):
        restapi = RestApiTemplate.RestApiTemplate('username', 'password', 'url')
        
        #GET request successfull
        mock_get.return_value = self._mock_response(json_data = self.pg)
        result = restapi.send_request('GET', 'url', {})
        self.assertEqual(result, self.pg)        
               
        #PUT request successfull
        mock_resp = self._mock_response(status=204)
        mock_put.return_value = mock_resp
        result = restapi.send_request('PUT', 'url', {})
        self.assertEqual(result.status_code, 204)
        
        #POST request successfull
        mock_resp = self._mock_response(status=200)
        mock_post.return_value = mock_resp     
        result = restapi.send_request('POST', 'url', {})
        self.assertEqual(result.status_code, 200)
        
        #DELETE request successfull
        mock_resp = self._mock_response(status=204)
        mock_delete.return_value = mock_resp        
        result = restapi.send_request('DELETE', 'url', {})
        self.assertEqual(result.status_code, 204)
        
        #connection timeout exception check    
        mock_resp = self._mock_response(status=500, raise_for_status=requests.exceptions.Timeout('timeout exception'))
        mock_get.return_value = mock_resp
        result = restapi.send_request('GET', 'url', {})
        expected_output = {"error_code": "connection-timeout", "error_message":
                           "Connection Timeout occurred, Please Check whether Backup Server is running"
                           " and details are correct"}
        self.assertEqual(result, expected_output)
        
        #TooManyRedirects exception check    
        mock_resp = self._mock_response(status=500, raise_for_status=requests.exceptions.TooManyRedirects('timeout exception'))
        mock_get.return_value = mock_resp
        result = restapi.send_request('GET', 'url', {})
        expected_output = {"error_code": "too-many-redirects", "error_message":
                           "Too many redirects. Please try after some time"}
        self.assertEqual(result, expected_output)
        
        #ConnectionException exception check
        mock_resp = self._mock_response(status=500, raise_for_status=requests.exceptions.ConnectionError("Connection Error Occurred, Please Check Backup Server details"))
        mock_get.return_value = mock_resp
        result = restapi.send_request('GET', 'url', {})
        expected_output = {"error_code": "ConnectionError", "error_message":
                        "Connection Error Occurred, Please Check Backup Server details"}
        self.assertEqual(result, expected_output)

    def _mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp      
        
if __name__ == '__main__':
    unittest.main()      
