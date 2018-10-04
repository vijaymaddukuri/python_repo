import yaml
import paramiko
data = dict(
    VM_hostname= 'testHost',
)

file_path = 'hostname.yml'
with open(file_path, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)

def run_ssh_command(server_address, server_username, server_pass):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_address, username =server_username, password =server_pass)
    ftp_client = ssh_client.open_sftp()
    print ftp_client
    ftp_client.put(r'C:\Users\madduv\Documents\Vijay\vijayGitRepo-master\vijayGitRepo-master\Pythong_scripts\data.yml', 'data.yaml')
    ftp_client.close()

run_ssh_command("10.100.26.124", "root", "Password1")





