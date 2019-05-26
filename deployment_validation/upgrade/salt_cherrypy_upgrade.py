import argparse
import datetime
import logging as logger
import os
import sys
import re
import yaml

current_dir = os.getcwd().replace('tas_middleware_validation', '')
sys.path.append(current_dir)

from common.ssh_utility import SSHUtil
from common.functions import (get_config, print_results, check_service, telnet_connectivity, tsa_service_operations)
from config.restConstants import *

logfile = datetime.datetime.now().strftime('tas_console_%H_%M_%d_%m_%Y.log')
logpath = '{}/{}'.format(current_dir, logfile)

yamlpath = '{}\\{}'.format(current_dir, 'config')

logger.basicConfig(level=logger.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=logpath,
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logger.StreamHandler()
console.setLevel(logger.INFO)
formatter = logger.Formatter('%(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logger.getLogger('').addHandler(console)

class SaltCherryPy:
    """
    Validate all SaltCherryPy API's
    """
    def __init__(self, config_file_path=yamlpath):
        self.yaml_file_path = os.path.join(config_file_path, 'config.yaml')
        self.sm_ip = get_config('SM_DETAILS', 'SM_IP', self.yaml_file_path)
        self.sm_user = get_config('SM_DETAILS', 'SM_USER', self.yaml_file_path)
        self.sm_pwd = get_config('SM_DETAILS', 'SM_PWD', self.yaml_file_path)
        self.nat_ip = get_config('NAT_VM', 'SERVER_IP', self.yaml_file_path)
        self.nat_user = get_config('NAT_VM', 'SERVER_USERNAME', self.yaml_file_path)
        self.nat_pwd = get_config('NAT_VM', 'SERVER_PASSWORD', self.yaml_file_path)
        self.nat_tmp_location = get_config('NAT_VM', 'CERTIFICATE_COPY_LOCATION', self.yaml_file_path)

        # Connect to NAT machine
        self.ssh_obj = SSHUtil(host=self.nat_ip, username=self.nat_user,
                          password=self.nat_pwd, timeout=10)

    def install_sshpass(self):
        # Install RPM in NAT machine
        present_dir = r'{}'.format(current_dir)
        present_dir = present_dir.replace('\\', '/')
        local_rpm_path = '{}{}'.format(present_dir, '/config/rpm/sshpass-1.06-2.el7.x86_64.rpm')
        tmp_rpm_path = os.path.join(self.nat_tmp_location, 'sshpass-1.06-2.el7.x86_64.rpm')
        self.ssh_obj.upload_file(local_rpm_path, tmp_rpm_path)

        command = "cd /tmp/ && yes | sudo yum install sshpass-1.06-2.el7.x86_64.rpm"
        self.ssh_obj.execute_command(command)

    def stop_salt_master_service(self):
        """
        This function will stop the salt-master service
        """
        logger.info('############################')
        logger.info("Stop Salt Master service")
        salt_master_service_result = "FAIL"
        # Stop and Check the salt-master service
        tsa_service_operations(self.ssh_obj, 'salt-master.service', login=False, operation='stop')
        result = tsa_service_operations(self.ssh_obj, 'salt-master.service', login=False, operation='status')

        if 'inactive' in result['output']:
            logger.info("Salt Master service is stopped")
        else:
            logger.error("Salt Master service is still running")
            logger.debug("Salt Master service is still running")
            logger.debug(result['output'])
            raise Exception("Salt Master service is running")

        # Stop and Check the salt-api service
        tsa_service_operations(self.ssh_obj, 'salt-api.service', login=False, operation='stop')
        result = tsa_service_operations(self.ssh_obj, 'salt-api.service', login=False, operation='status')

        if 'inactive' in result['output']:
            logger.info("Salt API service is stopped")
            salt_master_service_result = "PASS"
        else:
            logger.error("Salt API service is still running")
            logger.debug("Salt API service is still running")
            logger.debug(result['output'])
            raise Exception("Salt API service is running")

        return salt_master_service_result

    def start_salt_master_service(self):
        """
        This function will start the salt-master service
        """
        logger.info('############################')
        logger.info("Start Salt Master service")
        salt_master_service_result = "FAIL"
        # Check the salt-master service status
        tsa_service_operations(self.ssh_obj, 'salt-master.service', login=False, operation='start')
        result = tsa_service_operations(self.ssh_obj, 'salt-master.service', login=False, operation='status')

        if 'active' in result['output']:
            logger.info("Salt Master service is started")
        else:
            logger.error("Salt Master service is inactive")
            logger.debug("Salt Master service is inactive")
            logger.debug(result['output'])
            raise Exception("Salt Master service start failed")

        logger.info('############################')
        logger.info("Start Salt Master service")
        # Check the salt-api service status
        tsa_service_operations(self.ssh_obj, 'salt-api.service', login=False, operation='start')
        result = tsa_service_operations(self.ssh_obj, 'salt-api.service', login=False, operation='status')

        if 'active' in result['output']:
            logger.info("Salt API service is started")
            salt_master_service_result = "PASS"
        else:
            logger.error("Salt API service is inactive")
            logger.debug("Salt API service is inactive")
            logger.debug(result['output'])
            raise Exception("Salt API service start failed")

        return salt_master_service_result


    def upload_salt_cherrypy_bundle(self):
        """
        Upload Salt CherryPy Tar file to Salt Master VM
        """
        logger.info('############################')
        present_dir = r'{}'.format(current_dir)
        print(os.getcwd())
        local_salt_cherrypy_bundle_path= os.path.join(os.getcwd(),'binaries','tenant_automation_service-cherrypy_v1.1.0.37.tar')
        print(local_salt_cherrypy_bundle_path)

        # Upload the Yaml file to NAT Machine
        tmp_salt_cherrypy_path = os.path.join(self.nat_tmp_location,'tenant_automation_service-cherrypy_v1.1.0.37.tar')
        self.ssh_obj.upload_file(local_salt_cherrypy_bundle_path,
                                  tmp_salt_cherrypy_path)

        # Upload the yaml file from NAT Machine to BB Client
        local_nat_salt_cherrypy_path = tmp_salt_cherrypy_path
        remote_salt_cherrypy_path = os.path.join('/root/tenant_automation_service-cherrypy_v1.1.0.37.tar')
        command = UPOAD_FILE_USING_CURL.format(User=self.sm_user, Password=self.sm_pwd,
                                               localFilePath=local_nat_salt_cherrypy_path,
                                               IP=self.sm_ip, remoteFilePath=remote_salt_cherrypy_path)
        print(command)
        result = self.ssh_obj.execute_command(command)

        logger.info("Uploading the Salt Cherry Py to Salt Master  machine")
        logger.info(result['output'])

    def upgrade_salt_cherrypy(self):
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
            logger.info("Upgrading Salt CherryPy")
            health_result = 'PASS'
            remote_salt_cherrypy_path = os.path.join('/root/tenant_automation_service-cherrypy_v1.1.0.37.tar')
            extracted_salt_cherrypy_folder = 'configure_tsa_salt_1.1.0.37'
            script_name=os.path.join('configure_tsa_salt_1.1.0.37','upgrade_salt_dir.sh')
            salt_upgrade_command = 'sudo tar -xvf {};sudo chmod 755 {};sh {}'.format(remote_salt_cherrypy_path,
                                                                                    extracted_salt_cherrypy_folder,
                                                                                    script_name, script_name)

            sshpass_command = 'sshpass -p {Password} ssh -o StrictHostKeyChecking=no {User}@{IP} \'{cmd}\'' \
                .format(Password=self.sm_pwd, User=self.sm_user,
                        IP=self.sm_ip, cmd=salt_upgrade_command)
            result = self.ssh_obj.execute_command(sshpass_command)
            print(result)

            if "\"status\":True" in result:
                logger.info("Salt CherryPy Tar extracted ")
            else:
                message = "Salt CherryPy Tar extraction failed"
                logger.error(message)
                logger.debug(message)
                logger.error(result['output'])
                raise Exception(message)
            return health_result

    def cleanup(self):
        """
        Clean up the config.yaml
        :return:
        """
        # Close SSH sessions
        self.ssh_obj.close_connections()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    result_dict = {}
    salt_cherrypy_upgrade = SaltCherryPy()
    salt_cherrypy_upgrade.install_sshpass()
    salt_cherrypy_upgrade.upload_salt_cherrypy_bundle()
    salt_cherrypy_upgrade.stop_salt_master_service()
    salt_cherrypy_upgrade.upgrade_salt_cherrypy()
    salt_cherrypy_upgrade.start_salt_master_service()
    salt_cherrypy_upgrade.cleanup()
