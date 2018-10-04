"""
CLIRunner package
"""

import socket
from cliacore.lib.SSHWrapper import SSHWrapper

__author__ = 'GSE Automation'


class CLIRunner(object):
    """
    CLI Runner for running command / shell script
    on remote machine (Linux OS in particular) through SSH
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, **kwargs):
        """
        The required information for accessing SSH server
        : param kwargs:
        hostname: IP address or FQDN
        port: default value is 22
        username: SSH login user
        password: SSH login password
        timeout: default value is 30 seconds
        """
        __defaults__ = {
            'hostname': socket.gethostname(),
            'port': 22, 'username': 'root', 'timeout': 30}

        for key, value in __defaults__.iteritems():
            kwargs.setdefault(key, value)
        self.kwargs = kwargs

    def run_command(self, command='ls', *arguments):
        """
        Run specific bash script / command with different argument(s)
        :param command: Bash script / command
        :param arguments: required or optional arguments
        :return: Execution results with/without error message
        """
        ret = []

        if command:
            # No validation on the command or arguments
            cmd = command.strip()

            try:
                cmd += ' '.join([args[-1] for args in enumerate(arguments)])
                ret += self.run_commands(cmd)

            except RuntimeError:
                raise
        else:
            raise  ValueError('Invalid command:{}'.format(command))

        return ''.join(ret)

    def run_commands(self, *commands):
        """
        Run the specified commands
        :param commands:
        :return: Iterable results
        """
        with SSHWrapper(**self.kwargs) as ssh:
            for cmd in enumerate(commands):
                yield ssh.run_command(cmd[-1], self.kwargs['timeout'])