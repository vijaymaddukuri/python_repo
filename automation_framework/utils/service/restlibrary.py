from requests.sessions import Session
from robot.api import logger
from conf.restConstants import *
import yaml

class RestLib(Session):
    """
        Library for REST API Calls
    """

    def get(self, url, **kwargs):
        """Sends a GET request. Returns :class:`Response` object.
        Args:
        :param url: URL for the new :class:`Request` object.
        :param kwargs: Optional arguments that ``request`` takes.
        """

        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """Sends a POST request. Returns :class:`Response` object.
        Args:
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        """

        kwargs.setdefault('timeout', 60)
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        """Sends a PUT request. Returns :class:`Response` object.
        Args:
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param kwargs: Optional arguments that ``request`` takes.
        """

        kwargs.setdefault('timeout', 60)
        return self.request('PUT', url, data=data, **kwargs)

    def get_vmid_by_name(self, hostname, name):
        """
        Description: Get VM ID by Name
        Args:
        :param hostname: Hostname of the server
        :param name: template name
        :return: VM ID or stop the execution
        """
        try:
            logger.info('Begin the testcase to get VM ID')
            url = 'http://{}/{}'.format(hostname, VM_TEMPLATES)
            logger.info('URL is {}'.format(url))
            response = self.get(url)
            logger.info("The status of REST API command is {}".format(response.status_code))
            if not response.ok:
                logger.error('Failed to get the VM templates data with the above REST API')
                return False
            template_list = response.json()
            for template in template_list:
                if template['Name'] == name:
                    logger.info("For the template - {}, the Virtual Machine ID is {}"
                                .format(template['Name'],template['VirtualMachineID']))
                    return template['VirtualMachineID']
            logger.error("From the template list, unable to find the VM {}".format(name))
            return False
        except Exception as err:
            logger.error('Exception while get VM id by name')
            logger.error(err)
            return False

    def get_policy_id_by_name(self, hostname, name):
        """
        Description: Get VIJAY Policy ID by Name
        Args:
        :param hostname: Hostname of the server
        :param name: Name of the policy to fetch ID details
        :return: PolicyID or stop the execution
        """
        try:
            logger.info('Begin the testcase to get VIJAY Policy ID')
            url = 'http://{}/{}'.format(hostname, VIJAY_POLICIES)
            logger.info('URL is {}'.format(url))
            response = self.get(url)
            logger.info("The status of REST API command is {}".format(response.status_code))
            if not response.ok:
                logger.error('Failed to get the VIJAY Policy data with the above REST API')
                return False
            policy_list = response.json()
            for policy in policy_list:
                if policy['name'] == name:
                    logger.info("For the VIJAY Policy  - {}, the VIJAY ID is {}"
                                .format(policy['name'], policy['id']))
                    return policy['id']
            logger.error("From the VIJAY Policy list, unable to find the VIJAY policy {}".format(name))
            return False
        except Exception as err:
            logger.error('Exception while get VIJAY policy id by name')
            logger.error(err)
            return False

    # TODO: change after testing
    def get_yaml_value(self, keyname, param):
        """ This function gives the yaml value corresponding to the parameter
        Args:
            param keyname(string): specify key name
            param param(string): specify the parameter who's value is to be determined
        Returns:
            string: value corresponding to the parameter in yaml file
        """
        with open(YAML_FILE_PATH, 'r') as f:
            doc = yaml.load(f)
        param_value = doc[keyname][param]
        return param_value