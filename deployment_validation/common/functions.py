import yaml
import os
import shutil
import logging as logger
import datetime

from os.path import dirname, abspath, join
from csv_to_yaml_convertor.csv_to_yaml_convertor import CsvToYamlConvertor

current_dir = dirname(dirname(abspath(__file__)))


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
        if param is None:
            param_value = doc[appliance]
        else:
            param_value = doc[appliance][param]
        if param_value == "":
            message = 'Value is not updated for the parameter:{} in the yaml config file'\
                .format(param)
            raise Exception(message)
        return param_value
    except Exception as ex:
        message = "Exception: An exception occured: {}".format(ex)
        raise Exception(message)

def print_results(result_dict):
    print('\nResult Summary:')
    print("----------------------------------------------")
    print("Component" + 20 * " " + "Status")
    print("----------------------------------------------")
    for result in result_dict:
        gap = 29 - len(result)
        space = ' ' * gap
        print(result, space, result_dict[result])
        print("\n")
    count = 0
    passed = [i for i in result_dict.values() if i == "PASS"]
    print("----------------------------------------------")
    print("Total Testcases: {}  PASSED:  {}  FAILED: {}".format(len(result_dict), len(passed),
                                                                len(result_dict) - len(passed)))
    print('\n')

def check_service(sshObject, service, ip = None, username = None,
                  password = None, login = True):
    """
    Check the service in the VM and return the result
    :param sshObject: SSH Obj
    :param service: which service need to check example: tas.service
    :param ip: IP of VM to login and check service (Only for TAS)
    :param username: Username of VM to login and check service (Only for TAS)
    :param password: Password of VM to login and check service (Only for TAS)
    :param login: If multiple SSH, option is True (Default)
                  else need to pass the arg login = False
    :return: Dictionary (status, output)
    """
    cmnd = "sudo systVIJAYtl status {}".format(service)
    if login:
        ssh_command = 'sshpass -p {Pwd} ssh -l {User} {IP} {cmd}' \
            .format(Pwd=password, User=username,
                    IP=ip, cmd=cmnd)
    else:
        ssh_command = cmnd
    result = sshObject.execute_command(ssh_command)
    return result

def telnet_connectivity(sshObject, dsm_ip, tas_ip, tas_user, tas_pwd):
    """
    Check the service in the VM and return the result
    :param sshObject: SSH Obj
    :param dsm_ip: DSM IP to check telnet connectivity
    :return: Dictionary (status, output)
    """
    port_list = ['4119', '4120']
    output = {}
    status = True
    for port in port_list:
        shell_cmd = "(echo >/dev/tcp/{}/{}) &>/dev/null && echo \"open\" || echo \"close\""\
            .format(dsm_ip, port)

        ssh_command = "sshpass -p {TASPwd} ssh -l {TASUser} {TASIP} \"{cmd}\"" \
            .format(TASPwd=tas_pwd, TASUser=tas_user,
                    TASIP=tas_ip, cmd=shell_cmd)
        result = sshObject.execute_command(ssh_command)

        if 'open' in result['output']:
            output[port] = 'PASS'
        else:
            output[port] = 'FAIL'
            status = False
    return status, output

def tsa_service_operations(sshObject, service, ip = None, username = None,
                  password = None, login = True, operation='start'):
    """
    Start/stop/restart the tsa service (tas, mw and worker services) in the VM and
    return the result
    :param sshObject: SSH Obj
    :param service: which service need to check example: tas.service
    :param ip: IP of VM to login and check service (Only for TAS)
    :param username: Username of VM to login and check service (Only for TAS)
    :param password: Password of VM to login and check service (Only for TAS)
    :param login: If multiple SSH, option is True (Default)
                  else need to pass the arg login = False
    :param operation: Default is start, other operations are restart and stop
    :return: Dictionary (status, output)
    """
    cmnd = "sudo systVIJAYtl {} {}".format(operation, service)
    if login:
        ssh_command = 'sshpass -p {Pwd} ssh -l {User} {IP} {cmd}' \
            .format(Pwd=password, User=username,
                    IP=ip, cmd=cmnd)
    else:
        ssh_command = cmnd
    result = sshObject.execute_command(ssh_command)
    return result


def check_rabbitmq_queue(sshObject):
    """
    Check the rabbitmq queue in the VM and return the result
    :param sshObject: SSH Obj
    :return: Dictionary (status, output)
    """
    ssh_command = "sudo rabbitmqctl list_queues messages"

    result = sshObject.execute_command(ssh_command)
    return result

def list_of_yaml_files(dir_path):
    return [item for item in os.listdir(dir_path) if '.yaml' in item]

def copy_file(source_filename, source_dir = 'deployment', des_filename = 'config.yaml'):
    source_dir_path = join(current_dir, 'config', source_dir, source_filename)
    destination_dir_path = join(current_dir, 'config', des_filename)
    try:
        shutil.copy(source_dir_path, destination_dir_path)
    except:
        raise Exception("Unable to copy the file - {} to the destination folder {}".format(source_filename,
                                                                                           destination_dir_path))

def convert_csv_to_yaml(service, csv_files_path, base_yaml_name='config.yaml', file_name=None):
    if service == 'deployment':
        base_yaml_path = join(current_dir, 'config', base_yaml_name)

    else:
        base_yaml_path = join(current_dir, 'config', service, base_yaml_name)

    path_to_save_yaml = join(current_dir, 'config', service)
    csv_path = join(csv_files_path, '{}_configuration_data.csv'.format(service))

    # Create object to convert csv to yaml
    yaml_obj = CsvToYamlConvertor(service, base_yaml_path, csv_path, path_to_save_yaml, file_name)

    # Convert CSV to YAML and save the yaml files
    yaml_obj.convert_csv_to_yaml()

    yaml_file_list = list_of_yaml_files(path_to_save_yaml)

    if not len(yaml_file_list):
        raise Exception('Unable to generate {} yaml files'.format(service))
    return yaml_file_list


def save_execution_log(file_name):
    logfile = datetime.datetime.now().strftime('{}_%H_%M_%d_%m_%Y.log'.format(file_name))
    logpath = '{}/{}'.format(current_dir, logfile)
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

def search_for_file_in_dir(file_location, search_string):
    file_list = os.listdir(file_location)
    for item in file_list:
        if search_string in item:
            return item
    return 0



