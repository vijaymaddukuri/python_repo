from utils.SSHUtils import SSHUtil
from utils.GetYamlValue import GetYamlValue


class BridgeBurner:
    """
    Connect to Bridge Burner Server and generate certificates
    Upload Certs to BridgeBurner Client
    """
    def __init__(self):

        self.configyaml = GetYamlValue()
        self.server_ip = self.configyaml.get_config('BB_SERVER',
                                                    'SERVER_IP')
        self.server_username = self.configyaml.get_config('BB_SERVER',
                                                          'SERVER_USERNAME')
        self.server_pwd = self.configyaml.get_config('BB_SERVER',
                                                     'SERVER_PASSWORD')
        self.tenant_id = self.configyaml.get_config('BB_SERVER', 'TENANT_ID')
        self.dns_name = self.configyaml.get_config('BB_SERVER', 'DNS_NAME')
        self.rid_name = self.configyaml.get_config('BB_SERVER', 'RID')
        self.local_file_location = self.configyaml.get_config('BB_SERVER', 'LOCAL_FILE_LOCATION')
        self.client_crt_certificate = "{}.crt".format(self.rid_name)
        self.client_key_certificate = "{}.key".format(self.rid_name)
        self.client_cert_list = [self.client_crt_certificate, self.client_key_certificate]
        self.ca_cert_path = self.configyaml.get_config('BB_SERVER',
                                                       'CA_CERTIFICATES_PATH')
        self.ca_cert = self.configyaml.get_config('BB_SERVER',
                                                  'CA_CERTIFICATES')

    def generate_certificates(self):
        """
        Generate certificates in BB server and
        import the certificates to local machine
        :return: Output with status True or False
        """
        return_data = {}
        hostname = self.configyaml.get_config('BB_SERVER', 'HOSTNAME')
        client_cert_path = self.configyaml.get_config('BB_SERVER',
                                                      'CLIENT_CERTIFICATES_PATH')

        # Connect to Bridge Burner Server machine
        ssh_obj = SSHUtil(host=self.server_ip, username=self.server_username,
                          password=self.server_pwd, timeout=10)

        # Generate certificates on BB server
        command = """
         sudo /opt/appdir/xorch/bin/xorch -l debug bb_cert_generator \
         --gen_ext --gen_cert --yaml /etc/bridgeburner/data/DSO.yaml \
         --suc {tenantID} -T {tenantID} \
         --dns_names {dnsName} \
         --rid {ridName} \
         --server_ips {BBServerIP} \
         --host_name {host} \
         --dest ./certs/VIJAY/clients/ \
         --certpath /etc/bridgeburner/certs/
         """.format(tenantID=self.tenant_id, dnsName=self.dns_name,
                    ridName=self.rid_name, BBServerIP=self.server_ip,
                    host=hostname)

        print(command)
        result = ssh_obj.execute_command(command)

        # Validate the results
        if result['status']:
            print('Successfully generated the certificates')
        else:
            message = 'Unable to generate the certificates'
            print(message)
            return_data['comment'] = message
            raise Exception(return_data)

        # Give full permissions to the file
        command = "sudo chmod -R 777 {} && sudo chmod -R 777 {}/* "\
            .format(self.ca_cert_path, client_cert_path)
        ssh_obj.execute_command(command)

        # Export CA certificates to local machine
        ssh_obj.get_remote_files(files=self.ca_cert,
                                 remote_file_path=self.ca_cert_path,
                                 local_path=self.local_file_location,
                                 multiple_files=False)

        # Export Client certificates to local machine
        ssh_obj.get_remote_files(files=self.client_cert_list,
                                 remote_file_path=client_cert_path,
                                 local_path=self.local_file_location)

        print("Certificates are uploaded to local machine \n")

    def upload_certificates(self):
        """
        Uploading certificates to BB client and restarting the services
        :return: Output with status True or False
        """
        print("Upload BB certs to BB client Machine")
        print('############################')
        client_ip = self.configyaml.get_config('TAS_DETAILS', 'TAS_IP')
        client_username = self.configyaml.get_config('TAS_DETAILS', 'TAS_USER')
        client_pwd = self.configyaml.get_config('TAS_DETAILS', 'TAS_PWD')
        remote_client_cert_location = self.configyaml.get_config('TAS_DETAILS',
                                                                 'REMOTE_CLIENT_CERTIFICATE_LOCATION')
        remote_ca_cert_location = self.configyaml.get_config('TAS_DETAILS',
                                                             'REMOTE_CA_CERTIFICATE_LOCATION')

        local_crt_cert_path = '{}/{}'\
            .format(self.local_file_location, self.client_crt_certificate)
        remote_crt_cert_path = '{}/{}'\
            .format(remote_client_cert_location, self.client_crt_certificate)
        local_key_cert_path = '{}/{}'\
            .format(self.local_file_location, self.client_key_certificate)
        remote_key_cert_path = '{}/{}'\
            .format(remote_client_cert_location, self.client_key_certificate)
        local_ca_cert = '{}/{}'.format(self.local_file_location, self.ca_cert)
        remote_ca_cert = '{}/{}'.format(remote_ca_cert_location, self.ca_cert)

        print("Connect to BB client Machine {}".format(client_ip))
        # Connect to BB client machine
        ssh_obj = SSHUtil(host=client_ip, username=client_username,
                          password=client_pwd, timeout=10)

        # Update CRT certificate to BB client Machine
        ssh_obj.upload_file(local_crt_cert_path,
                            remote_crt_cert_path)
        print("Successfully uploaded {} file to remote machine"
              .format(self.client_cert_list[0]))

        # Update Key certificate to BB client Machine
        ssh_obj.upload_file(local_key_cert_path,
                            remote_key_cert_path)
        print("Successfully uploaded {} file to remote machine"
              .format(self.client_cert_list[1]))

        # Update CA certificate to BB client Machine
        ssh_obj.upload_file(local_ca_cert,
                            remote_ca_cert)
        print("Successfully uploaded {} file to remote machine"
              .format(self.ca_cert))

        # Restart BB service in TAS machine
        command = 'sudo systemctl restart  bridgeburner'
        ssh_obj.execute_command(command)
        print('############################')
        print("BB service restarted")

        # Check BB service status in TAS machine
        command = 'systVIJAYtl status  bridgeburner'
        result = ssh_obj.execute_command(command)
        print('############################')
        print("BB service status")
        print(result['output'].encode('utf-8'))


if __name__ == '__main__':
    BridgeBurnerObj = BridgeBurner()
    BridgeBurnerObj.generate_certificates()
    BridgeBurnerObj.upload_certificates()
