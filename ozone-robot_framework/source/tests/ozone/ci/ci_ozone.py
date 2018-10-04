#!/bin/env python
"""
Author: Sambit Taria
E-mail: sambit.taria@dell.com
Description: This is the script to trigger automation script in
             the CI infrastructure.The following steps are carried
             out.
             step 1: Install the python dependencies(i.e. Paramiko)

             step 2: Acquire the lock on CI infrastructure

             step 3: Connect to the host System and execute the
                     pybot command

             step 4: After Completion copy the log file from CI machine
                     to the local directory

             step 5: Parse the output.xml file for test case failure
                     and accordingly pass or fail  the build

"""

import subprocess
import xml.etree.ElementTree as eTree
import time
import os
import threading
import importlib

print "Starting CI script"
lock_status = True


def ssh_exec_thread(ssh_object, command):
    (cmd_in, cmd_out, cmd_err) = ssh_object.exec_command(command)
    cmd_out.readlines()
    global lock_status
    lock_status = False


# Check if paramiko is installed or not in bamboo agent
try:
    importlib.import_module(name='paramiko')
    print ('Paramiko already installed')

except ImportError as err:
    print('Paraamiko is not installed')
    # Installing paramiko in bamboo agent
    print ('Installing paramiko.....')
    command = "pip install paramiko"
    ps = subprocess.Popen(command, stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, shell=True)

    out = ps.communicate()[0]
    time.sleep(10)

# Creating time-stamp output directory
dir_name = time.strftime("%Y%m%d%H%M%S")
print('Remote output directory: {0}'.format(dir_name))

# CI infrastructure credentials
# This needs to be changed once fixed CI setup is ready
host = '10.110.102.161'  # This is the static IP for Dedicated CI Machine
user = 'administrator'
password = 'Password2'

# Connect to remote CI machine
import paramiko

print ('Opening SSH connection......')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname=host, username=user, password=password, port=10002)
except Exception as err:
    print("Error: {0}".format(err))
    exit(1)

# Acquiring lock on CI infrastructure
command = '/cygdrive/c/ozone_dev/ozone/source/tests/ozone/ci/file.lock'
print ('Executing command:\n{0}'.format(command))

thread = threading.Thread(target=ssh_exec_thread, args=(ssh, command))
thread.start()
time.sleep(5)

# waiting for lock to be acquired
print('Waiting for lock to be acquired......')
print ('isLocked: {0}'.format(lock_status))
while not lock_status:
    thread.join(timeout=5)
    lock_status = True
    print ("CI infra busy....\n")
    thread = threading.Thread(target=ssh_exec_thread, args=(ssh, command))
    thread.start()
    time.sleep(5)
    print('isLocked = {0}'.format(lock_status))

print ('lock  Acquired...')

# Running Pybot command on remote machine
command = "/cygdrive/c/Python27/Scripts/pybot.bat -d /tmp/{0} -x xunit.xml C:/ozone_dev/ozone/source/tests/ozone/robot/ozone.robot".format(dir_name)
print('Executing robot command:\n{0}'.format(command))

(input, output, error) = ssh.exec_command(command=command)
result = output.readlines()
print('Pybot command result:\n{0}'.format(result))

# Copying result files from CI machine to bamboo agent for parsing
print('Start copying result files from test machine....')
transport = paramiko.Transport((host, 10002))
transport.connect(username=user, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)
files_to_copy = ['report.html', 'log.html', 'output.xml', 'xunit.xml']

for file_name in files_to_copy:
    os.system('touch {0}'.format(file_name))
    try:
        print('Copying {0} file.....'.format(file_name))
        sftp.get('C:\\tmp\{0}\{1}'.format(dir_name, file_name), '{0}'.format(file_name))
        print('{0} file copied'.format(file_name))
    except Exception as err:
        print('Error occurred while copying file')
        print('Error:\n{0}\n'.format(err))
        print('Releasing lock...')
        command = 'pidof -x bash'
        (input, output, error) = ssh.exec_command(command=command)
        status = str(output.readlines())
        while status and str(status) != '\n':
            print ('Killing processes....')
            command = "kill -9 $(pidof -x bash | awk '{print $1}')"
            (input, output, error) = ssh.exec_command(command=command)

            command = 'pidof -x bash'
            (input, output, error) = ssh.exec_command(command=command)
            status = output.readlines()
            print 'status:\n', status
            if status and isinstance(status, list):
                print('ststus = ', status)
                status = status[0]
        print('Lock released')
        print('Closing thread...')
        thread.join(timeout=5)
        exit(-2)

# Parsing the result file
print ('Parsing result file')
FH = open('output.xml')
xml_tree = eTree.parse(FH)
FH.close()
root = xml_tree.getroot()
for child in root:
    if child.tag == 'suite':
        for item in child:
            if item.tag == 'status':
                data = item.attrib
                if data['status'] == 'FAIL':
                    print('Test case Failed')
                    print('releasing lock..')
                    # kill all file lock process
                    command = 'pidof -x bash'
                    (input, output, error) = ssh.exec_command(command=command)
                    status = str(output.readlines())
                    while status and str(status) != '\n':
                        print ('Killing processes....')
                        # command = "kill -9 $(pidof -x bash | awk '{print $1}')"
                        command = "kill -9 $(pidof -x bash)"
                        (input, output, error) = ssh.exec_command(command=command)

                        command = 'pidof -x bash'
                        (input, output, error) = ssh.exec_command(command=command)
                        status = output.readlines()
                        print 'status:\n', status
                        if status and isinstance(status, list):
                            status = status[0]
                    print('Lock released')
                    print('Closing SSH handle')
                    ssh.close()
                    print ('Closing thread')
                    thread.join(timeout=5)
                    # exit(-2)

                else:
                    print('Test case Passed')
                    print('releasing lock..')
                    # kill all file lock process
                    command = 'pidof -x bash'
                    (input, output, error) = ssh.exec_command(command=command)
                    status = str(output.readlines())
                    while status and str(status) != '\n':
                        print ('Killing processes....')
                        # command = "kill -9 $(pidof -x bash | awk '{print $1}')"
                        command = "kill -9 $(pidof -x bash)"
                        print command
                        (input, output, error) = ssh.exec_command(command=command)

                        command = 'pidof -x bash'
                        (input, output, error) = ssh.exec_command(command=command)
                        status = output.readlines()
                        print 'status:\n', status
                        if status and isinstance(status, list):
                            status = status[0]
                    print('Lock released')
                    print ('Closing SSH handle')
                    ssh.close()
                    print ('Closing thread')
                    thread.join(timeout=5)





