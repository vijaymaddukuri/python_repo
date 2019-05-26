from common.exceptions import APIException
from common.functions import get_config
from common.constants import REQUEST_TIMEOUT
from functools import reduce
import logging
import requests
import operator
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = logging.getLogger(__name__)

class RestClient(object):
    """ Utility class. """

    @staticmethod
    def getFromDict(dataDict, path_list):
        """
        :param dataDict: dictionary to parse.
        :param path_list: path from root to the desired node.
        :return: return value at the end of the path_list.
        """
        return reduce(operator.getitem, path_list, dataDict)

    @staticmethod
    def get_url(ip, port, endpoint):
        """
        :param ip: ip.
        :param port: port.
        :param endpoint: endpoint.
        :return: url.
        """
        return "http://{}:{}/{}".format(ip, port, endpoint)

    @staticmethod
    def get_https_url(ip, port, endpoint):
        """
        :param ip: ip.
        :param port: port.
        :param endpoint: endpoint.
        :return: url.
        """
        return "https://{}:{}/{}".format(ip, port, endpoint)

    @staticmethod
    def result_success(result):
        """
        Check if HTTP result code is in the 2xx range.
        :param result: status code.
        :return: Boolean True or False.
        """

        if 200 <= result < 300:
            return True

        return False

    @staticmethod
    def post_form(url, headers, payload):
        """
        Post form data, which will be encoded as application/x-www-form-urlencoded
        :param url: url to make a post request.
        :param headers: request headers.
        :param payload: data.
        :return: response object.
        """

        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        return RestClient.make_post_request(url, headers=headers, data=payload)

    @staticmethod
    def post_JSON(url, headers, payload):
        """
        Post data as JSON
        :param url: url to make a post request.
        :param headers: request headers.
        :param payload: data.
        :return: response object.
        """

        headers['Content-Type'] = 'application/json'

        return RestClient.make_post_request(url,
                                       headers=headers,
                                       json_data=payload)

    @staticmethod
    def make_post_request(url, headers=None, json_data=None, data=None):
        """
        Make a POST request to a given url. This takes either JSON, raw
        form data.
        :param url: url to make a post request.
        :param headers: request headers.
        :param json_data: json post request data.
        :param data: form post request data.
        :return: response object.
        """
        logger.info("Inside: make_post_request")
        logger.debug("make_post_request: parameters - {}, {}, {}, {}".format(url, headers, json_data, data))

        timeout = get_config(REQUEST_TIMEOUT,"timeout")

        if not headers:
            headers = {}

        if json_data:
            resp = requests.post(url, verify=False, headers=headers, json=json_data, timeout=timeout)
        elif data:
            resp = requests.post(url, verify=False, headers=headers, data=data, timeout=timeout)

        logger.debug('received status : {}'.format(resp.status_code))
        logger.debug('received text   : {}'.format(resp.text))
        logger.info("Exit: make_post_request")
        if RestClient.result_success(resp.status_code):
            return resp
        else:
            err_msg = 'ERROR, received {} code during API call {}'.format(resp.status_code, url)
            logger.error(err_msg)
            raise APIException(err_msg, resp.text)

    @staticmethod
    def make_get_request(url, headers=None):
        """
        Make a GET request to a given url.
        :param url: url to make a post request.
        :param headers: request headers.
        :return: response object.
        """
        logger.info("Inside: make_get_request")
        logger.debug("make_get_request: parameters - {}, {}".format(url, headers))

        timeout = get_config(REQUEST_TIMEOUT,"timeout")

        if not headers:
            headers = {}

        resp = requests.get(url, verify=False, headers=headers, timeout=timeout)

        logger.debug('received status : {}'.format(resp.status_code))
        logger.debug('received text   : {}'.format(resp.text))
        logger.info("Exit: make_get_request")

        if RestClient.result_success(resp.status_code):
            return resp
        else:
            err_msg = 'ERROR, received {} code during API call {}'.format(resp.status_code, url)
            logger.error(err_msg)
            raise APIException(err_msg, resp.text)

    @staticmethod
    def make_delete_request(url, headers=None):
        logger.info("Inside: make_delete_request")
        logger.debug("make_delete_request: parameters - {}, {}".format(url, headers))

        timeout = get_config(REQUEST_TIMEOUT,"timeout")

        if not headers:
            headers = {}

        resp = requests.delete(url, verify=False, headers=headers, timeout=timeout)

        logger.debug('received status : {}'.format(resp.status_code))
        logger.debug('received text   : {}'.format(resp.text))
        logger.info('Exit: make_delete_request')

        if RestClient.result_success(resp.status_code):
            return resp
        else:
            err_msg = 'ERROR, received {} code during API call {}'.format(resp.status_code, url)
            logger.error(err_msg)
            raise APIException(err_msg, resp.text)
