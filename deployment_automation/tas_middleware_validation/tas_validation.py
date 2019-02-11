import argparse
import datetime
import logging as logger
import os
import sys
import re
import yaml

current_dir = os.getcwd().replace('tas_middleware_validation', '')
sys.path.append(current_dir)

from deployment_automation.common.ssh_utility import SSHUtil
from deployment_automation.common.functions import (get_config, print_results)
from deployment_automation.config.restConstants import *

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

class TAS:
    """
    Validate all Middleware API's
    """
    def __init__(self, config_file_path=yamlpath):
        self.yaml_file_path = os.path.join(config_file_path, 'config.yaml')
        self.tas_ip = get_config('TAS_DETAILS', 'TAS_IP', self.yaml_file_path)
        self.tas_user = get_config('TAS_DETAILS', 'TAS_USER', self.yaml_file_path)
        self.tas_pwd = get_config('TAS_DETAILS', 'TAS_PWD', self.yaml_file_path)
        self.tenant_id = get_config('TAS_DETAILS', 'TENANT_ID', self.yaml_file_path)
        self.vmid = get_config('VM_DETAILS', 'VMID', self.yaml_file_path)
        self.vm_hostname = get_config('VM_DETAILS', 'VMHOSTNAME', self.yaml_file_path)
        self.retention_days = get_config('VM_DETAILS', 'RETENTION_DAYS', self.yaml_file_path)
        self.retention_type = get_config('VM_DETAILS', 'RETENTION_TYPE', self.yaml_file_path)
        self.callback_url = get_config('VM_DETAILS', 'CALLBACKURL', self.yaml_file_path)
        self.linux_policy_id = get_config('VM_DETAILS', 'LINUX_POLICY_ID', self.yaml_file_path)
        self.win_policy_id = get_config('VM_DETAILS', 'WIN_POLICY_ID', self.yaml_file_path)
        self.task_id = get_config('VM_DETAILS', 'TASKID', self.yaml_file_path)
        self.vm_ip = get_config('VM_DETAILS', 'VM_IP', self.yaml_file_path)
        self.tas_header = BACKUP_SERVICE_HEADER
        self.nat_ip = get_config('NAT_VM', 'SERVER_IP', self.yaml_file_path)
        self.nat_user = get_config('NAT_VM', 'SERVER_USERNAME', self.yaml_file_path)
        self.nat_pwd = get_config('NAT_VM', 'SERVER_PASSWORD', self.yaml_file_path)
        self.nat_tmp_location = get_config('NAT_VM', 'CERTIFICATE_COPY_LOCATION', self.yaml_file_path)
        self.tas_yaml_file_path = '{}\\{}\\{}'.format(yamlpath, 'tas', 'config_tas.yaml')

        # Connect to NAT machine
        self.ssh_obj = SSHUtil(host=self.nat_ip, username=self.nat_user,
                          password=self.nat_pwd, timeout=10)

    def get_tas_config(self):
        """
        Get the tas config.yaml file to jump host
        """
        logger.info("############################")
        logger.info("Get TAS config.yaml to Jump host machine")
        # Get config.yaml from TAS machine to NAT machine
        command = "sshpass -p {passwd} scp {user}@{tas_ip}:/opt/tas/tenant_automation_service/config.yaml /tmp/"\
            .format(passwd=self.tas_pwd, user=self.tas_user, tas_ip=self.tas_ip)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        # Get config.yaml from NAT machine to windows jump host
        remote_file_path = '/{}/{}'.format('tmp', 'config.yaml')
        self.ssh_obj.get_remote_files('config_tas.yaml', remote_file_path,
                                      self.tas_yaml_file_path, multiple_files=False)
        logger.info("Successfully imported the TAS config.yaml to Jump host machine")

    def install_sshpass(self):
        # Install RPM in NAT machine
        present_dir = r'{}'.format(current_dir)
        present_dir = present_dir.replace('\\', '/')
        local_rpm_path = '{}{}'.format(present_dir, '/config/rpm/sshpass-1.06-2.el7.x86_64.rpm')
        tmp_rpm_path = os.path.join(self.nat_tmp_location, 'sshpass-1.06-2.el7.x86_64.rpm')
        self.ssh_obj.upload_file(local_rpm_path, tmp_rpm_path)

        command = "cd /tmp/ && yes | sudo yum install sshpass-1.06-2.el7.x86_64.rpm"
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

    def upload_yaml_file(self):
        """
        Upload Yaml file to tas VM
        """

        logger.info('############################')
        self.tas_config = get_config('TAS_DETAILS', 'CONFIG_YAML_PATH', self.yaml_file_path)
        present_dir = r'{}'.format(current_dir)
        present_dir = present_dir.replace('\\', '/')
        local_tas_yaml_path = '{}{}'.format(present_dir, '/config/tas/config.yaml')

        # Take Backup of config.yaml in TAS machine
        cmnd = 'sudo cp {} /opt/tas/tenant_automation_service/backup_config.yaml'.format(self.tas_config)
        command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
            .format(bbCleintPwd=self.tas_pwd, bbClientUser=self.tas_user,
                    bbClientIP=self.tas_ip, cmd=cmnd)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line
        logger.info("Taking Back of yaml file")
        logger.info(return_value)

        # Upload the Yaml file to NAT Machine
        tmp_yaml_cert_path = os.path.join(self.nat_tmp_location, 'config.yaml')
        self.ssh_obj.upload_file(local_tas_yaml_path,
                                 tmp_yaml_cert_path)

        # Upload the Upload from NAT Machine to BB Client
        local_client_yaml_path = tmp_yaml_cert_path
        remote_client_yaml_path = self.tas_config
        command = "curl --insecure --user {bbClientUser}:{bbCleintPwd} \
        -T {localFilePath} sftp://{bbClientIP}{remoteFilePath}".format(bbClientUser=self.tas_user,
                                                                       bbCleintPwd=self.tas_pwd,
                                                                       localFilePath=local_client_yaml_path,
                                                                       bbClientIP=self.tas_ip,
                                                                       remoteFilePath=remote_client_yaml_path)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line
        logger.info("Uploading the Yaml file to BB client machine")
        logger.info(return_value)

    def check_services(self):
        """
        Check the TAS service
        :return: True or False
        """
        # Check the TAS service status
        tas_result = 'PASS'
        logger.info('############################')
        logger.info("Checking the tas service")
        cmnd = "sudo systemctl status tas.service"
        command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
            .format(bbCleintPwd=self.tas_pwd, bbClientUser=self.tas_user,
                    bbClientIP=self.tas_ip, cmd=cmnd)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        if '(running)' in return_value:
            logger.info("TAS is up and running")
        else:
            message = "TAS service is not running"
            logger.error(message)
            logger.debug(message)
            logger.error(return_value)
            raise Exception("TAS service is not running")

        bb_result = 'PASS'
        # Check the TAS service status
        logger.info('############################')
        logger.info("Checking the Bridgeburner service")
        cmnd = "sudo systemctl status bridgeburner"
        command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
            .format(bbCleintPwd=self.tas_pwd, bbClientUser=self.tas_user,
                    bbClientIP=self.tas_ip, cmd=cmnd)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        if '(running)' in return_value:
            logger.info("Bridgeburner is up and running")
        else:
            message = "Bridgeburner service is not running"
            logger.error(message)
            logger.debug(message)
            logger.error(return_value)
            raise Exception("Bridgeburner service is not running")
        return tas_result, bb_result

    def execute_tas_health_check(self):
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
            logger.info("Validating TAS health check")
            health_result = 'PASS'
            url = API_HEALTH_CHECK.format(self.tas_ip)
            cmnd = "curl {}".format(url)
            command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
                .format(bbCleintPwd=self.tas_pwd, bbClientUser=self.tas_user,
                        bbClientIP=self.tas_ip, cmd=cmnd)
            result = self.ssh_obj.execute_command(command)
            return_value = ''
            for line in result['output'].readlines():
                return_value = return_value + line

            if "\"status\":true" in return_value:
                logger.info("TAS service is up and running")
            else:
                message = "TAS service is not running"
                logger.error(message)
                logger.debug(message)
                logger.error(return_value)
                raise Exception(message)
            return health_result

    def execute_tas_enable_backup(self):
        """
        Function to enable the backup.
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        logger.info('############################')
        logger.info("Validating TAS Enable Backup API")
        url = API_ENABLE_BACKUP.format(self.tas_ip)
        backup_result = 'PASS'
        command = "curl -X POST \"%s\" -H \"accept: application/json\" -H \"Content-Type: application/json\" " \
               "-d \"{\\\"hostName\\\": \\\"%s\\\", \\\"retentionPeriod\\\": %d, " \
                  "\\\"retentionPeriodType\\\": \\\"%s\\\"}\"" \
               % (url, self.vm_hostname, int(self.retention_days), self.retention_type)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        logger.info("Output of Enable Backup command")
        logger.info(return_value)

        if "\"status\":true" in return_value:
            logger.info("Backup is enabled in the VM")
        elif "Failed connect to" in return_value:
            message = "Networker server is not reachable"
            logger.info(message)
            logger.debug(message)
            logger.debug(return_value)
        elif "HTTP/1.1 500 Internal Server Error" in return_value:
            message = "Can access TAS enable backup API."
            logger.info(message)
            logger.debug(message)
            logger.debug(return_value)
        elif "\"status\":false" in return_value:
            message = "Can access TAS enable backup API."
            logger.info(message)
            logger.debug(message)
            logger.debug(return_value)
        elif "Please check the hostname you have entered" in return_value:
            message = "Can access TAS enable backup API."
            logger.info(message)
            logger.debug(message)
            logger.debug(return_value)
        return backup_result

    def execute_tas_enable_security(self):
        """
        Function to enable the security.
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        logger.info('############################')
        logger.info("Validating TAS Enable SECURITY API")
        url = API_ENABLE_SECURITY.format(self.tas_ip)
        security_result = 'PASS'
        command = "curl -X POST \"%s\" -H \"accept: application/json\" -H \"Content-Type: application/json\" " \
                  "-d \"{\\\"LinuxPolicyID\\\": \\\"%s\\\", \\\"WindowsPolicyID\\\": \\\"%s\\\", \\\"VirtualMachineHostName\\\": \\\"%s\\\", \\\"VirtualMachineIPAddress\\\": \\\"%s\\\"}\"" \
                  % (url, self.linux_policy_id, self.win_policy_id, self.vm_hostname, self.vm_ip)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        logger.info("Output of Enable security command")
        logger.info(return_value)

        if "\"status\":true" in return_value:
            logger.info("Enable security API is initiated successfully from TAS")
        else:
            message = "Can access TAS security API."
            logger.info(message)
            logger.debug(message)
            logger.debug(return_value)
        return security_result

    def execute_tas_enable_monitoring(self):
        """
        Function to enable the monitoring.
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        logger.info('############################')
        logger.info("Validating TAS Enable MONITORING API")
        url = API_ENABLE_MONITORING.format(self.tas_ip)
        monitoring_result = 'PASS'
        command = "curl -X POST \"%s\" -H \"accept: application/json\" -H \"Content-Type: application/json\" " \
               "-d \"{\\\"VirtualMachineID\\\": \\\"%s\\\", " \
                  "\\\"VirtualMachineHostName\\\": \\\"%s\\\", \\\"VirtualMachineIPAddress\\\": \\\"%s\\\"}\"" \
               % (url, self.vmid, self.vm_hostname, self.vm_ip)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        logger.info("Output of monitoring API command")
        logger.info(return_value)

        if "\"status\":true" in return_value:
            logger.info("Enable monitoring API is initiated "
                        "successfully from TAS")
        else:
            message = "Can access TAS monitoring API."
            logger.info(message)
            logger.debug(message)
            logger.debug(return_value)
        return monitoring_result

    def validate_networker_end_point(self):
        """
        # Run CURL command to validate the networker end point
        :return: True or False
        """
        logger.info('############################')
        logger.info("Validating NETWORKER end point connectivity API")
        self.nw_count = get_config('networker_server_details',
                                   'NETWORKER_SERVER_COUNT', self.tas_yaml_file_path)
        self.servers = get_config('networker_server_details',
                                  'NETWORKER_SERVERS', self.tas_yaml_file_path)
        self.nw_exp_version = get_config('TAS_DETAILS', 'EXPECTED_NW_VERSION',
                                         self.yaml_file_path)
        networker_result = 'PASS'
        for i in range(int(self.nw_count)):

            url = self.servers[i]['url']
            api = '{}/{}'.format(url, 'nwrestapi')
            user = self.servers[i]['username']
            password = self.servers[i]['password']

            cmnd = 'sudo curl --insecure --user {}:{} {}'.format(user, password, api)
            command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
                .format(bbCleintPwd=self.tas_pwd, bbClientUser=self.tas_user,
                        bbClientIP=self.tas_ip, cmd=cmnd)
            result = self.ssh_obj.execute_command(command)
            return_value = ''
            for line in result['output'].readlines():
                return_value = return_value + line

            logger.info("Checking the Networker server   - {} version"
                        .format(url))

            # Grep the Networker version
            matchObj = re.search("\"version\":\S+", return_value)
            if matchObj:
                print('Networker Version -', matchObj.group())
                # Validate the version
                if self.nw_exp_version in matchObj.group():
                    logger.info('For the networker server - {}, '
                                'Expected Networker version is installed'.format(url))
                else:
                    message = ('For Networker server - {}, Networker version mismatch, '
                               'expected version {} found version {}'
                               .format(url, self.nw_exp_version, matchObj.group()))
                    logger.error(message)
                    logger.debug(message)
                    logger.error(return_value)
                    networker_result = 'FAIL'
            else:
                    message = 'Unable to fetch the Networker version for the server {}'\
                        .format(url)
                    logger.error(message)
                    logger.debug(message)
                    logger.error(return_value)
                    networker_result = 'FAIL'
            return networker_result

    def validate_monitoring_end_point(self):
        """
        Run CURL command to validate the monitoring end point
        :return: True or False
        """

        logger.info('############################')
        logger.info("Validating Monitoring end point connectivity")
        self.monitoring_ip = get_config('nimsoft_server_details', 'NIMSOFT_HUB_IP',
                                        self.tas_yaml_file_path)
        nimsoft_result = 'PASS'

        cmnd = 'ping -c 5 {}'.format(self.monitoring_ip)
        command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
            .format(bbCleintPwd=self.tas_pwd, bbClientUser=self.tas_user,
                    bbClientIP=self.tas_ip, cmd=cmnd)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        logger.info("Pinging to monitoring server  - {}".format(self.monitoring_ip))

        # Grep the Ping results
        matchObj = re.findall('([0-9]+)\%\spacket\sloss', return_value)

        if matchObj:
            if int(matchObj[0]) > 60:
                message = 'Monitoring server is not reachable - {}'\
                    .format(self.monitoring_ip)
                logger.error(message)
                logger.error(return_value)
                nimsoft_result = 'FAIL'
            else:
                logger.info('Monitoring server is reachable')
        else:
            logger.info('Monitoring server is reachable')
        return nimsoft_result

    def validate_dsm_end_point(self):
        """
        # Run CURL command to validate the DSM end point
        :return: True or False
        """
        logger.info('############################')
        logger.info("Validating DSM end point connectivity")
        self.dsm_ip = get_config('trendmicro_server_details', 'DSM_IP',
                                 self.tas_yaml_file_path)
        dsm_result = 'PASS'

        cmnd = 'ping -c 5 {}'.format(self.dsm_ip)
        command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
            .format(bbCleintPwd=self.tas_pwd, bbClientUser=self.tas_user,
                    bbClientIP=self.tas_ip, cmd=cmnd)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        logger.info("Pinging to DSM server  - {}".format(self.dsm_ip))

        # Grep the ping results
        matchObj = re.findall('([0-9]+)\%\spacket\sloss', return_value)

        if matchObj:
            if int(matchObj[0]) > 60:
                message = 'DSM server is not reachable - {}'\
                    .format(self.dsm_ip)
                logger.error(message)
                logger.error(return_value)
                dsm_result = 'FAIL'
            else:
                logger.info('DSM server is reachable')
        else:
            logger.info('DSM server is reachable')
        return dsm_result

    def validate_salt_master_connectivity(self):
        """
        Validating Salt master connectivity from TAS VM
        :return: True or False
        """
        logger.info('############################')
        logger.info("Validating Salt master connectivity from TAS VM")
        salt_master_result = 'PASS'
        self.salt_master_ip = get_config('salt_master_details',
                                         'MASTER_IP', self.tas_yaml_file_path)
        self.salt_master_port = get_config('salt_master_details',
                                           'MASTER_API_PORT', self.tas_yaml_file_path)
        self.salt_master_user = get_config('salt_master_details',
                                           'MASTER_API_USERNAME', self.tas_yaml_file_path)
        self.salt_master_pwd = get_config('salt_master_details',
                                          'MASTER_API_PASSWORD', self.tas_yaml_file_path)

        cmnd = "curl -si {ip}:{port}/login -H \"accept: application/json\" " \
               "-d username='{user}' -d password='{pwd}' -d eauth='pam'"\
            .format(ip=self.salt_master_ip, port=self.salt_master_port,
                    user=self.salt_master_user, pwd=self.salt_master_pwd)
        command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
            .format(bbCleintPwd=self.tas_pwd, bbClientUser=self.tas_user,
                    bbClientIP=self.tas_ip, cmd=cmnd)
        result = self.ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line

        if '200 OK' in return_value:
            logger.info("Able to connect to the salt master from TAS VM")
        else:
            message = "Unable to connect to the salt master from TAS VM"
            logger.error(message)
            logger.error(return_value)
            salt_master_result = 'FAIL'
        return salt_master_result

    def cleanup(self):
        """
        Clean up the config.yaml
        :return:
        """
        tas_config_yaml_path = '{}\\{}'.format(yamlpath, 'tas')
        os.chdir(tas_config_yaml_path)
        if os.path.exists('config_tas.yaml'):
            os.remove('config_tas.yaml')

        fname = self.yaml_file_path
        stream = open(fname, 'r')

        data = yaml.load(stream)

        data['NAT_VM']['SERVER_IP'] = ''
        data['NAT_VM']['SERVER_USERNAME'] = ''
        data['NAT_VM']['SERVER_PASSWORD'] = ''
        data['TAS_DETAILS']['TAS_IP'] = ''
        data['TAS_DETAILS']['TAS_PWD'] = ''
        data['TAS_DETAILS']['TAS_USER'] = ''
        data['TAS_DETAILS']['TENANT_ID'] = ''

        with open(fname, 'w') as yaml_file:
            yaml_file.write(yaml.dump(data, default_flow_style=False))

        # Close SSH sessions
        self.ssh_obj.close_connections()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', "--allapi",
                        action='store_true', help="To run all available TAS APIs")
    parser.add_argument('-y', "--uploadyaml",
                        action='store_true', help="To upload yaml to tas vm")
    parser.add_argument('-b', "--backupapi",
                        action='store_true', help="To run TAS backup API")
    parser.add_argument('-s', "--securityapi",
                        action='store_true', help="Too run TAS security API")
    parser.add_argument('-m', "--monitoringapi",
                        action='store_true', help="To run monitoring API")

    args = parser.parse_args()
    result_dict = {}
    tasObj = TAS()
    tasObj.install_sshpass()
    if args.uploadyaml:
        tasObj.upload_yaml_file()
    tasObj.get_tas_config()
    result_dict['SALT_MASTER_CONNECTIVITY'] = tasObj.validate_salt_master_connectivity()
    result_dict['NETWORKER_CONNECTIVITY'] = tasObj.validate_networker_end_point()
    result_dict['DSM_CONNECTIVITY'] = tasObj.validate_dsm_end_point()
    result_dict['NIMSOFT_CONNECTIVITY'] = tasObj.validate_monitoring_end_point()
    result_dict['TAS_SERVICE'], result_dict['BRIDGEBURNER_SERVICE'] = tasObj.check_services()
    result_dict['TAS_HEALTH_CHECK'] = tasObj.execute_tas_health_check()
    if args.backupapi:
        result_dict['TAS_BACKUP_API'] = tasObj.execute_tas_enable_backup()
    if args.monitoringapi:
        result_dict['TAS_MONITORING_API'] = tasObj.execute_tas_enable_monitoring()
    if args.securityapi:
        result_dict['TAS_SECURITY_API'] = tasObj.execute_tas_enable_security()
    if args.allapi:
        result_dict['TAS_SECURITY_API'] = tasObj.execute_tas_enable_security()
        result_dict['TAS_MONITORING_API'] = tasObj.execute_tas_enable_monitoring()
        result_dict['TAS_BACKUP_API'] = tasObj.execute_tas_enable_backup()

    print_results(result_dict)
    tasObj.cleanup()
