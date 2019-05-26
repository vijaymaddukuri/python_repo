import argparse

from utils.SSHUtils import SSHUtil
from utils.GetYamlValue import GetYamlValue


class SaltRepo:
    """
    Connect to Salt Master Server and upgrade Salt artifacts
    """
    def __init__(self):

        self.configyaml = GetYamlValue()

        self.server_ip = self.configyaml.get_config('SALT_MASTER_DETAILS',
                                                    'SM_IP')
        self.server_username = self.configyaml.get_config('SALT_MASTER_DETAILS',
                                                          'SM_SSH_USER')
        self.server_pwd = self.configyaml.get_config('SALT_MASTER_DETAILS',
                                                     'SM_SSH_PWD')

    def update_salt_repo(self, local_tar_path):
        """
        Upload salt tar to Salt Master machine and install it
        :return: Output with status True or False
        """
        return_data = {}

        # Connect to Salt Master  machine
        ssh_obj = SSHUtil(host=self.server_ip, username=self.server_username,
                          password=self.server_pwd, timeout=10)

        # Upload salt repo to temp directory
        ssh_obj.upload_file(local_tar_path,
                            '/tmp/tenant_automation_service-cherrypy_nightly.tar')

        # Untar the salt repo
        command = "cd /tmp/ && tar -xvf  tenant_automation_service-cherrypy_nightly.tar"
        result = ssh_obj.execute_command(command)

        # Upgrade the salt repo
        command = "cd /tmp/ && " \
                  "cd configure_tsa_salt_nightly && " \
                  "chmod -R 777 upgrade_salt_dir.sh && " \
                  "./upgrade_salt_dir.sh"
        result = ssh_obj.execute_command(command)

        # Validate the results
        if result['status']:
            print('Successfully upgraded the salt repo')
            print(result['output'].encode('utf-8'))
        else:
            message = 'Unable to upgrade the salt repo'
            print(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--salt_tar_path',
                        help='Path to the salt tar file')
    args = parser.parse_args()
    SaltObj = SaltRepo()
    SaltObj.update_salt_repo(args.salt_tar_path)
