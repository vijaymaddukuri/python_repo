import threading
from sshclient import CustomSSHClient
from csv import reader

class RemoteLogin:
    def __init__(self, host, user, passwd, cmd, target_file):
        self.host = host
        self.cmd = cmd
        self.log_file = target_file
        self.ssh=CustomSSHClient(host, user=user, password=passwd)
        self.__run_cmd()

    def __run_cmd(self):
        response = self.ssh.check_output(self.cmd)
        response=response.decode('ascii')
        t_name = threading.current_thread().getName()
        content = "{} login's to the host : {} and ran {} \n {}".format(t_name,
                                                                        self.host, self.cmd, response)
        with open(self.log_file, 'a') as fw:
            fw.write(content)
            print("{} don with {}".format(t_name, self.host))

def main():
    threads = []
    target = 'session.log'
    for record in reader(open('host.csv')):
        host, user, passwd, cmd = record
        t = threading.Thread(target=RemoteLogin, args=(host, user, passwd, cmd, target))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()