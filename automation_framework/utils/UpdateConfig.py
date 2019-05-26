"""
Usage:

# Create Object for updating yaml
yamlObj = UpdateConfig(service='TAS')

# Update the yaml file
yamlObj.update_yaml_file(myYaml=readyamldata,
                                     key=['networker_server_details', 'NETWORKER_MAX_JOBS'],
                                     value='102')

# Revert the config.yaml with default values
yamlObj.cleanup()

"""
from os.path import dirname, abspath, os
from robot.api import logger
from utils.GetYamlValue import GetYamlValue
from utils.SSHUtils import SSHUtil

import sys
import yaml

current_dir = dirname(dirname(abspath(__file__)))


class UpdateConfig:
    """
    Update TAS/middleware/worker config.yaml files with latest values.
    """
    def __init__(self, service=None, config_file_path=current_dir):
        """
        :param config_file_path: Path of yaml file
        :param service: TAS/Middleware/Worker
        """
        self.service = str(service).lower()
        self.configyaml = GetYamlValue()

        if not self.service:
            raise Exception("Service name should pass [TAS or Middleware or Worker]")

        if self.service == 'tas':

            self.back_up_yaml_path = r'/opt/tas/tenant_automation_service/backup_config.yaml'

            self.yaml_file_path = os.path.join(config_file_path, 'conf', 'tas_config.yaml')

            self.remote_file_path = self.configyaml.get_config('TAS_DETAILS',
                                                               'CONFIG_YAML_PATH')
            self.vm_ip = self.configyaml.get_config('TAS_DETAILS',
                                                    'TAS_IP')
            self.vm_user = self.configyaml.get_config('TAS_DETAILS',
                                                      'TAS_USER')
            self.vm_pwd = self.configyaml.get_config('TAS_DETAILS',
                                                     'TAS_PWD')
        elif self.service == 'middleware' or self.service == 'worker':

            if self.service == 'middleware':
                self.back_up_yaml_path = r'/opt/middleware/middleware_service/backup_config.yaml'
                self.yaml_file_path = os.path.join(config_file_path, 'conf', 'middleware_config.yaml')
                self.remote_file_path = self.configyaml.get_config('MW_DETAILS',
                                                                   'MW_CONFIG_YAML_PATH')
            else:
                self.back_up_yaml_path = r'/opt/middleware/worker/backup_config.yaml'
                self.yaml_file_path = os.path.join(config_file_path, 'conf', 'worker_config.yaml')
                self.remote_file_path = self.configyaml.get_config('MW_DETAILS',
                                                                   'WORKER_CONFIG_YAML_PATH')

            self.vm_ip = self.configyaml.get_config('MW_DETAILS',
                                                    'MW_IP')
            self.vm_user = self.configyaml.get_config('MW_DETAILS',
                                                      'MW_USER')
            self.vm_pwd = self.configyaml.get_config('MW_DETAILS',
                                                     'MW_PWD')
        # Connect to VM
        self.ssh_obj = SSHUtil(host=self.vm_ip, username=self.vm_user,
                               password=self.vm_pwd, timeout=10)

    def get_yaml_file(self):
        """
        Get the config.yaml from remote machine to local host
        """
        # Take backup of existing config.yaml
        command = 'sudo cp {} {}'.format(self.remote_file_path, self.back_up_yaml_path)

        self.ssh_obj.execute_command(command)

        logger.info("############################")
        logger.info("Get the {} config.yaml to local host machine".format(self.service))
        # Get config.yaml from TAS machine to NAT machine

        self.ssh_obj.get_remote_files(None, self.remote_file_path,
                                          self.yaml_file_path, multiple_files=False)

        logger.info("Successfully imported the {} config.yaml from remote host machine".format(self.service))

    def load_yaml_file(self):
        """
        load YAML file
        In case of any error, this function calls sys.exit(1)
        :return: YAML as dict
        """
        try:
            with open(self.yaml_file_path, 'r') as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    logger.error(exc)
                    sys.exit(1)
        except IOError as e:
            logger.error(e)
            sys.exit(1)

    def update_yaml_data(self, myYaml, key, value, append_mode=False):
        """
        Set or add a key to given YAML data. Call itself recursively.
        :param myYaml: YAML data to be modified
        :param key: key as array of key tokens
        :param value: value of any data type
        :param append_mode default is False
        :return: modified YAML data
        """
        if len(key) == 1:
            if not append_mode or not key[0] in myYaml:
                myYaml[key[0]] = value
            else:
                if type(myYaml[key[0]]) is not list:
                    myYaml[key[0]] = [myYaml[key[0]]]
                myYaml[key[0]].append(value)
        else:
            if not key[0] in myYaml or type(myYaml[key[0]]) is not dict:
                myYaml[key[0]] = {}
            myYaml[key[0]] = self.update_yaml_data(myYaml[key[0]], key[1:], value, append_mode)
        return myYaml

    def rm_yaml_data(self, myYaml, key):
        """
        Remove a key and it's value from given YAML data structure.
        No error or such thrown if the key doesn't exist.
        :param myYaml: YAML data to be modified
        :param key: key as array of key tokens
        :return: modified YAML data
        """
        if len(key) == 1 and key[0] in myYaml:
            del myYaml[key[0]]
        elif key[0] in myYaml:
            myYaml[key[0]] = self.rm_yaml_data(myYaml[key[0]], key[1:])
        return myYaml

    def save_yaml(self, data):
        """
        Saves given YAML data to file and upload yaml file to remote machine
        :param data: YAML data
        """
        try:
            with open(self.yaml_file_path, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)
        except IOError as e:
            logger.error(e)
            sys.exit(1)

        # Upload yaml to remote machine
        self.ssh_obj.upload_file(self.yaml_file_path, self.remote_file_path)

    def cleanup(self):
        # Revert the config.yaml
        command = 'sudo cp {} {}'.format(self.back_up_yaml_path, self.remote_file_path)
        self.ssh_obj.execute_command(command)

    def update_yaml_file(self, keys, value, append=False):
        """
        Update the yaml file
        :param keys: key as array of key tokens
        :param value: value of any data type
        :param append_mode default is False
        :return:
        """
        keys = keys.split(" ")
        logger.info(keys)
        logger.info(value)
        # Get the yaml from remote machine to local machine
        self.get_yaml_file()

        # Read the data of yaml file
        readyamldata = self.load_yaml_file()
        logger.info(readyamldata)

        # Update the values in yaml file
        set_value = self.update_yaml_data(myYaml=readyamldata,
                                             key=keys,
                                             value=value)
        logger.info(set_value)

        # Save and upload the yaml file to remote machine
        self.save_yaml(set_value)
