import paramiko

def run_ssh_command(command, server_address, server_username, server_pass):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_address,
                username=server_username,
                password=server_pass)
    session = ssh.get_transport().open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command(command)
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write(server_pass + '\n')
    stdin.flush()
    print(stdout.read().decode("utf-8"))


command = "echo \"master: 10.100.26.124\" > /etc/salt/minion.d/master.conf"
run_ssh_command(command, "10.100.249.55", "root", "Password1")