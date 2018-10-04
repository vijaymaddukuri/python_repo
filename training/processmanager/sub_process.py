from subprocess import check_output
from shutil import copy, move, rmtree

def run(cmd):
    return  check_output(cmd).decode('ascii')

if __name__ == '__main__':
    print(run(['ipconfig']))
    copy(r'C:\Users\madduv\PycharmProjects\training\processmanager\sub_process.py', 'host.txt')