import logging
import os
import sys

from ci.ssh_utility import SSHUtil
from common.functions import (get_config)


def upload_code(ci_dir_path, source_path, des_path):
    """
    Upload code to remote machine
    Example: upload_code ws/ci ws/dist/tenant.tar.gz /tmp/tenant.tar.gz
    :param ci_dir_path: CI folder path where all CI scripts are located
    :param source_path: Path the source code
    :param des_path: Destination folder to save the code
    :return: Output with status True or False
    """
    return_data = {}
    # Get master details from Yaml file
    yaml_file_path = os.path.join(ci_dir_path,'config.yaml')
    server_ip = get_config('back_up_server_details', 'SERVER_IP', yaml_file_path)
    server_username = get_config('back_up_server_details', 'SERVER_USERNAME', yaml_file_path)
    server_pwd = get_config('back_up_server_details', 'SERVER_PASSWORD', yaml_file_path)

    # Connect to remote machine
    ssh_obj = SSHUtil(host=server_ip, username=server_username,
                      password=server_pwd, timeout=10)


    # Upload code to remote machine
    upload_data = ssh_obj.upload_file(source_path, des_path)

    # Unzip the code in the remote machine
    if upload_data['status']:
        file = (des_path.split('/'))[-1]
        command = """
        cd /tmp/ && tar -xvf {}
        """.format(file)
        return_data = ssh_obj.execute_command(command)
    else:
        message = 'Unable to upload the code to the remote machine {}'.format(server_ip)
        logging.debug(message)
        return_data['comment'] = message
        raise Exception(return_data)

    # Upload config.yaml file into the remote ONBfactory code
    if return_data['status']:
        file_name = (des_path.split('/'))[-1]
        folder_name = file_name.split('.tar')[0]
        upload_folder = os.path.join('/tmp', folder_name)
        upload_file= os.path.join(upload_folder, 'config.yaml')
        config_filepath = os.path.join(ci_dir_path, 'onb')
        del_command = """
        cd {} && rm -rf config.yaml
        """.format(upload_folder)

        # Remove existing config.yaml file
        return_data=ssh_obj.execute_command(del_command)

        # upload config.yaml to remote machine
        upload_config = ssh_obj.upload_file(os.path.join(config_filepath, 'config.yaml'), upload_file)
    else:
        message = 'Unable to upload the shell script to the remote machine {}'.format(server_ip)
        logging.debug(message)
        return_data['comment'] = message
        raise Exception(return_data)

    # Upload the shell script to remote machine to start the django server
    if upload_config['status']:
        upload_data = ssh_obj.upload_file(os.path.join(ci_dir_path, 'start_server.sh'), '/tmp/start_server.sh')
        dir_path = file.split('.tar')[0]
        command = """
        cd /tmp/ && chmod -R 777 start_server.sh && ./start_server.sh {}
        """.format(dir_path)
        return_data = ssh_obj.execute_command(command)
    else:
        message = 'Unable to upload the config.yaml file to the remote machine {}'.format(server_ip)
        logging.debug(message)
        return_data['comment'] = message
        raise Exception(return_data)

    # Validate the results
    if return_data['status']:
        logging.info('Successfully started the backup server')
    else:
        message = 'Unable to start the backup server in the remote machine {}'.format(server_ip)
        logging.debug(message)
        return_data['comment'] = message
        raise Exception(return_data)


if __name__ == '__main__':
    ci_dir_path = sys.argv[1]
    source_path = sys.argv[2]
    des_path = sys.argv[3]
    upload_code(ci_dir_path, source_path, des_path)
