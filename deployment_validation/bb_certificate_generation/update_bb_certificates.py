import os
import re
import sys

import yaml

current_dir = os.getcwd().replace('bb_certificate_generation', '')
sys.path.append(current_dir)

yamlpath = '{}/{}'.format(current_dir, 'bb_certificate_generation')

from common.ssh_utility import SSHUtil
from common.functions import (get_config)


def generate_certificates(config_file_path=yamlpath):
    """
    Generate certificates in BB server and
    import the certificates to local machine
    Example: generate_certificates(C:/deployment_automation)
    :param config_file_path: Config.yaml file path
    :return: Output with status True or False
    """
    return_data = {}
    # Get master details from Yaml file
    yaml_file_path = os.path.join(config_file_path, 'config.yaml')
    server_ip = get_config('BB_SERVER', 'SERVER_IP', yaml_file_path)
    server_username = get_config('BB_SERVER', 'SERVER_USERNAME', yaml_file_path)
    server_pwd = get_config('BB_SERVER', 'SERVER_PASSWORD', yaml_file_path)
    tenant_id = get_config('BB_SERVER', 'TENANT_ID', yaml_file_path)
    site_id = get_config('BB_SERVER', 'SITE_ID', yaml_file_path)
    dns_name = get_config('BB_SERVER', 'DNS_NAME', yaml_file_path)
    rid_name = get_config('BB_SERVER', 'RID', yaml_file_path)
    hostname = get_config('BB_SERVER', 'HOSTNAME', yaml_file_path)

    client_cert_path = get_config('BB_SERVER', 'CLIENT_CERTIFICATES_PATH', yaml_file_path)
    client_crt_certificate = "{}-backup-automation.crt".format(rid_name)
    client_key_certificate = "{}-backup-automation.key".format(rid_name)
    client_cert_list = [client_crt_certificate, client_key_certificate]
    ca_cert_path = get_config('BB_SERVER', 'CA_CERTIFICATES_PATH', yaml_file_path)
    car_cert = get_config('BB_SERVER', 'CA_CERTIFICATES', yaml_file_path)
    local_file_location = get_config('BB_SERVER', 'LOCAL_FILE_LOCATION', yaml_file_path)

    # Connect to remote machine
    ssh_obj = SSHUtil(host=server_ip, username=server_username,
                      password=server_pwd, timeout=10)

    # Update the DSO.yaml file in BB server
    # Give full permissions to the /etc/bridgeburner/data/ folder
    command = "sudo chmod -R 777 /etc/bridgeburner/data/"
    ssh_obj.execute_command(command, prompt=True, prompt_value=server_pwd)

    fname = "DSO.yaml"
    stream = open(fname, 'r')
    data = yaml.load(stream)
    ip = server_ip
    usdc1_site = site_id

    data['providers']['ServiceProvider']['url'] = "https://{}".format(ip)
    data['providers']['ServiceProvider']['location'] = usdc1_site

    with open(fname, 'w') as yaml_file:
        yaml_file.write(yaml.dump(data, default_flow_style=False))

    os.getcwd()
    local_toml_file_path = os.path.join(os.getcwd(), 'DSO.yaml')
    ssh_obj.upload_file(local_toml_file_path, '/tmp/DSO.yaml')
    ssh_obj.upload_file(local_toml_file_path, r'/etc/bridgeburner/data/DSO.yaml')

    # Generate certificates on BB server
    command = """
     sudo /opt/appdir/xorch/bin/xorch -l debug bb_cert_generator \
     --gen_ext --gen_cert --yaml /etc/bridgeburner/data/DSO.yaml \
     --suc {tenantID} -T {tenantID} \
     --dns_names {dnsName} \
     --rid {ridName}-backup-automation \
     --server_ips {BBServerIP} \
     --host_name {host} \
     --dest ./certs/VIJAY/clients/ \
     --certpath /etc/bridgeburner/certs/
     """.format(tenantID=tenant_id, dnsName=dns_name,
                ridName=rid_name, BBServerIP=server_ip, host=hostname)
    print(command)
    result = ssh_obj.execute_command(command, prompt=True, prompt_value=server_pwd)

    print('############################')
    print("Certificate generation log")
    print(result['output'])

    # Validate the results
    if result['status']:
        print('Successfully generated the certificates')
    else:
        message = 'Unable to generate the certificates'
        print(message)
        return_data['comment'] = message
        raise Exception(return_data)

    # Give full permissions to the file
    command = "sudo chmod -R 777 {} && sudo chmod -R 777 {}/* ".format(ca_cert_path, client_cert_path)
    ssh_obj.execute_command(command, prompt=True, prompt_value=server_pwd)


    # Export CA certificates to local machine
    ssh_obj.get_remote_files(files=car_cert,
                             remote_file_path=ca_cert_path,
                             local_path=local_file_location)

    # Export Client certificates to local machine
    ssh_obj.get_remote_files(files=client_cert_list,
                             remote_file_path=client_cert_path,
                             local_path=local_file_location)

    print("Certificates are uploaded to local machine \n")


def upload_certificates(config_file_path=r'C:\deployment_automation\bb_certificate_generation'):
    """
    Uploading certificates to BB client and restarting the services
    :param config_file_path: Config.yaml file path
    :return: Output with status True or False
    """
    # Get master details from Yaml file
    yaml_file_path = os.path.join(config_file_path, 'config.yaml')
    bbserver_ip = get_config('BB_SERVER', 'SERVER_IP', yaml_file_path)
    tenant_id = get_config('BB_SERVER', 'TENANT_ID', yaml_file_path)
    nat_ip = get_config('NAT_VM', 'SERVER_IP', yaml_file_path)
    nat_user = get_config('NAT_VM', 'SERVER_USERNAME', yaml_file_path)
    nat_pwd = get_config('NAT_VM', 'SERVER_PASSWORD', yaml_file_path)
    nat_tmp_location = get_config('NAT_VM', 'CERTIFICATE_COPY_LOCATION', yaml_file_path)

    client_ip = get_config('BB_CLIENT', 'CLIENT_IP', yaml_file_path)
    client_username = get_config('BB_CLIENT', 'CLIENT_USERNAME', yaml_file_path)
    client_pwd = get_config('BB_CLIENT', 'CLIENT_PASSWORD', yaml_file_path)
    remote_client_cert_location = get_config('BB_CLIENT',
                                             'REMOTE_CLIENT_CERTIFICATE_LOCATION',
                                             yaml_file_path)
    remote_ca_cert_location = get_config('BB_CLIENT',
                                         'REMOTE_CA_CERTIFICATE_LOCATION',
                                         yaml_file_path)

    rid_name = get_config('BB_SERVER', 'RID', yaml_file_path)
    client_crt_certificate = "{}-backup-automation.crt".format(rid_name)
    client_key_certificate = "{}-backup-automation.key".format(rid_name)

    client_cert_list = [client_crt_certificate, client_key_certificate]
    ca_cert = get_config('BB_SERVER', 'CA_CERTIFICATES', yaml_file_path)
    local_cert_file_location = get_config('BB_SERVER', 'LOCAL_FILE_LOCATION', yaml_file_path)

    # Connect to remote machine
    ssh_obj = SSHUtil(host=nat_ip, username=nat_user,
                      password=nat_pwd, timeout=10)

    # Upload the client certificates to NAT machine
    for cert in client_cert_list:
        local_client_cert_path = os.path.join(local_cert_file_location, cert)
        tmp_client_cert_path = os.path.join(nat_tmp_location, cert)
        ssh_obj.upload_file(local_client_cert_path,
                            tmp_client_cert_path)

    # Upload the CA certificates to NAT Machine
    for cert in ca_cert:
        local_ca_cert_path = os.path.join(local_cert_file_location, cert)
        tmp_ca_cert_path = os.path.join(nat_tmp_location, cert)
        ssh_obj.upload_file(local_ca_cert_path,
                            tmp_ca_cert_path)

    # Upload the client certificates from NAT Machine to BB Client
    for cert in client_cert_list:
        local_client_cert_path = os.path.join(nat_tmp_location, cert)
        remote_client_cert_path = os.path.join(remote_client_cert_location, cert)
        command = "curl --insecure --user {bbClientUser}:{bbCleintPwd} \
        -T {localFilePath} sftp://{bbClientIP}{remoteFilePath}".format(bbClientUser=client_username,
                                                                       bbCleintPwd=client_pwd,
                                                                       localFilePath=local_client_cert_path,
                                                                       bbClientIP=client_ip,
                                                                       remoteFilePath=remote_client_cert_path)
        result = ssh_obj.execute_command(command)

        print('############################')
        print("Uploading the Client Certificate to BB client machine")
        print(result['output'])

    # Upload the CA certificates from NAT Machine to BB Client
    for cert in ca_cert:
        local_ca_cert_path = os.path.join(nat_tmp_location, cert)
        remote_ca_cert_path = os.path.join(remote_ca_cert_location, cert)
        command = "curl --insecure --user {bbClientUser}:{bbCleintPwd} \
        -T {localFilePath} sftp://{bbClientIP}{remoteFilePath}".format(bbClientUser=client_username,
                                                                       bbCleintPwd=client_pwd,
                                                                       localFilePath=local_ca_cert_path,
                                                                       bbClientIP=client_ip,
                                                                       remoteFilePath=remote_ca_cert_path)
        result = ssh_obj.execute_command(command)
        print('############################')
        print("Uploading the CA Certificate to BB client machine")
        print(result['output'])

    # Update toml file

    fname = "bridgeburner.toml"

    # Read in the file
    with open(fname, 'r') as file:
        filedata = file.read()

    output = filedata

    cername = "certFile=\"/etc/bridgeburner/certs/VIJAY/clients/{}\"".format(client_cert_list[0])
    keyname = "keyFile=\"/etc/bridgeburner/certs/VIJAY/clients/{}\"".format(client_cert_list[1])
    server = "serverAddress=\"{}:7000\"".format(bbserver_ip)
    bb_client = "Address=\"{}\"".format(client_ip)
    ten_id = "Name=\"{}\"".format(tenant_id)

    output = re.sub("certFile=\"/etc/bridgeburner/certs/VIJAY/clients/\S+.crt\"", cername, output)
    output = re.sub("keyFile=\"/etc/bridgeburner/certs/VIJAY/clients/\S+.key\"", keyname, output)
    output = re.sub("serverAddress=\"\S+\"", server, output)
    output = re.sub("\sAddress=\"\S+\"", " " + bb_client, output)
    output = re.sub("Name=\"\S+\"", ten_id, output)

    with open(fname, 'w') as f:
        f.write(output)

    # Upload the toml file to NAT machine
    for cert in client_cert_list:
        local_client_toml_path = 'bridgeburner.toml'
        tmp_client_toml_path = os.path.join(nat_tmp_location, 'bridgeburner.toml')
        ssh_obj.upload_file(local_client_toml_path,
                            tmp_client_toml_path)

    # Upload the CA certificates from NAT Machine to BB Client
    tmp_client_toml_path = '/tmp/bridgeburner.toml'
    remote_toml_cert_path = '/tmp/bridgeburner.toml'
    command = "curl --insecure --user {bbClientUser}:{bbCleintPwd} \
    -T {localFilePath} sftp://{bbClientIP}{remoteFilePath}".format(bbClientUser=client_username,
                                                                   bbCleintPwd=client_pwd,
                                                                   localFilePath=tmp_client_toml_path,
                                                                   bbClientIP=client_ip,
                                                                   remoteFilePath=remote_toml_cert_path)
    result = ssh_obj.execute_command(command)
    print('############################')
    print("Uploading the toml file to BB client machine")
    print(result['output'])

    # Install SSHPASS in remote machine
    present_dir = r'{}'.format(current_dir)
    present_dir = present_dir.replace('\\', '/')
    local_rpm_path = '{}{}'.format(present_dir, '/config/rpm/sshpass-1.06-2.el7.x86_64.rpm')
    tmp_rpm_path = os.path.join(nat_tmp_location, 'sshpass-1.06-2.el7.x86_64.rpm')
    ssh_obj.upload_file(local_rpm_path, tmp_rpm_path)

    command = "cd /tmp/ && yes | sudo yum install sshpass-1.06-2.el7.x86_64.rpm"
    ssh_obj.execute_command(command)


    # Copy toml file to /etc/bridgeburner folder in TAS machine
    cmnd = 'sudo cp -Rf /tmp/bridgeburner.toml /etc/bridgeburner/client/bridgeburner.toml && sudo systVIJAYtl restart  bridgeburner && sudo systVIJAYtl status  bridgeburner'
    command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
        .format(bbCleintPwd=client_pwd, bbClientUser=client_username,
                bbClientIP=client_ip, cmd=cmnd)
    ssh_obj.execute_command(command)
    print('############################')
    print("Toml file copied to BB client machine")

    # Restart BB service in TAS machine
    cmnd = 'sudo systVIJAYtl restart  bridgeburner'
    command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
        .format(bbCleintPwd=client_pwd, bbClientUser=client_username,
                bbClientIP=client_ip, cmd=cmnd)
    ssh_obj.execute_command(command)
    print('############################')
    print("BB service restarted")

    # Check BB service status in TAS machine
    cmnd = 'systVIJAYtl status  bridgeburner'
    command = 'sshpass -p {bbCleintPwd} ssh -l {bbClientUser} {bbClientIP} {cmd}' \
        .format(bbCleintPwd=client_pwd, bbClientUser=client_username,
                bbClientIP=client_ip, cmd=cmnd)
    result = ssh_obj.execute_command(command)
    print('############################')
    print("BB service status")
    print(result['output'])


if __name__ == '__main__':
    generate_certificates()
    upload_certificates()
