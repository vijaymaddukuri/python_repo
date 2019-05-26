import logging
import requests
import time
from common.constants import SALT_MINION_ERRORS, SALT_MASTER_ERROR, KEY_SALT_RETRY_CONFIG_VALUES
from common import constants as const
from common.functions import (get_config)
from common.exceptions import SALTException

logger = logging.getLogger(__name__)


class SaltNetAPI:
    """
        This class  will connect to Salt Master and will get details of minions and
        add jobs to execute on minions.
    """
    def __init__(self, username=None, password=None, hostname=None, port=None):
        """
        :param username: Username of the VM
        :param password: Password of the VM
        :param hostname: IP address or Hostname
        :param port: SSH port
        """
        if username is not None:
            self.username = username
        else:
            self.username = get_config('salt_master_details', 'MASTER_API_USERNAME')

        if password is not None:
            self.password = password
        else:
            self.password = get_config('salt_master_details', 'MASTER_API_PASSWORD')

        if hostname is not None:
            self.hostname = hostname
        else:
            self.hostname = get_config('salt_master_details', 'MASTER_IP')

        if port is not None:
            self.port = port
        else:
            self.port = get_config('salt_master_details', 'MASTER_API_PORT')
        self.salt_session = None

    def url(self, api_name=""):
        """Creates url for the given input
        :param api_name: name of the api
        :return: http://<hostname>:<port>/<api_name>
        """
        return "http://%s:%s/%s" % (self.hostname, self.port, api_name)

    def login(self):
        """
        Login to the machine with the give username and password
        """
        logger.info("inside login")
        self.salt_session = requests.Session()
        try:
            response = self.salt_session.post(self.url('login'), json={
                'username': self.username,
                'password': self.password,
                'eauth': 'pam'
            })
            return response
        except requests.ConnectionError as e:
            logger.debug("Connection error -{}".format(e))
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def verify_login(self, login_resp):
        if login_resp is None:
            err_msg = SALT_MASTER_ERROR['SALT001_CONNECTION_ERROR']
            raise SALTException(err_msg, login_resp)
        if not login_resp.ok:
            err_msg = SALT_MASTER_ERROR['SALT002_LOGIN_ERROR']
            raise SALTException(err_msg, login_resp)

    def get_vm_minion_status(self, target, expr_form):
        """
        Get status of the minion from minion hostname/ip
        :param target: Minion hostname or ip
        :return: Status
        """
        return_data = {}
        try:
            return_data['status'] = False
            self.verify_login(self.login())
            resp = self.salt_session.post(self.url(), json=[{
                'client': 'local',
                'tgt': target,
                'fun': 'test.ping',
                'expr_form': expr_form,
                'timeout': 5
            }])
            logger.debug('salt master api request - ' + resp.url)
            response_in_dict = resp.json()
            minion_response = response_in_dict['return'][0]
            for key, status in minion_response.items():
                if status:
                    return_data['status'] = True
                    return return_data
            err_msg = SALT_MASTER_ERROR['SALT004_MINION_NOT_RESPONDING']
            raise SALTException(err_msg, minion_response)
        except (KeyError, IndexError) as e:
            message = SALT_MASTER_ERROR['SALT003_EMPTY_MINION_RESPONSE']
            return_data['comment'] = message
            logger.critical(message)
            return return_data
        except SALTException as e:
            logger.debug(e.error_message)
            return_data['comment'] = e.error_message
            return return_data
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def check_minion_status(self, vm_ip):
        """
        :param vm_ip: IP address of client vm
        :return: True / False
        """
        logger.debug("check_minion_status: parameters : {}  ".format(vm_ip))
        salt_ping_no_of_retries = get_config(KEY_SALT_RETRY_CONFIG_VALUES, "SALT_PING_NO_OF_RETRIES")
        salt_ping_retries_timeout = get_config(KEY_SALT_RETRY_CONFIG_VALUES, "SALT_PING_RETRIES_TIMEOUT")
        status = False
        for limit in range(salt_ping_no_of_retries):
            resp = self.get_vm_minion_status(vm_ip, 'ipcidr')
            logger.debug("minion status : {}".format(resp))
            if resp["status"]:
                logger.info("minion successfully found for ip: {}".format(vm_ip))
                status = True
                break
            logger.info("Retrying for minion status: Attempt {}/{}.".format(limit + 1,
                                                                            salt_ping_no_of_retries))
            time.sleep(salt_ping_retries_timeout)

        return status

    def get_minion_name_from_ip(self, vm_ip):
        """
        Get minion name from ip address
        :param vm_ip: minion ip address
        :return:
        """
        logger.debug("get_minion_name_from_ip: parameters : {} ".format(vm_ip))
        vm_minion_id_resp = self.get_minion_name(vm_ip, 'ipcidr')
        return vm_minion_id_resp

    def get_minion_name(self, target, expr_form):
        """
        Get the minion Name with the IP
        :param target: Minion IP/ hostname
        :param expr_form: value based on hostname or ip
                         'ipcidr': for ip, 'compound' for hostname
        :return: Minion Name
        """
        return_data = {}
        try:
            minion_name = False
            return_data['status'] = False
            # response = self.login()
            self.verify_login(self.login())
            resp = self.salt_session.post(self.url(), json=[{
                'client': 'local',
                'tgt': target,
                'fun': 'grains.get',
                'arg': 'id',
                'expr_form': expr_form
            }])
            logger.debug('salt master api request - ' + resp.url)
            response_in_dict = resp.json()
            minion_response = response_in_dict['return'][0]
            for key, name in minion_response.items():
                if key == name:
                    minion_name = name
            if minion_name is False:
                err_msg = SALT_MASTER_ERROR['SALT004_MINION_NOT_RESPONDING']
                raise SALTException(err_msg, minion_response)
            return_data['status'] = True
            return_data['minion_name'] = minion_name
            return return_data
        except (KeyError, IndexError) as e:
            message = SALT_MASTER_ERROR['SALT003_EMPTY_MINION_RESPONSE']
            return_data['comment'] = message
            logger.critical(message)
            return return_data
        except SALTException as e:
            logger.debug(e.error_message)
            return_data['comment'] = e.error_message
            return return_data
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def get_minion_ip(self, minion_name):
        """
        Get the minion IP Address with the Name
        :param minion_name: Minion Name
        :return: Minion IP Address
        """
        return_data = {}
        try:
            return_data['status'] = False
            response = self.login()
            if response is not None:
                if response.ok:
                    resp = self.salt_session.post(self.url(), json=[{
                        'client': 'local',
                        'tgt': minion_name,
                        'fun': 'grains.get',
                        'arg': 'fqdn_ip4'
                    }])
                    logger.debug('salt master api request - '+resp.url)
                    response_in_dict = resp.json()

                    minion_ipaddress = None
                    if 'return' in response_in_dict:
                        minion_response = response_in_dict['return'][0]
                        if minion_response:
                            ip_values = list(minion_response.values())
                            if len(ip_values) > 0 and len(ip_values[0]) > 0:
                                minion_ipaddress = ip_values[0][0]

                    if minion_ipaddress is not None:
                        return_data['status'] = True
                        return_data['minion_ipaddress'] = minion_ipaddress
                        return return_data
                    else:
                        message = "Unable to fetch the Minion IP, response return object is empty"
                        logger.debug(resp.json())
                        logger.critical(message)
                        return_data['comment'] = message
                        return return_data
                else:
                    message = 'Unable to login to the salt master ' \
                              'machine with the given username and password'
                    logger.debug(message)
                    return_data['comment'] = message
                    return return_data
            else:
                message = 'Unable to establish connection with the salt master machine. ' \
                          'Please ensure the machine is up and Salt Master/Salt NetApi services are running.'
                logger.debug(message)
                return_data['comment'] = message
                return return_data
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def get_fqdn_from_minion_id(self, minion_id):
        """Get the FQDN Name from minion hostname
        :param minion_id: Minion id
        :return: Minion FQDN Name
        """
        return_data = {}
        try:
            fqdn_name = False
            return_data['status'] = False
            response = self.login()
            if response is None or not response.ok:
                message = 'Unable to establish connection with the salt master machine. ' \
                          'Please ensure the machine is up and Salt Master/Salt NetApi services are running.'
                logger.debug(message)
                return_data['comment'] = message
                return return_data

            resp = self.salt_session.post(self.url(), json=[{
                'client': 'local',
                'tgt': minion_id,
                'fun': 'grains.item',
                'arg': 'fqdn'
            }])
            logger.debug('salt master api request - ' + resp.url)
            response_in_dict = resp.json()
            if 'return' not in response_in_dict or len(response_in_dict['return']) <= 0:
                message = "Response is not in proper format."
                logger.critical(message)
                return_data['comment'] = message
                return return_data

            minion_response = response_in_dict['return'][0]
            if isinstance(minion_response, dict) and isinstance(minion_response[minion_id], dict) and \
                    'fqdn' in minion_response[minion_id]:
                fqdn_name = minion_response[minion_id]['fqdn']
            if fqdn_name is False:
                message = "Unable to fetch the FQDN, response return object is empty"
                logger.critical(message)
                return_data['comment'] = message
                return return_data

            return_data['status'] = True
            return_data['fqdn'] = fqdn_name
            return return_data
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def get_os_kernel_from_minion_id(self, minion_id):
        """Get the OS Name from minion hostname
        :param minion_id: Minion id
        :return: Minion os Name
        """
        try:
            kernel_name = False
            response = self.login()
            if response is None or not response.ok:
                err_msg = SALT_MINION_ERRORS['LOGIN']
                logger.debug(err_msg)
                raise SALTException(err_msg, response)

            resp = self.salt_session.post(self.url(), json=[{
                'client': 'local',
                'tgt': minion_id,
                'fun': 'grains.item',
                'arg': 'kernel'
            }])
            logger.debug('salt master api request - ' + resp.url)
            response_in_dict = resp.json()
            if 'return' not in response_in_dict or len(response_in_dict['return']) <= 0:
                err_msg = SALT_MASTER_ERROR['SALT003_EMPTY_MINION_RESPONSE']
                logger.critical(err_msg)
                raise SALTException(err_msg, response_in_dict)

            minion_response = response_in_dict['return'][0]
            if isinstance(minion_response, dict) and isinstance(minion_response[minion_id], dict) and \
                    'kernel' in minion_response[minion_id]:
                kernel_name = minion_response[minion_id]['kernel']
            if kernel_name is False:
                err_msg = SALT_MINION_ERRORS['FETCH_KERNEL']
                logger.critical(err_msg)
                raise SALTException(err_msg, minion_response[minion_id])

            return kernel_name
        except SALTException as e:
            raise
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def send_grains_and_sync(self, minion_ipaddress, minion_name=None):
        """Upload the grain files to remote machine and sync with salt master
        :param minion_ipaddress:  Minion Ip address
        :param minion_name: optional (Minion Name)
        :return: True
        :expect: Exception when grain not uploads to the minion VM
        """
        return_data = {}
        return_data['status'] = False
        if minion_name is None:
            minion_data = self.get_minion_name(minion_ipaddress, 'ipcidr')
            if minion_data['status'] is False:
                return_data['comment'] = 'Unable to get the minion name'
                return return_data
            minion_name = minion_data['minion_name']
        try:
            response = self.login()
            if response is not None:
                if response.ok:
                    resp = self.salt_session.post(self.url(), json=[{
                        'client': 'local',
                        'tgt': minion_name,
                        'fun': 'state.sls',
                        'arg': 'copygrains'
                    }])
                    logger.debug('salt master api request - ' + resp.url)
                    response_in_dict = resp.json()
                    if 'return' in response_in_dict:
                        minion_response = response_in_dict['return'][0]
                        if minion_response:
                            resp_sync = self.salt_session.post(self.url(), json=[{
                                'client': 'local',
                                'tgt': minion_name,
                                'fun': 'saltutil.sync_all'
                            }])
                            logger.debug('salt master api request - ' + resp_sync.url)
                            response_in_dict = resp_sync.json()
                            if 'return' in response_in_dict:
                                minion_response = response_in_dict['return'][0]
                                if minion_response:
                                    return_data['status'] = True
                                    return return_data
                                else:
                                    message = "syncing of grains file to minion has failed."
                                    logger.critical(message)
                                    return_data['comment'] = message
                                    return return_data
                            else:
                                message = "syncing of grains file to minion has failed."
                                logger.critical(message)
                                return_data['comment'] = message
                                return return_data
                        else:
                            message = "sending grains file to minion has failed."
                            logger.critical(message)
                            return_data['comment'] = message
                            return return_data
                    else:
                        message = "sending grains file to minion has failed."
                        logger.critical(message)
                        return_data['comment'] = message
                        return return_data
                else:
                    message = 'Unable to login to the salt master machine ' \
                              'with the given username and password.'
                    logger.debug(message)
                    return_data['comment'] = message
                    return return_data
            else:
                message = 'Unable to establish connection with the salt master machine. ' \
                          'Please ensure the machine is up and Salt Master/Salt NetApi services are running.'
                logger.debug(message)
                return_data['comment'] = message
                return return_data
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def check_master_minion_connection(self, minion_name):
        """
        Check the minion and master connection
        :param minion_name = Minion Name
        :return: Boolean (True or False)
        """
        return_data = {}
        try:
            return_data['status'] = False
            response = self.login()
            if response is not None:
                if response.ok:
                    resp = self.salt_session.post(self.url(), json=[{
                        'client': 'local',
                        'tgt': minion_name,
                        'fun': 'test.ping',
                    }])
                    logger.debug('salt master api request - ' + resp.url)
                    response_in_dict = resp.json()
                    if 'return' in response_in_dict and minion_name in response_in_dict['return'][0] \
                            and response_in_dict['return'][0][minion_name]:
                        return_data['status'] = True
                        return return_data
                    else:
                        error_message = 'Salt Master and Minion connection establishment failed.'
                else:
                    error_message = 'Unable to login to the salt master ' \
                                    'machine with the given username and password.'
            else:
                error_message = 'Unable to establish connection with the salt master machine. ' \
                                'Please ensure the machine is up and ' \
                                'Salt Master/Salt NetApi services are running.'
            if error_message != '':
                return_data['comment'] = error_message
                logger.error(error_message)
                return return_data

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def execute_command(self, vm_hostname, args=None, pillar_details=None, function='state.apply'):
        """Upload the net api salt command into the Minion from Master VM
                :param vm_hostname: Minion VM Hostname
                :param args: state file location on salt master(optional)
                :param pillar_details: key value arguments required by net api command(optional)
                :param function: function to run by salt net api command(optional)
                :return: JSON response
                :except: Exception when could not perform the function on minion
                """
        logger.info("Inside: execute_command")
        logger.debug("execute_command: parameters -{}, {} ".format(vm_hostname, args))
        execute_command_status = {}
        error_message = ''
        try:
            response = self.login()
            if response is not None:
                if response.ok:
                    minion_status = self.check_master_minion_connection(vm_hostname)
                    if minion_status['status']:
                        resp = self.salt_session.post(self.url(), json=[{
                            'client': 'local',
                            'tgt': vm_hostname,
                            'fun': function,
                            'arg': args,
                            'kwarg': pillar_details,
                        }])
                        logger.debug('salt master api request - ' + resp.url)
                        response_in_dict = resp.json()
                        if 'return' in response_in_dict and vm_hostname in response_in_dict['return'][0] \
                                and response_in_dict['return'][0][vm_hostname]:
                            execute_command_status['status'] = True
                            execute_command_status['comment'] = response_in_dict
                            logger.info("Response for executing net api command-" +
                                        str(execute_command_status['status']))
                        else:
                            error_message = 'Execution of Net API command on the Client VM failed.'
                    else:
                        error_message = 'Unable to connect to the Client VM. Please ensure the ' \
                                        'machine is up, configured with the salt master and ' \
                                        'minion service is running.'
                else:
                    error_message = 'Unable to login to the salt master machine ' \
                                    'with the given username and password.'
            else:
                error_message = 'Unable to establish connection with the salt master machine. ' \
                                'Please ensure the machine is up and ' \
                                'Salt Master/Salt NetApi services are running.'

            if error_message is not '':
                execute_command_status['status'] = False
                execute_command_status['comment'] = error_message
                logger.error(str(execute_command_status))

            logger.info('Exit: execute_command')

            return execute_command_status

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def execute_command_with_minion_ip(self, vm_ipaddress, args=None,
                                       pillar_details=None, function='state.apply'):
        """
        Upload the net api salt command into the Minion from Master VM
        :param vm_ipaddress: Minion VM IP address
        :param args: state file location on salt master(optional)
        :param pillar_details: key value arguments required by net api command(optional)
        :param function: function to run by salt net api command(optional)
        :return: JSON response
        :except: Exception when could not perform the function on minion
        """
        logger.info("Inside: execute_command")
        logger.debug("execute_command: parameters -%s, %s, %s ", vm_ipaddress, args, pillar_details)
        return_data = {}
        return_data['status'] = False
        try:
            minion_name_resp = self.get_minion_name(vm_ipaddress, 'ipcidr')
            if minion_name_resp['status'] is False:
                return minion_name_resp

            if 'minion_name' not in minion_name_resp:
                message = "Unable to fetch the Minion name, response return object is empty"
                logger.critical(message)
                return_data['comment'] = message
                return return_data

            minion_name = minion_name_resp['minion_name']
            nim_api_response = self.execute_command(minion_name, args, pillar_details, function)
            return nim_api_response
        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def sync_modules(self, vm_hostname):

        """Syncs the files on the salt master
            :param vm_hostname: Minion VM Hostname
            :return: True
            :expect: Exception when file is not able to sync
            """
        logger.info("Inside: sync_modules")
        logger.debug("sync_modules: parameters -", vm_hostname)
        sync_module_status = {}
        error_message = ''
        try:
            response = self.login()
            if response is not None:
                if response.ok:
                    minion_status = self.check_master_minion_connection(vm_hostname)
                    if minion_status['status']:
                        resp_sync = self.salt_session.post(self.url(), json=[{
                            'client': 'local',
                            'tgt': vm_hostname,
                            'fun': 'saltutil.sync_all'
                        }])

                        logger.debug('salt master api request - ' + resp_sync.url)
                        response_in_dict = resp_sync.json()
                        if 'return' in response_in_dict and vm_hostname in response_in_dict['return'][0] \
                                and response_in_dict['return'][0][vm_hostname]:
                            sync_module_status['status'] = True
                            sync_module_status['comment'] = response_in_dict
                            logger.info("Response for syncing modules-" +
                                        str(sync_module_status['comment']))
                        else:
                            error_message = const.BACKUP_SERVICE_ERRORS["SYNC_FAILURE"]
                    else:
                        error_message = 'Unable to connect to the Client VM. Please ensure ' \
                                        'the machine is up, configured with the salt master ' \
                                        'and minion service is running.'
                else:
                    error_message = 'Unable to login to the salt master machine ' \
                                    'with the given username and password.'
            else:
                error_message = 'Unable to establish connection with the salt master machine. ' \
                                'Please ensure the machine is up and ' \
                                'Salt Master/Salt NetApi services are running.'
            if error_message is not '':
                sync_module_status['status'] = False
                sync_module_status['comment'] = error_message
                logger.error(str(sync_module_status))

            logger.info('Exit: sync_module')

            return sync_module_status

        except Exception as e:
            message = "Unknown exception - {}".format(e)
            logger.debug(message)
            raise Exception(message)
