import paramiko
from getpass import getpass

class CustomSSHClient:
    def __init__(self, hostname, port=22, user=None, password=None):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname, port, user, password)

    def check_output(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.read()

    def __del__(self):
        self.ssh.close()

if __name__ == '__main__':

    ssh=CustomSSHClient('localhost', 22, 'training', getpass())
    op=ssh.check_output('ls-ltr')
    print(op.decode('ascii'))
