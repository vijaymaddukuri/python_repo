"""
paramiko.SSHClient wrapper
"""

import os
import tempfile
import paramiko
from robot.api import logger


class SSHWrapper(object):
    """
    Wrap paramiko.SSHClient for running command on remote Linux OS
    """

    def __init__(self, *args, **kwargs):
        self._ssh = None
        self._sftp = None
        self.args = args
        self.kwargs = kwargs

    def run_command(self, command, timeout=30):
        """
        Run the specified command and get the output back through SSH
        :param command: Specific command (Linux)
        :param timeout: 30 seconds by default
        :return: output message or error message if any
        """
        ret = ''

        if command:
            logger.info('\nExecuting command: ' + command, False, True)

            try:
                if not self._ssh:
                    self.__enter__()

                std_in, std_out, std_err = self._ssh.exec_command(command, timeout)

                out = std_out.read()
                err = std_err.read()

                std_in.close()
                std_out.close()
                std_err.close()

                if err:
                    logger.warn('\nExecuted the command with error', False)
                    ret = err + out
                else:
                    logger.debug('\nSucceed on executing the command', True)
                    ret = out
            except IOError:
                raise

        return ret

    def send_file(self, local_path, remote_path):
        """
        Send files through SSH 
        """
        try:
            self._sftp = self._ssh.open_sftp()
            self._sftp.put(local_path, remote_path)
        except Exception as e:
            logger.error(e)
            raise

        return True

    def copy_dir(self, local_dir, remote_dir):
        """
        Copy Entire Folder
        """
        try:
            self._sftp = self._ssh.open_sftp()
            for dirpath, dirnames, filenames in os.walk(local_dir):
                print 'dir', dirpath[len(local_dir):]
                remote_path = os.path.join(remote_dir, dirpath[len(local_dir):])
                print remote_path
                try:
                    self._sftp.listdir(remote_path)
                except IOError:
                    self._sftp.mkdir(remote_path)

                for filename in filenames:
                    self._sftp.put(os.path.join(dirpath, filename),
                                   os.path.join(remote_path, filename))
        except Exception as e:
            logger.error(e)
            raise

        return True

    def close(self):
        """
        Close the SSH connection explicitly
        """
        self.__exit__(None, None, None)

    def __enter__(self):
        """
        Initialization
        :return: SSHWrapper object
        """

        # Currently we use username / password to perform authentication
        # host key file is not applied,
        # and the log file is located at %tmp% (/tmp) folder
        filename = os.path.join(
            tempfile.gettempdir(), 'SSHWrapper.log')
        paramiko.util.log_to_file(filename)
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(*self.args, **self.kwargs)

        hostname = self.args[1] if len(self.args) > 1 else self.kwargs['hostname']
        logger.debug('\nConnected to the SSH server: ' + hostname, True)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close SSH connection and clean up resources
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if self._ssh:
            self._ssh.close()
            self._ssh = None
