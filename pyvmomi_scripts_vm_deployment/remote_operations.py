import logging
import os
import sys

from ci.ssh_utility import SSHUtil
from ci.functions import (get_config)


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
    server_ip = get_config('vm_details', 'SERVER_IP', yaml_file_path)
    server_username = get_config('vm_details', 'SERVER_USERNAME', yaml_file_path)
    server_pwd = get_config('vm_details', 'SERVER_PASSWORD', yaml_file_path)

    # Connect to remote machine
    ssh_obj = SSHUtil(host=server_ip, username=server_username, password=server_pwd, timeout=10)

    # Make the directory in remote machine
    command = """mkdir -p /home/install"""
    ssh_obj.execute_command(command)
    
    # Upload code to remote machine
    upload_data = ssh_obj.upload_file(source_path, des_path)
	
    # Upload tas_svc shell script into remote machine
    tas_svc_file_path = os.path.join(ci_dir_path,'install_tas_svc.sh')
    upload_data = ssh_obj.upload_file(tas_svc_file_path, '/home/install/install_tas_svc.sh')
	
    # Execute tas_svc file in remote machine
    command = """
        cd /home/install && chmod -R 777 install_tas_svc.sh && ./install_tas_svc.sh
        """
    return_data = ssh_obj.execute_command(command)


if __name__ == '__main__':
    ci_dir_path = sys.argv[1]
    source_path = sys.argv[2]
    des_path = sys.argv[3]
    upload_code(ci_dir_path, source_path, des_path)
