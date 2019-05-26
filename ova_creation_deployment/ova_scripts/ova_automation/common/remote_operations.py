import os
import sys
import time

from ci.ssh_utility import SSHUtil
from ci.functions import (get_config)


def upload_code(ci_dir_path, source_path, des_path, service, cleanup):
    """
    Upload code to remote machine
    Example: upload_code ws/ci ws/dist/tenant.tar.gz /tmp/tenant.tar.gz
    :param ci_dir_path: CI folder path where all CI scripts are located
    :param source_path: Path the source code
    :param des_path: Destination folder to save the code
    :param service: backupservice or middleware
    :param cleanup: Execute cleanup scripts or not (True or False)
    :return: Output with status True or False
    """
    # Get master details from Yaml file
    yaml_file_path = os.path.join(ci_dir_path, 'config.yaml')
    server_ip = get_config(service, 'SERVER_IP', yaml_file_path)
    server_username = get_config(service, 'SERVER_USERNAME', yaml_file_path)
    server_pwd = get_config(service, 'SERVER_PASSWORD', yaml_file_path)


    # Connect to remote machine
    ssh_obj = SSHUtil(host=server_ip, username=server_username,
                      password=server_pwd, timeout=10)

    # Add proxy
    command = """
    export http_proxy="http://10.131.236.9:3128"
    export https_proxy="https://10.131.236.9:3128" &&
    export PATH=$PATH:$https_proxy &&
    export PATH=$PATH:$http_proxy &&
    echo $http_proxy &&
    echo $https_proxy """
    result = ssh_obj.execute_command(command)

    return_value = ''
    for line in result['output'].readlines():
        return_value = return_value + line
    print('############################')
    print("Proxy settings  info")
    print(return_value)

    # Clearing the existing tar.gz files in remote machine
    command = """cd /home/tas/ && sudo rm -rf *.gz"""
    result = ssh_obj.execute_command(command)

    # Upload tas-tams-python packages to remote machine
    tsa_tams_package_path = os.path.join(ci_dir_path, 'tsa_tams_packages.tar')
    print(tsa_tams_package_path)
    ssh_obj.upload_file(tsa_tams_package_path, '/home/tas/tsa_tams_packages.tar')

    # Upload check_bbc_svc.sh to remote machine
    bbc_svc_path = os.path.join(ci_dir_path, 'check_bbc_svc.sh')
    print(bbc_svc_path)
    ssh_obj.upload_file(bbc_svc_path, '/home/tas/check_bbc_svc.sh')


    # Upload ova_startup_script.py to remote machine
    ova_scriptpath_script_path = os.path.join(ci_dir_path, 'ova_startup_script.py')
    print(ova_scriptpath_script_path)
    ssh_obj.upload_file(ova_scriptpath_script_path, '/home/tas/ova_startup_script.py')

    # Upload clean_up_app_logs.sh to remote machine
    clean_up_app_logs_path = os.path.join(ci_dir_path, 'clean_up_app_logs.sh')
    print(clean_up_app_logs_path)
    ssh_obj.upload_file(clean_up_app_logs_path, '/home/tas/clean_up_app_logs.sh')

    # Upload clear_ovaconfig.sh to remote machine
    clear_ovaconfig_path = os.path.join(ci_dir_path, 'clear_ovaconfig.sh')
    ssh_obj.upload_file(clear_ovaconfig_path, '/home/tas/clear_ovaconfig.sh')

    # Upload install_tas_svc.sh to remote machine
    install_tas_path = os.path.join(ci_dir_path, 'install_tas_svc.sh')
    ssh_obj.upload_file(install_tas_path, '/home/tas/install_tas_svc.sh')

    # Upload bridgeburner.toml to remote machine
    bridgeburner_toml_path = os.path.join(ci_dir_path, 'bridgeburner.toml')
    ssh_obj.upload_file(bridgeburner_toml_path, '/home/tas/bridgeburner.toml')

    # Upload code to remote machine
    ssh_obj.upload_file(source_path, des_path)

    # Upload installation shell script into remote machine
    installation_scripts = get_config(service, 'INSTALLATION_SCRIPT',
                                      yaml_file_path)
    for script in installation_scripts:
        ins_script = '{}'.format(script)
        local_installation_script_path = os.path.join(ci_dir_path, ins_script)
        remote_installation_path = '/home/tas/{}'.format(ins_script)
        ssh_obj.upload_file(local_installation_script_path,
                            remote_installation_path)

        # Execute installation shell script in remote machine
        command = "export http_proxy=http://10.131.236.9:3128 && export https_proxy=https://10.131.236.9:3128 && " \
                  "cd /home/tas/ && ./{}".format(ins_script)
        result = ssh_obj.execute_command(command)
        return_value = ''
        for line in result['output'].readlines():
            return_value = return_value + line
        print('############################')
        print("{} - shell script execution log".format(script))
        print(return_value)
        time.sleep(5)


    if cleanup == 'True':
        stop_service_list = get_config(service, 'STOP_SERVICES',
                                       yaml_file_path)
        # Stop the service
        for process in stop_service_list:
            command = "sudo systVIJAYtl stop {}".format(process)
            ssh_obj.execute_command(command)
            print('{} has been stopped'.format(process))

        clean_up_script_list = get_config(service, 'CLEANUP_SCRIPTS', yaml_file_path)
        # Clean up application logs
        for app in clean_up_script_list:
            command = "cd /home/tas/ && sudo ./{}".format(app)
            result = ssh_obj.execute_command(command)
            return_value = ''
            for line in result['output'].readlines():
                return_value = return_value + line
            print('############################')
            print("{} - clean up script execution log".format(app))
            print(return_value)
            time.sleep(5)


if __name__ == '__main__':
    ci_dir_path = sys.argv[1]
    source_path = sys.argv[2]
    des_path = sys.argv[3]
    service = sys.argv[4]
    cleanup = sys.argv[5]
    upload_code(ci_dir_path, source_path, des_path, service, cleanup)