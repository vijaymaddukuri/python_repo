import logging
import os
import sys

from bb_certificate_generation.ssh_utility import SSHUtil
from bb_certificate_generation.functions import (get_config)


def generate_certificates(config_file_path):
    """
    Generate certificates in BB server and
    import the certificates to local machine
    Example: generate_certificates(C:/deployment_automation)
    :param config_file_path: Config.yaml file path
    :return: Output with status True or False
    """
    return_data = {}
    # Get master details from Yaml file
    yaml_file_path = os.path.join(config_file_path,'config.yaml')
    server_ip = get_config('BB_SERVER', 'SERVER_IP', yaml_file_path)
    server_username = get_config('BB_SERVER', 'SERVER_USERNAME', yaml_file_path)
    server_pwd = get_config('BB_SERVER', 'SERVER_PASSWORD', yaml_file_path)
    tenant_id = get_config('BB_SERVER', 'TENANT_ID', yaml_file_path)
    dns_name = get_config('BB_SERVER', 'DNS_NAME', yaml_file_path)
    rid_name = get_config('BB_SERVER', 'RID', yaml_file_path)

    client_cert_path = get_config('BB_SERVER', 'CLIENT_CERTIFICATES_PATH', yaml_file_path)
    client_cert_list = get_config('BB_SERVER', 'CLIENT_CERTIFICATES', yaml_file_path)
    ca_cert_path = get_config('BB_SERVER', 'CA_CERTIFICATES_PATH', yaml_file_path)
    car_cert = get_config('BB_SERVER', 'CA_CERTIFICATES', yaml_file_path)
    local_file_location = get_config('BB_SERVER', 'LOCAL_FILE_LOCATION', yaml_file_path)



    # Connect to remote machine
    ssh_obj = SSHUtil(host=server_ip, username=server_username,
                      password=server_pwd, timeout=10)

    # Generate certificate on BB server
    command = """
     /opt/appdir/xorch/bin/xorch -l debug bb_cert_generator \
     --gen_ext --gen_cert --yaml /etc/bridgeburner/data/DSO.yaml \
     --suc {tenantID} -T {tenantID} \
     --dns_names {dnsName} \
     --rid {ridName} \
     --server_ips {BBServerIP} \
     --host_name {dnsName} \
     --dest ./certs/Virtustream/clients/ \
     --certpath /etc/bridgeburner/certs/
     """.format(tenantID=tenant_id, dnsName=dns_name,
                ridName=rid_name,BBServerIP=server_ip)
    print(command)
    result = ssh_obj.execute_command(command)

    return_value = ''
    for line in result['output'].readlines():
        return_value = return_value + line
    print('############################')
    print("Certificate generation log")
    print(return_value)

    # Validate the results
    if result['status']:
        logging.info('Successfully generated the certificates')
    else:
        message = 'Unable to generate the certificates'
        logging.debug(message)
        return_data['comment'] = message
        raise Exception(return_data)

    # Export CA certificates to local machine
    ssh_obj.get_remote_files(files=car_cert,
                             remote_file_path=ca_cert_path,
                             local_path=local_file_location)


    # Export Client certificates to local machine
    ssh_obj.get_remote_files(files=client_cert_list,
                             remote_file_path=client_cert_path,
                             local_path=local_file_location)

def upload_certificates(config_file_path):
    """
    Uploading certificates to BB client and restarting the services
    :param config_file_path: Config.yaml file path
    :return: Output with status True or False
    """

    # Get master details from Yaml file
    yaml_file_path = os.path.join(config_file_path,'config.yaml')
    client_ip = get_config('BB_CLIENT', 'CLIENT_IP', yaml_file_path)
    client_username = get_config('BB_CLIENT', 'CLIENT_USERNAME', yaml_file_path)
    client_pwd = get_config('BB_CLIENT', 'CLIENT_PASSWORD', yaml_file_path)
    remote_client_cert_location = get_config('BB_CLIENT',
                                             'REMOTE_CLIENT_CERTIFICATE_LOCATION',
                                             yaml_file_path)
    remote_ca_cert_location = get_config('BB_CLIENT',
                                             'REMOTE_CA_CERTIFICATE_LOCATION',
                                             yaml_file_path)
    os_version = get_config('BB_CLIENT', 'OS_VERSION', yaml_file_path)



    client_cert_list = get_config('BB_SERVER', 'CLIENT_CERTIFICATES', yaml_file_path)
    ca_cert = get_config('BB_SERVER', 'CA_CERTIFICATES', yaml_file_path)
    local_cert_file_location = get_config('BB_SERVER', 'LOCAL_FILE_LOCATION', yaml_file_path)


    # Connect to remote machine
    ssh_obj = SSHUtil(host=client_ip, username=client_username,
                      password=client_pwd, timeout=10)

    # Upload the client certificates to remote machine
    for cert in client_cert_list:
        local_client_cert_path = os.path.join(local_cert_file_location, cert)
        remote_client_cert_path = os.path.join(remote_client_cert_location, cert)
        ssh_obj.upload_file(local_client_cert_path,
                            remote_client_cert_path)

    # Upload the CA certificates to remote machine
    for cert in ca_cert:
        local_ca_cert_path = os.path.join(local_cert_file_location, cert)
        remote_ca_cert_path = os.path.join(remote_ca_cert_location, cert)
        ssh_obj.upload_file(local_ca_cert_path,
                            remote_ca_cert_path)

    # Restart BB Client service
    rhel_flavour = ['centos6', 'rhel7', 'centos7', 'rhel6']
    if os_version.lower() in rhel_flavour:
        command = "initctl restart  bridgeburner \
        && initctl status  bridgeburner"
    elif 'suse' in os_version.lower():
        command = '/etc/init.d/bridgeburner restart \
        && /etc/init.d/bridgeburner status'
    else:
        command = 'systemctl restart bridgeburner && systemctl status bridgeburner'

    result = ssh_obj.execute_command(command)
    return_value = ''
    for line in result['output'].readlines():
        return_value = return_value + line
    print('############################')
    print("{} - Bridgeburner status")
    print(return_value)

    """
    curl --insecure --user root:Password1 -T /root/key.pem sftp://10.100.249.33/root/tem_cert/key.pem
    """


if __name__ == '__main__':
    config_file_path = sys.argv[1]
    generate_certificates(config_file_path)
