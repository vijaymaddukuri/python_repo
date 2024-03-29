import base64
import json
import logging
import os
import yaml


from os.path import join

COMMON_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_config(appliance, param, yaml_file_path):
    """This function gives the yaml value corresponding to the parameter
    sample Yaml file
        xstream_details:
            xtm_host: 10.100.26.90
    :param appliance: The header name as mentioned in the yaml file (ex:xstream_details)
    :param param: The parameter name who's value is to be determined (ex: xtm_host)
    :param yaml_file_path: Path of yaml file, Default will the config.yaml file
    :return: value corresponding to the parameter in yaml file
    :except: Exception while opening or loading the file
    """
    try:
        with open(yaml_file_path, 'r') as f:
            doc = yaml.load(f)
        param_value = doc[appliance][param]
        if param_value == "":
            message = 'Value is not updated for the parameter:{} in the yaml config file'\
                .format(param)
            raise Exception(message)
        return param_value
    except Exception as ex:
        message = "Exception: An exception occured: {}".format(ex)
        raise Exception(message)