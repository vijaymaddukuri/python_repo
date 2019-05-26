import yaml

from os.path import dirname, abspath
from utils.SSHUtils import SSHUtil
from conf.restConstants import MWS, BWS, TAS
current_dir = dirname(dirname(abspath(__file__)))
yaml_path = '{}/{}/'.format(current_dir, 'conf')


class GetConfigurations:
    """
    Fetches Config Files from all Services and keep them handy for reference
    """
    def __init__(self, yaml_file_path=yaml_path):
        """
        :param yaml_file_path: Path of yaml file,
        Default will the config.yaml file
        """
        try:
            self.configs = {}
            # Get Common Configs
            with open(yaml_file_path + 'generic.yaml', 'r') as f:
                self.configs['local'] = yaml.load(f)

            # Get the TAS configs
            self.ssh_tas = SSHUtil(host=self.get_config('local', 'TAS_DETAILS', 'TAS_IP'),
                                   username=self.get_config('local', 'TAS_DETAILS', 'TAS_USER'),
                                   password=self.get_config('local', 'TAS_DETAILS', 'TAS_PWD'),
                                   timeout=10)
            self.ssh_tas.get_remote_files("", self.get_config('local', 'CONFIG', 'TAS_CONFIG'),
                                          yaml_file_path + TAS, multiple_files=False)

            with open(yaml_file_path + TAS, 'r') as f:
                self.configs["tas"] = yaml.load(f)

            # Get the Middleware configs
            self.ssh_mws = SSHUtil(host=self.get_config('local', 'MW_DETAILS', 'MW_IP'),
                                   username=self.get_config('local', 'MW_DETAILS', 'MW_USER'),
                                   password=self.get_config('local', 'MW_DETAILS', 'MW_PWD'),
                                   timeout=10)
            self.ssh_mws.get_remote_files("", self.get_config('local', 'CONFIG', 'MWS_CONFIG'),
                                          yaml_file_path + MWS,
                                          multiple_files=False)
            with open(yaml_file_path + MWS, 'r') as f:
                self.configs["middleware"] = yaml.load(f)

            # Get the Worker configs
            self.ssh_mws.get_remote_files("", self.get_config('local', 'CONFIG', 'BWS_CONFIG'),
                                          yaml_file_path + BWS,
                                          multiple_files=False)
            with open(yaml_file_path + BWS, 'r') as f:
                self.configs["worker"] = yaml.load(f)

        except Exception as ex:
            message = "Exception: An exception occured: {}".format(ex)
            raise Exception(message)

    def get_config(self, appliance, param1, param2):
        """This function gives the yaml value corresponding
        to the parameter
        sample Yaml file
            xstream_details:
                xtm_host: 10.100.26.90
        :param appliance: The header name as mentioned in the
        yaml file (ex:xstream_details)
        :param param: The parameter name who's value is to
        be determined (ex: xtm_host)

        :return: value corresponding to the parameter in yaml file
        :except: Exception while opening or loading the file
        """
        param_value = self.configs[appliance][param1][param2]
        if param_value == "":
            message = 'Value is not updated for the parameter:{} in the yaml config file'\
                .format(param1)
            raise Exception(message)
        return param_value
