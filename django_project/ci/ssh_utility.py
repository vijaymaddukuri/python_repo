import logging
import paramiko
import socket

logger = logging.getLogger(__name__)


class SSHUtil(object):
    """
    Class to connect to remote server and perform tasks,
    executing the command and uploading the files
    """

    def __init__(self, host, username, password, keyfilepath=None, keyfiletype=None, port=22, timeout=10):
        """
        :param host: Hostname/Ip to connect and upload
        :param username: username to connect the machine
        :param password: Password of the machine
        :param keyfilepath: Path of Key file
        :param keyfiletype: Type of the keyfile (example: DSA or RSA)
        :param port: SSH port
        :param: timeout: connection timeout in secs
        """
        self.key = None
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout
        self.keyfilepath = keyfilepath
        self.keyfiletype = keyfiletype
        self.port = port
        self.client = None
        self.ftp_client = None
        try:
            # Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            logger.debug('Establishing SSH connection to:', self.host, self.port)
            if self.keyfilepath is not None:
                # Get the private key used to authenticate user.
                if self.keyfiletype == 'DSA':
                    # Generating DSA type key.
                    self.key = paramiko.DSSKey.from_private_key_file(self.keyfilepath)
                else:
                    # Generating RSA type key.
                    self.key = paramiko.RSAKey.from_private_key(self.keyfilepath)

            # SSHClient can be used to make connections to the remote server and transfer files
            self.client = paramiko.SSHClient()

            # Setting the missing host key policy to AutoAddPolicy will silently add any missing host keys.
            # Using WarningPolicy, a warning message will be logged if the host key is not previously known
            # but all host keys will still be accepted.
            # Finally, RejectPolicy will reject all hosts which key is not previously known.

            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the host.
            if self.key is not None:
                # Authenticate with a username and a private key located in a file.
                self.client.connect(self.host, self.port, self.username, self.key)
            else:
                # Authenticate with a username and a password.
                self.client.connect(self.host, self.port, self.username, self.password)
            logger.debug("Connected to the server", self.host)
        except paramiko.AuthenticationException:
            message = "Authentication failed, please verify your credentials"
            logger.debug(message)
            raise Exception(message)
        except ConnectionError as ce:
            message = "Unable to connect to the remote machine {}".format(ce)
            logger.info(message)
            raise Exception(message)
        except socket.timeout as e:
            message = "Connection timeout: {}".format(e)
            logger.debug(message)
            raise Exception(message)
        except Exception as e:
            message = "Connection timeout: {}".format(e)
            logger.debug(message)
            raise Exception(message)

    def execute_command(self, command, get_pty=True, allowed_return_codes=[0,1], with_output=False):
        """Execute a command on the remote host.Return a tuple containing
        an integer status and a two strings, the first containing stdout
        and the second containing stderr from the command.
        :param command: Command to execute in remote machine
        :param get_pty: Default Value True
        :param allowed_return_codes: Allowed return code
        :returns: Boolean True or False
        :except: SSH, TimeOut and Authentication Exceptions
        """
        self.ssh_output = None
        return_data = {}
        try:
            if command is not None:
                logger.info("Executing command --> {}".format(command))
                stdin, stdout, stderr = self.client.exec_command(command, timeout=10, get_pty=get_pty)
                if with_output and not stdout:
                    message = "Problem occurred while running command: {} The error is {}"\
                        .format(command, stderr)
                    logger.debug(message)
                    return_data['status'] = False
                    return_data['comment'] = message
                    return return_data
                else:
                    logger.info("Command execution completed successfully {}".format(command))
                    return_data['output'] = stdout
                    return_data['error'] = stderr
                    return_data['status'] = True
                result_flag = stdout.channel.recv_exit_status()
                if result_flag in allowed_return_codes:
                    logger.info('Swallowed acceptable return code of {}'.format(result_flag))
                    return_data['flag'] = result_flag
                else:
                    message = ('unacceptable return code: {}'.format(result_flag))
                    logger.warning(message)
                    return_data['status'] = False
                    return_data['comment'] = message
                    return return_data
                return return_data
        except socket.timeout as e:
            message = "Command timed out.", e
            logger.debug(message)
            raise Exception(message)
        except AttributeError as sshexp:
            message = "Failed to execute the command!", sshexp
            logger.debug(message)
            raise Exception(message)

    def upload_file(self, uploadlocalfilepath, uploadremotefilepath):
        """This method uploads the file to remote server
        :param uploadlocalfilepath: File path in local machine
        :param uploadremotefilepath: Remote location to update the file
        :return: Boolean True or False
        :except: SFTP related exceptions
        """
        return_data = {}
        try:
            ftp_client = self.client.open_sftp()
            if ftp_client is not None:
                # Upload file to the remote machine
                ftp_client.put(uploadlocalfilepath, uploadremotefilepath)
                message = "Successfully uploaded  the file to remote machine: %s" % self.host
                logger.debug(message)
                return_data['status'] = True
            else:
                message = "Unable to establish the FTP connection"
                return_data['status'] = False
                return_data['comment'] = message
                return return_data
        except Exception as e:
            message = 'Unable to upload the file to the remote server', uploadremotefilepath
            logger.debug(message)
            raise Exception(message)
        return return_data

    def close_connections(self):
        """Close the connections"""
        if self.client is not None:
            self.client.close()
        if self.ftp_client is not None:
            self.ftp_client.close()
