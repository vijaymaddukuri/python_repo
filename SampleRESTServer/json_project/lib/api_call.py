import requests
import conf.rest_constants as const
from lib.common import get_json
from requests.auth import HTTPBasicAuth
from os.path import dirname, abspath, join
base_dir = dirname(dirname(abspath(__file__)))


class ExecuteAPICall:
    def api_call(self, request_type, api_suffix, json_file_name):
        """
        This function is a generic REST API Call function
        :param request_type: Type of the request
        :param api_suffix:   The suffix to the Base URL of IONOS API
        :param json_file_name: The name of the JSON Template to be used for the request
        :return: response: The API response
        """
        try:
            requests.packages.urllib3.disable_warnings()
            json_path = join(base_dir, 'json', json_file_name)
            body = get_json(json_path)
            url = const.API_BASE_URL.format(api_suffix)
            basic_auth = HTTPBasicAuth(const.API_USER, const.API_PASSWORD)
            header = const.JSON_HEADER
            if request_type == 'GET':
                response = requests.get(url, auth=basic_auth,
                                        verify=False,
                                        timeout=const.REST_TIMEOUT)
                print(url)
                return response
            elif request_type == 'POST':
                response = requests.post(url, auth=basic_auth,
                                         json=body, headers=header, verify=False,
                                         timeout=const.REST_TIMEOUT)
                print(url)
                return response
            elif request_type == 'PUT':
                response = requests.put(url, auth=basic_auth,
                                        json=body, headers=header, verify=False,
                                        timeout=const.REST_TIMEOUT)
                print(url)
                return response
            elif request_type == 'PATCH':
                response = requests.patch(url, auth=basic_auth, json=body,
                                          headers=header, verify=False,
                                          timeout=const.REST_TIMEOUT)
                print(url)
                return response
            elif request_type == 'DELETE':
                response = requests.delete(url, auth=basic_auth,
                                           verify=False,
                                           timeout=const.REST_TIMEOUT)
                print(url)
                return response
        except requests.exceptions.RequestException as e:
            response = {"error_code": "generic-request-error", "error_message": e}
            return response
