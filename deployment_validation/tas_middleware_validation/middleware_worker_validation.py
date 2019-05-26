import argparse
import datetime
import json
import logging as logger
import os
import re
import requests as req
import sys
import time
import yaml

from os.path import dirname, abspath
from common.functions import save_execution_log

current_dir = dirname(dirname(abspath(__file__)))
sys.path.append(current_dir)

from base64 import b64encode
from common.ssh_utility import SSHUtil
from common.functions import (get_config, print_results, check_service, tsa_service_operations, check_rabbitmq_queue)
from config.restConstants import *



yamlpath = '{}/{}'.format(current_dir, 'config')



class Middleware:
    """
    Validate all Middleware API's
    """

    def __init__(self, config_file_path=yamlpath):
        self.yaml_file_path = os.path.join(config_file_path, 'config.yaml')
        self.mw_ip = get_config('MW_DETAILS', 'MW_IP', self.yaml_file_path)
        self.mw_user = get_config('MW_DETAILS', 'MW_USER', self.yaml_file_path)
        self.mw_pwd = get_config('MW_DETAILS', 'MW_PWD', self.yaml_file_path)
        self.tenant_id = get_config('TENANT_ID', None, self.yaml_file_path)
        self.vmid = get_config('VM_DETAILS', 'VMID', self.yaml_file_path)
        self.vm_hostname = get_config('VM_DETAILS', 'VMHOSTNAME', self.yaml_file_path)
        self.retention_days = get_config('VM_DETAILS', 'RETENTION_DAYS', self.yaml_file_path)
        self.callback_url = get_config('VM_DETAILS', 'CALLBACKURL', self.yaml_file_path)
        self.linux_policy_id = get_config('VM_DETAILS', 'LINUX_POLICY_ID', self.yaml_file_path)
        self.win_policy_id = get_config('VM_DETAILS', 'WIN_POLICY_ID', self.yaml_file_path)
        self.task_id = get_config('VM_DETAILS', 'TASKID', self.yaml_file_path)
        self.vm_ip = get_config('VM_DETAILS', 'VM_IP', self.yaml_file_path)
        self.swagger_user = get_config('MW_DETAILS', 'SWAGGER_USER', self.yaml_file_path)
        self.swagger_pwd = get_config('MW_DETAILS', 'SWAGGER_PWD', self.yaml_file_path)
        self.mw_header = JSON_HEADER
        self.worker_yaml_file_path = '{}\\{}\\{}'.format(yamlpath, 'worker', 'config_worker.yaml')
        self.mw_yaml_file_path = '{}\\{}\\{}'.format(yamlpath, 'middleware', 'config_mw.yaml')

        userAndPass = '{}:{}'.format(self.swagger_user, self.swagger_pwd)
        convertToBytes = bytes(userAndPass, 'utf-8')
        auth = b64encode(convertToBytes).decode("ascii")
        self.mw_header['Authorization'] = 'Basic %s' % auth

        # Connect to Middlware machine
        self.ssh_obj = SSHUtil(host=self.mw_ip, username=self.mw_user,
                               password=self.mw_pwd, timeout=10)

    def get_mw_worker_config(self):
        """
        Get middleware and worker yaml files from remote machine
        to jump host machine
        """
        logger.info("############################")
        logger.info("Get Worker config.yaml to Jump host machine")
        # Get config.yaml from TAS machine to windows machine
        remote_file_path = '/opt/middleware/worker/config.yaml'

        self.ssh_obj.get_remote_files('config_worker.yaml', remote_file_path,
                                      self.worker_yaml_file_path, multiple_files=False)
        logger.info("Successfully imported the worker config.yaml to Jump host machine")

        logger.info("############################")
        logger.info("Get Middleware config.yaml to Jump host machine")
        # Get config.yaml from TAS machine to windows machine
        remote_file_path = '/opt/middleware/middleware_service/config.yaml'

        self.ssh_obj.get_remote_files('config_mw.yaml', remote_file_path,
                                      self.mw_yaml_file_path,
                                      multiple_files=False)
        logger.info("Successfully imported the Middleware config.yaml to Jump host machine")

    def upload_yaml_files(self, service=None):
        """
        Uploads Yaml files to Middleware VM
        :return:
        """

        present_dir = r'{}'.format(current_dir)
        present_dir = present_dir.replace('\\', '/')

        if service == "middleware" or service is None:
            logger.info('############################')
            logger.info('Uploading Middleware yaml file')
            self.mw_config = get_config('MW_DETAILS', 'MW_CONFIG_YAML_PATH', self.yaml_file_path)
            local_mw_yaml_path = '{}{}'.format(present_dir, '/config/middleware/middleware_config.yaml')
            command = 'cp {} /opt/middleware/middleware_service/backup_config.yaml'\
                .format(self.mw_config)
            self.ssh_obj.execute_command(command)

            # Upload MW config.yaml
            return_data = self.ssh_obj.upload_file(local_mw_yaml_path, self.mw_config)
            if return_data['status']:
                logger.info('Successfully uploaded MW config.yaml file')

        if service == "worker" or service is None:
            logger.info('############################')
            logger.info('Uploading Worker yaml file')
            self.worker_config = get_config('MW_DETAILS', 'WORKER_CONFIG_YAML_PATH', self.yaml_file_path)
            local_worker_yaml_path = '{}{}'.format(present_dir, '/config/worker/worker_config.yaml')
            command = 'cp {} /opt/middleware/worker/backup_config.yaml'\
                .format(self.worker_config)
            self.ssh_obj.execute_command(command)
            # Upload Worker config.yaml
            return_data = self.ssh_obj.upload_file(local_worker_yaml_path, self.worker_config)
            if return_data['status']:
                logger.info('Successfully uploaded Worker config.yaml file')

    def check_services(self):
        """
        Check the Middleware and Backup workerservices
        :return:
        """
        logger.info('############################')
        logger.info("Checking MW service")
        mw_service_result = "PASS"
        # Check the Middleware service status
        result = check_service(self.ssh_obj, 'mws.service', login=False)

        if '(running)' in result['output']:
            logger.info("Middleware is up and running")
        else:
            logger.error("Middleware service is not running")
            logger.debug("Middleware service is not running")
            logger.debug(result['output'])
            raise Exception("Middleware service is not running")

        logger.info('############################')
        logger.info("Checking worker service")
        worker_service_result = "PASS"
        # Check the Worker service status
        result = check_service(self.ssh_obj, 'bws.service', login=False)

        if '(running)' in result['output']:
            logger.info("Backup Worker is up and running")
        else:
            message = "Backup Worker service is not running"
            logger.error(message)
            logger.debug(message)
            logger.debug(result['output'])
            raise Exception("Backup Worker service is not running")
        return mw_service_result, worker_service_result

    def execute_middleware_health_check(self):
        """
        Function to check the health for a given VM.
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        logger.info('############################')
        logger.info("Validating MW Health check API")
        mw_health_result = "PASS"
        try:
            health_check_resp = req.get(MIDDLEWARE_API_HEALTH_CHECK.format(self.mw_ip),
                                        headers=self.mw_header)
        except Exception as e:
            logger.info("Exception occurred while calling  health_check API. \n "
                        "health_check did not happen.\nException: %s" % e)
            return 0

        logger.info("Status Code = %s" % health_check_resp.status_code)
        logger.info("Message = %s" % health_check_resp.text)
        if health_check_resp.status_code != 200:
            message = 'Middleware health check is failed', \
                      health_check_resp.status_code
            logger.error(message)
            logger.debug(message)
            raise Exception(message)
        else:
            logger.info('Middleware health check is fine')
        return mw_health_result

    def execute_middleware_enable_backup(self):
        """
        Function to enable the filesystem backup for a given VM.
        Args:
        tenant_id (mandatory): String	tenant  uuid in xstream
        vm_id (mandatory): String    vm uuid in xstream
        hostname (mandatory): String  hostname of the vm
        retention_days (mandatory): Int   no. of retention days
        callback_url (mandatory): String
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        logger.info('############################')
        logger.info("Validating MW enable backup API")
        backup_result = "PASS"
        enable_backup_data = {'TenantID': self.tenant_id,
                              'VirtualMachineID': self.vmid,
                              'VirtualMachineHostName': self.vm_hostname,
                              'RetentionDays': self.retention_days,
                              'Callback': self.callback_url
                              }
        try:
            enable_backup_resp = req.post(MIDDLEWARE_API_ENABLE_BACKUP.format(self.mw_ip),
                                          json=enable_backup_data,
                                          headers=self.mw_header)
        except Exception as e:
            logger.info("Exception occurred while calling Enable Backup API. \n "
                        "Backup enabling did not happen.\nException: %s" % e)
            return 0

        logger.info("Status Code = %s" % enable_backup_resp.status_code)
        logger.info("Message = %s" % enable_backup_resp.text)
        if enable_backup_resp.status_code != 200:
            message = 'Could not access middleware enable backup API.', \
                      enable_backup_resp.status_code
            logger.error(message)
            logger.debug(message)
            backup_result = "FAIL"
        else:
            logger.info('Can access middleware enable backup API. '
                        'Response code = 200')

        if enable_backup_resp.status_code == 200:
            # Validating the worker log
            logger.info('Waiting for enable backup API to process the request')
            time.sleep(50)
            command = 'tail -n 210 /var/log/middleware/worker.log'
            result = self.ssh_obj.execute_command(command)

            cdate = datetime.datetime.now().strftime("%d/%b/%Y")
            matchObj = re.findall("{}\s\d+\:\d+\:\d+\]\s+ERROR \[\S+\:\d+\] \|\*BACKUP\*\|"
                                  .format(cdate), result['output'])
            if matchObj:
                message = 'Logging happening in worker log for middleware ' \
                        'enable backup API.'
                logger.debug(message)
                logger.debug(result['output'])
                logger.info(message)
            else:
                logger.info('Enable backup API is Successfully executed')
        else:
            backup_result = "FAIL"
        return backup_result

    def execute_middleware_enable_security(self):
        """
        Function to enable the security for a given VM.
        Args:
        linuxpolicy_id: String
        windowspolicy_id: String
        tenant_id (mandatory): String	tenant  uuid in xstream
        vm_id (mandatory): String    vm uuid in xstream
        hostname (mandatory): String  hostname of the vm
        vm_ip (mandatory): String
        task_id (mandatory): String
        callback_url (mandatory): String
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        logger.info('############################')
        logger.info("Validating MW enable security API")
        sercurity_result = "PASS"
        enable_security_data = {'LinuxPolicyID': self.linux_policy_id,
                                'WindowsPolicyID': self.win_policy_id,
                                'TenantID': self.tenant_id,
                                'VirtualMachineID': self.vmid,
                                'VirtualMachineHostName': self.vm_hostname,
                                'VirtualMachineIPAddress': self.vm_ip,
                                'TaskID': self.task_id,
                                'Callback': self.callback_url
                                }
        try:
            enable_security_resp = req.post(MIDDLEWARE_API_ENABLE_SECURITY.format(self.mw_ip),
                                          json=enable_security_data,
                                          headers=self.mw_header)
        except Exception as e:
            logger.info("Exception occurred while calling Enable security API. \n "
                        "Security enabling did not happen.\nException: %s" % e)
            return 0

        logger.info("Status Code = %s" % enable_security_resp.status_code)
        logger.info("Message = %s" % enable_security_resp.text)
        if enable_security_resp.status_code != 200:
            message = 'Could not access middleware security API', \
                      enable_security_resp.status_code
            logger.error(message)
            logger.debug(message)
            sercurity_result = "FAIL"
        else:
            logger.info('Can access middleware security API. '
                        'Response code = 200')

        # Validating the worker log
        if enable_security_resp.status_code == 200:
            logger.info('Waiting for enable security API to process the request')
            time.sleep(60)
            command = 'tail -n 210 /var/log/middleware/worker.log'
            result = self.ssh_obj.execute_command(command)
            cdate = datetime.datetime.now().strftime("%d/%b/%Y")
            matchObj = re.findall("{}\s\d+\:\d+\:\d+\]\s+ERROR \[\S+\:\d+\] \|\*SECURITY\*\|"
                                  .format(cdate), result['output'])
            if matchObj:
                message = 'Logging happening in worker log for middleware security API.'
                logger.info(message)
                logger.debug(message)
                logger.debug(result['output'])
            else:
                logger.info('Enable security API log is Successfully executed')

            logger.info('############################')
            logger.info("Validating worker log for Middleware to "
                        "tas connectivity")

            if "No route to host" in result['output']:
                message = 'Middleware to tas connectivity failed'
                logger.error(message)
            else:
                logger.info("Able to connect to tas VM from middleware VM")
        else:
            sercurity_result = "FAIL"
        return sercurity_result

    def execute_middleware_enable_monitoring(self):
        """
        Function to enable the monitoring for a given VM.
        Args:
        tenant_id (mandatory): String	tenant  uuid in xstream
        vm_id (mandatory): String    vm uuid in xstream
        hostname (mandatory): String  hostname of the vm
        vm_ip (mandatory): String
        task_id (mandatory): String
        callback_url (mandatory): String
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        logger.info('############################')
        logger.info("Validating MW enable monitoring API")
        monitoring_result = "PASS"
        enable_monitoring_data = {'TenantID': self.tenant_id,
                                  'VirtualMachineID': self.vmid,
                                  'VirtualMachineHostName': self.vm_hostname,
                                  'VirtualMachineIPAddress': self.vm_ip,
                                  'TaskID': self.task_id,
                                  'Callback': self.callback_url
                                  }
        try:
            enable_monitoring_resp = req.post(MIDDLEWARE_API_ENABLE_MONITORING
                                              .format(self.mw_ip),
                                              json=enable_monitoring_data,
                                              headers=self.mw_header)
        except Exception as e:
            logger.info("Exception occurred while calling Enable monitoring API. \n "
                  "monitoring enabling did not happen.\nException: %s" % e)
            logger.debug("Exception occurred while calling Enable monitoring API. \n "
                  "monitoring enabling did not happen.\nException: %s" % e)
            return 0

        logger.info("Status Code = %s" % enable_monitoring_resp.status_code)
        logger.info("Message = %s" % enable_monitoring_resp.text)
        if enable_monitoring_resp.status_code != 200:
            message = 'Could not access middleware monitoring API', \
                      enable_monitoring_resp.status_code
            logger.error(message)
            logger.debug(message)
            monitoring_result = "FAIL"
        else:
            logger.info('Can access middleware monitoring API. '
                        'Response code = 200.')

        if enable_monitoring_resp.status_code == 200:
            # Validating the worker log
            logger.info('Waiting for monitoring API to process the request')
            time.sleep(60)
            command = 'tail -n 210 /var/log/middleware/worker.log'
            result = self.ssh_obj.execute_command(command)

            logger.info("Validating the worker logs")
            cdate = datetime.datetime.now().strftime("%d/%b/%Y")
            matchObj = re.findall("{}\s\d+\:\d+\:\d+\]\s+ERROR \[\S+\:\d+\] \|\*MONITORING\*\|"
                                  .format(cdate), result['output'])
            if matchObj:
                message = 'Logging happening in worker log for ' \
                          'middleware monitoring API.'
                logger.info(message)
                logger.debug(message)
                logger.debug(result['output'])
            else:
                logger.info('Enable monitoring API log is Successfully executed')
        else:
            monitoring_result = "FAIL"
        return monitoring_result

    def execute_middleware_enable_vulnerability(self):
        """
        Function to enable the vulnerability for a given VM.
        Args:
        tenant_id (mandatory): String	tenant  uuid in xstream
        vm_ip (mandatory): String
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        logger.info('############################')
        logger.info("Validating MW enable vulnerability API")
        result_vun = "PASS"
        enable_vulnerability_data = {'TenantID': self.tenant_id,
                                     'VirtualMachineIPAddress': self.vm_ip}
        try:
            enable_vulnerability_resp = req.post(MIDDLEWARE_API_ENABLE_VULNERABILITY
                                                 .format(self.mw_ip),
                                                 json=enable_vulnerability_data,
                                                 headers=self.mw_header)
        except Exception as e:
            logger.info("Exception occurred while calling Enable vulnerability API. \n "
                  "vulnerability enabling did not happen.\nException: %s" % e)
            return "FAIL"

        logger.info("Status Code = %s" % enable_vulnerability_resp.status_code)
        logger.info("Message = %s" % enable_vulnerability_resp.text)
        if enable_vulnerability_resp.status_code != 200:
            message = 'Could not access middleware vulnerability API', enable_vulnerability_resp.status_code
            logger.error(message)
            logger.debug(message)
            raise Exception(message)
        else:
            logger.info('Can access middleware vulnerability API. '
                        'Response code = 200.')

        # Validating the worker log
        logger.info('Waiting for vulnerability scan API to '
                    'process the request')
        time.sleep(30)
        command = 'tail -n 210 /var/log/middleware/worker.log'
        result = self.ssh_obj.execute_command(command)
        logger.info("Validating the worker logs for vulnerability scan")
        cdate = datetime.datetime.now().strftime("%d/%b/%Y")
        matchObj = re.findall("{}\s\d+\:\d+\:\d+\]\s+ERROR \[vulnerability.vscan_server"
                              .format(cdate), result['output'])
        if matchObj:
            message = 'Logging happening in worker log for ' \
                    'middleware vulnerability API.'
            logger.info(message)
            logger.debug(message)
            logger.debug(result['output'])
        else:
            logger.info('Enable vulnerability scan API log is '
                        'Successfully executed')

        return result_vun

    def get_service_ip_from_consul(self):
        """
        This method takes the service name , calls the GET services API
        And returns the corresponding IP for the service.
        :param service_name: service_name to query.
        """
        logger.info("############################")
        logger.info("Verify Consul connectivity from middleware")
        result_consul = "PASS"
        service_name = self.tenant_id
        logger.debug("get_service_ip_from_consul: parameters - {}"
                     .format(service_name))
        ip = get_config('consul', "CONSUL_IP", self.worker_yaml_file_path)
        port = get_config('consul', "CONSUL_PORT", self.worker_yaml_file_path)
        api_get_consul_services = API_CONSUL_SERVICE.format(ip, port)
        command = 'curl {}'.format(api_get_consul_services)
        result = self.ssh_obj.execute_command(command)

        resp_json = json.loads(result['output'])
        consul_lookup_id = None
        for each_id in resp_json:
            if resp_json[each_id]["Service"] == service_name:
                consul_lookup_id = resp_json[each_id]
                break

        if not consul_lookup_id:
            err_msg = "Invalid tenant ID  or tenant not available on consul: {}".format(service_name)
            logger.error(err_msg)
            raise Exception(err_msg)
        else:
            service_ip = consul_lookup_id["Address"]
            service_port = consul_lookup_id["Port"]
            logger.info("Received BB sever IP {}".format(service_ip))
            logger.info("Received BB server port {}".format(service_port))
            logger.info("Successfully connected to consul from Middleware VM")
            return service_ip, service_port, result_consul

    def validate_mw_bb_server_connection(self, server_ip, server_port):
        """
        Validate Middleware to BB server connectivity
        :param server_ip: BB server IP
        :param server_port: BB server Port
        :return:
        """
        logger.info("############################")
        logger.info("Validate Middleware to BB server connectivity")
        result_bb_server = "PASS"
        command = 'curl -k http://{}:{}'.format(server_ip, server_port)
        result = self.ssh_obj.execute_command(command)

        if "HTML for static distribution" in result['output']:
            logger.info('Successfully connected to BB server from middleware VM')
            logger.info("Able to connect to tas VM from middleware VM")
        else:
            logger.error("Unable to connect to BB server from middleware")
            logger.error("Middleware to tas connectivity failed")
            logger.error(result['output'])
            result_bb_server = "FAIL"
        return result_bb_server

    def validate_vulnerability_endpoint(self):
        """
        Validate vulnerability endpoint
        """
        logger.info("############################")
        logger.info("Validate vulnerability endpoint from middleware")
        url = get_config('vulnerability', "VSCAN_SERVER_URL",
                         self.worker_yaml_file_path)
        username = get_config('vulnerability', "VSCAN_SERVER_USERNAME",
                              self.worker_yaml_file_path)
        password = get_config('vulnerability', "VSCAN_SERVER_PASSWORD",
                              self.worker_yaml_file_path)
        API = '{}/{}'.format(url, 'api/3/')
        result_vun = "PASS"
        vul_userAndPass = '{}:{}'.format(username, password)
        convertToBytes = bytes(vul_userAndPass, 'utf-8')
        auth_vun = b64encode(convertToBytes).decode("ascii")
        header = VUNERABILITY_JSON
        header['Authorization'] = 'Basic %s' % auth_vun

        try:
            vulnerability_resp = req.get(API, headers=header, verify=False)
        except Exception as e:
            logger.info("Exception occurred while calling vulnerability API. \n "
                        "\nException: %s" % e)
            return "FAIL"

        logger.info("Status Code = %s" % vulnerability_resp.status_code)
        if vulnerability_resp.status_code != 200:
            message = 'Could not access vulnerability API from middleware.', \
                    vulnerability_resp.status_code
            logger.error(message)
        else:
            logger.info('Can access vulnerability API from middleware. '
                        'Response code = 200')
        return result_vun

    def cleanup(self):
        """
        Clean up the config.yaml
        :return:
        """
        mw_config_yaml_path = '{}\\{}'.format(yamlpath, 'middleware')
        os.chdir(mw_config_yaml_path)
        if os.path.exists('config_mw.yaml'):
            os.remove('config_mw.yaml')

        mw_config_yaml_path = '{}\\{}'.format(yamlpath, 'worker')
        os.chdir(mw_config_yaml_path)
        if os.path.exists('config_worker.yaml'):
            os.remove('config_worker.yaml')

        fname = self.yaml_file_path
        stream = open(fname, 'r')

        data = yaml.load(stream)

        data['MW_DETAILS']['MW_IP'] = ''
        data['MW_DETAILS']['MW_PWD'] = ''
        data['MW_DETAILS']['MW_USER'] = ''
        data['MW_DETAILS']['TAS_IP'] = ''
        data['MW_DETAILS']['SWAGGER_PWD'] = ''
        data['MW_DETAILS']['SWAGGER_USER'] = ''
        data['MW_DETAILS']['TENANT_ID'] = ''

        with open(fname, 'w') as yaml_file:
            yaml_file.write(yaml.dump(data, default_flow_style=False))

        # Close SSH sessions
        self.ssh_obj.close_connections()

    def stop_mw_worker_services(self):
        """
        This function will stop the middleware service and waits the worker to complete
        the existing tasks to complete and stops the worker service as well
        """
        logger.info('############################')
        logger.info("Stop MW service")
        mw_bws_service_result = "FAIL"
        # Check the Middleware service status
        tsa_service_operations(self.ssh_obj, 'mws.service', login=False, operation='stop')
        result = tsa_service_operations(self.ssh_obj, 'mws.service', login=False, operation='status')


        if 'active (running)' not in result['output']:
            logger.info("Middleware service is stopped")
        else:
            logger.error("Middleware service is still running")
            logger.debug("Middleware service is still running")
            logger.debug(result['output'].encode("utf-8"))
            raise Exception("Middleware service is running")

        logger.info('############################')
        logger.info("Check worker queue for active jobs")

        # Wait for 10 mins (max) for worker to complete all the tasks and stop the worker service
        for i in range(60):

            result = check_rabbitmq_queue(self.ssh_obj)
            # Filter the list of tasks in the queue (integers)
            task_list = re.findall('(\d+)', result['output'])
            # Length of the queue should be 1 and that value should be 0
            if len((set(task_list))) == 1 and set(task_list) == {'0'}:

                tsa_service_operations(self.ssh_obj, 'bws.service', login=False, operation='stop')
                result = tsa_service_operations(self.ssh_obj, 'bws.service', login=False, operation='status')
                if 'active (running)' not in result['output']:
                    logger.info("Worker service is stopped, TSA upgrade can be started")
                    mw_bws_service_result = "PASS"
                else:
                    logger.error("Worker service is still running")
                    logger.debug("Worker service is still running")
                    logger.debug(result['output'])
                    raise Exception("Worker service is running")
                break
            else:
                time.sleep(10)
        return mw_bws_service_result

def perfrom_middlewre_enpoint_validation():
    result_dict = {}
    mwObj = Middleware()
    mwObj.get_mw_worker_config()
    result_dict['MIDDLEWARE_SERVICE'],  result_dict['WORKER_SERVICE'] = mwObj.check_services()
    result_dict['MIDDLEWARE_HEALTH_CHECK'] = mwObj.execute_middleware_health_check()
    bb_ip, port, result_dict['CONSUL_CONNECTIVITY'] = mwObj.get_service_ip_from_consul()
    result_dict['BRIDGEBURNER_CONNECTIVITY'] = mwObj.validate_mw_bb_server_connection(bb_ip, port)
    result_dict['VULNERABILITY_CONNECTIVITY'] = mwObj.validate_vulnerability_endpoint()
    print_results(result_dict)
    mwObj.cleanup()


if __name__ == '__main__':
    save_execution_log('mw_consloe')
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', "--allapi",
                        action='store_true', help="To run all available MW APIs")
    parser.add_argument('-y', "--uploadyaml",
                        action='store_true', help="To upload middleware and worker yaml files to MW vm")
    parser.add_argument('-b', "--backupapi",
                        action='store_true', help="To run MW backup API")
    parser.add_argument('-s', "--securityapi",
                        action='store_true', help="To run MW security API")
    parser.add_argument('-m', "--monitoringapi",
                        action='store_true', help="To run MW monitoring API")
    parser.add_argument('-v', "--vulnerabilityapi",
                        action='store_true', help="To run MW vulnerability API")
    parser.add_argument('-stop_services', "--stop_mw_worker_service",
                        action='store_true', help="To stop both MW and worker service")
    args = parser.parse_args()
    result_dict = {}
    mwObj = Middleware()
    if args.uploadyaml:
        mwObj.upload_yaml_files()
    mwObj.get_mw_worker_config()
    result_dict['MIDDLEWARE_SERVICE'],  result_dict['WORKER_SERVICE'] = mwObj.check_services()
    result_dict['MIDDLEWARE_HEALTH_CHECK'] = mwObj.execute_middleware_health_check()
    bb_ip, port, result_dict['CONSUL_CONNECTIVITY'] = mwObj.get_service_ip_from_consul()
    result_dict['BRIDGEBURNER_CONNECTIVITY'] = mwObj.validate_mw_bb_server_connection(bb_ip, port)
    result_dict['VULNERABILITY_CONNECTIVITY'] = mwObj.validate_vulnerability_endpoint()
    if args.allapi:
        result_dict['MW_SECURITY_API'] = mwObj.execute_middleware_enable_security()
        result_dict['MW_VULNERABILITY_API'] = mwObj.execute_middleware_enable_vulnerability()
        result_dict['MW_BACKUP_API'] = mwObj.execute_middleware_enable_backup()
        result_dict['MW_MONITORING_API'] = mwObj.execute_middleware_enable_monitoring()
    if args.backupapi:
        result_dict['MW_BACKUP_API'] = mwObj.execute_middleware_enable_backup()
    if args.monitoringapi:
        result_dict['MW_MONITORING_API'] = mwObj.execute_middleware_enable_monitoring()
    if args.securityapi:
        result_dict['MW_SECURITY_API'] = mwObj.execute_middleware_enable_security()
    if args.vulnerabilityapi:
        result_dict['MW_VULNERABILITY_API'] = mwObj.execute_middleware_enable_vulnerability()

    if args.stop_mw_worker_service:
        result_dict['MW_WORKER_SERVICE'] = mwObj.stop_mw_worker_services()


    print_results(result_dict)
    mwObj.cleanup()