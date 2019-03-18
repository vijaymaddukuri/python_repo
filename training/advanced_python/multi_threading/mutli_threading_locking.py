import threading
from paramiko_ssh_utility.ssh_utility import SSHUtil
from csv import reader
import logging
from time import sleep

fmt="%(threadName)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)

class RemoteLogin:
    def __init__(self, host, user, passwd, cmd, target_file, lock):
        self.host = host
        self.cmd = cmd
        self.lock=lock
        self.log_file = target_file
        self.ssh=SSHUtil(host, username=user, password=passwd)
        self.__run_cmd()

    def __run_cmd(self):
        response = self.ssh.check_output(self.cmd)
        response=response.decode('ascii')
        t_name = threading.current_thread().getName()

        content= "{} login's to the host : {} and ran {} \n {}".format(t_name,
                                                                           self.host, self.cmd, response)
        logging.info('waits the lock')

        with self.lock:
            logging.info('Aquired the lock')
            with open(self.log_file, 'a') as fw:
                sleep(1)
                fw.write(content)
                print(">> {} done with {} <<".format(t_name, self.host))
            logging.debug('Release the lock')

def main():
    threads = []
    target = 'session.log'
    lock_obj = threading.Lock()
    for record in reader(open('host.csv')):
        host, user, passwd, cmd = record
        t = threading.Thread(target=RemoteLogin, args=(host, user, passwd, cmd, target, lock_obj))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()