import requests
from requests.auth import HTTPBasicAuth
import json
from common.constants import REQUEST_TIMEOUT
from common.functions import get_config

class RestApiTemplate:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url.rstrip('/')

    def send_request(self, request_type, uri, body):
        """
        :param request_type:
        :param uri:
        :param body:
        :return: returns the response of the API Call OR the error in a structured format
        """
        requests.packages.urllib3.disable_warnings()
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        response = {}
        timeout = get_config(REQUEST_TIMEOUT,"timeout")
        try:
            if request_type == 'GET':
                response = requests.get(self.url + uri, auth=HTTPBasicAuth(self.username, self.password),
                                        headers=headers, verify=False, timeout=timeout)
                response.raise_for_status()
                return response.json()
            elif request_type == 'POST':
                body = json.dumps(body)
                response = requests.post(self.url + uri, auth=HTTPBasicAuth(self.username, self.password),
                                         data=body, headers=headers, verify=False, timeout=timeout)
                response.raise_for_status()
            elif request_type == 'PUT':
                body = json.dumps(body)
                response = requests.put(self.url + uri, auth=HTTPBasicAuth(self.username, self.password),
                                        data=body, headers=headers, verify=False, timeout=timeout)
                response.raise_for_status()
            elif request_type == 'DELETE':
                response = requests.delete(self.url + uri, auth=HTTPBasicAuth(self.username, self.password),
                                           headers=headers, verify=False, timeout=timeout)
                response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            response = {"error_code": e.response.json()["status"]["code"],
                        "error_message": e.response.json()["message"]}
            return response
        except requests.exceptions.Timeout as e:
            response = {"error_code": "connection-timeout", "error_message":
                        "Connection Timeout occurred, Please Check whether Backup Server is running"
                        " and details are correct"}
            return response
        except requests.exceptions.TooManyRedirects as e:
            response = {"error_code": "too-many-redirects", "error_message":
                        "Too many redirects. Please try after some time"}
            return response
        except requests.exceptions.ConnectionError as e:
            response = {"error_code": "ConnectionError", "error_message":
                        "Connection Error Occurred, Please Check Backup Server details"}
            return response
        except requests.exceptions.RequestException as e:
            response = {"error_code": "generic-request-error", "error_message": e}
            return response
        return response
