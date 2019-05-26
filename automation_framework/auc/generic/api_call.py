from conf.restConstants import JSON_HEADER, REST_TIMEOUT
from robot.api import logger
from utils.preprocess_robot_input import preprocess_kwargs
import requests
from requests.auth import HTTPBasicAuth
import json


class ExecuteAPICall:
    """
    The Generic Class for ALl API call and related helper function needs in the ROBOT File.
    In future it will be extended to support Other authentication mechanisms. Currently it
    supports basic only.
    """
    def api_call(self, **kwargs):
        """
        :param kwargs: The value of every entry in kwargs can be Any of the Python Datatypes
        and also Functions (Need to be defined in  auc/generic/functions/)

        Example: We can pass a dictionary or a function in 'body'
                 {'a': 'b'}    OR    function:function_name  ('function:' prefix needs to be used)

        Args:
            url: Complete URL Of the API call
            auth: Basic or None
            usr: Username for Basic Auth
            pwd: Password for Basic Auth
            rtype: Can be GET, POST, PUT or DELETE
            body: In case of POST or PUT, Dictionary should be passed

        :return: Python Requests.response Object
        """

        # Pre-process Inputs:
        kwargs = preprocess_kwargs(kwargs)

        # Get all parameters
        request_type = kwargs.get('rtype')
        url = kwargs.get('url')
        if 'body' in kwargs.keys():
            body = json.loads(kwargs.get('body'))

        if 'auth' in kwargs.keys() and kwargs.get('auth') == 'basic':
            username = kwargs.get('usr')
            password = kwargs.get('pwd')
            auth = HTTPBasicAuth(username, password)
        else:
            auth = None

        response = {}
        try:
            requests.packages.urllib3.disable_warnings()
            if request_type == 'GET':
                response = requests.get(url, auth=auth,
                                        headers=JSON_HEADER, verify=False,
                                        timeout=REST_TIMEOUT)
                return response.json()
            elif request_type == 'POST':
                body = json.dumps(body)
                response = requests.post(url, auth=auth,
                                         data=body, headers=JSON_HEADER, verify=False,
                                         timeout=REST_TIMEOUT)
                logger.info(response)
            elif request_type == 'PUT':
                body = json.dumps(body)
                response = requests.put(url, auth=auth,
                                        data=body, headers=JSON_HEADER, verify=False,
                                        timeout=REST_TIMEOUT)
            elif request_type == 'DELETE':
                response = requests.delete(url, auth=auth,
                                           headers=JSON_HEADER, verify=False,
                                           timeout=REST_TIMEOUT)
            logger.info('Response Code is ' + str(response.status_code))
        except requests.exceptions.RequestException as e:
            response = {"error_code": "generic-request-error", "error_message": e}
        return response
