import yaml

from os.path import dirname, abspath

current_dir = dirname(dirname(abspath(__file__)))
yaml_path = '{}/{}/{}'.format(current_dir, 'conf', 'generic.yaml')


class GetYamlValue:

    def __init__(self, yaml_file_path=yaml_path):
        """
        :param yaml_file_path: Path of yaml file,
        Default will the config.yaml file
        """
        try:
            with open(yaml_file_path, 'r') as f:
                self.doc = yaml.load(f)
        except Exception as ex:
            message = "Exception: An exception occured: {}".format(ex)
            raise Exception(message)

    def get_config(self, appliance, param):
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
        param_value = self.doc[appliance][param]
        if param_value == "":
            message = 'Value is not updated for the parameter:{} in the yaml config file'\
                .format(param)
            raise Exception(message)
        return param_value
