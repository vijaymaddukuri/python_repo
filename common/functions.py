import base64
import json
import logging
import os
import yaml


from os.path import join
from common.constants import CONFIG_FILE_PATH, PROTECTION_GROUPS
COMMON_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def decode_base64_string(encoded_data):
    """Decode the data
    :param encoded_data: Encoded data input
    :return: Decoded string
    """
    return str(base64.b64decode(encoded_data), 'utf-8')


def decode_base64_json(encoded_data):
    """Decode the Json data
    :param encoded_data: Encoded data input
    :return: Decoded json output
    """
    return json.loads(str(base64.b64decode(encoded_data), 'utf-8'))


def get_config(appliance, param, yaml_file_path=join(COMMON_BASE_DIR, CONFIG_FILE_PATH)):
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


def dict_to_yaml(data_dict, yaml_file_name):
    """Convert the Dictionary to Yaml file
    :param yaml_file_name: File name to save the yaml data
    :param data: Dictionary variable which contains key, value pairs
    :return: Boolean True or False
    """
    logging.info('Parsing Config Files')
    try:
        with open(yaml_file_name, 'w') as outfile:
            logging.debug('Opening {}'.format(yaml_file_name))
            # Dumping the data to yaml file
            yaml.dump(data_dict, outfile, default_flow_style=False)
            logging.debug('Successfully converted the Dictionary to Yaml file')
            result_flag = True
    except FileNotFoundError:
        message = 'FileNotFoundError: No such file or directory: {}'.format(yaml_file_name)
        logging.fatal(message)
        raise Exception(message)
    except yaml.YAMLError as exc:
        message = "Exception: An exception occured: {}".format(exc)
        logging.fatal(message)
        raise Exception(message)
    except IOError as io_error:
        message = "Exception: An exception occured: {}".format(io_error)
        raise Exception(message)
    except Exception as ex:
        message = "Exception: An exception occured: {}".format(ex)
        raise Exception(message)
    return result_flag


def get_pg_for_retention_time(retention_period, retention_period_type='Day'):
    """
    :param retention_period: Number of Days/Weeks/Months/Years
    :param retention_period_type: If retentionPeriod is 11 and retentionPeriodType is
           Day then backup requested for 11 Days.
           - Default Value: 'Day'
           - Possible Values: 'Day', 'Decade', 'Month', 'Quarter', 'Week', 'Year'
    :return: Name of the Protection Group
    """
    try:
        if str.lower(retention_period_type) not in ['day']:
            return "Invalid type"
        protection_group = PROTECTION_GROUPS[retention_period_type][retention_period]
        return protection_group
    except KeyError:
        return ""

