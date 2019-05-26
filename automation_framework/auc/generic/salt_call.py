from robot.api import logger
from utils.SSHUtils import SSHUtil
from utils.GetConfigurations import GetConfigurations
from utils.preprocess_robot_input import preprocess_kwargs, list_2_str
import re


class ExecuteSaltCall:
    """
    This Class is a wrapper for All Salt Calls. Any Salt related functionality in future should come here.

    Saltstack Documentations:
    1. Get started Guide: https://docs.saltstack.com/en/getstarted/fundamentals/index.html
    2. Module references: https://docs.saltstack.com/en/latest/ref/index.html
    """
    def salt_call(self, **kwargs):
        """
        :param kwargs: The value of every entry in kwargs can be Any of the Python Datatypes
        and also Functions (Need to be defined in  auc/generic/functions/)

        Example: We can pass a dictionary or a function in 'pillar'
                 {'a': 'b'}    OR    function:function_name  ('function:' prefix needs to be used)

        Salt Usage:
            A salt Command is typically structured like
            sudo salt <Targeted minion>  <Function/Module name>  <Module arguments>  <Pillars>
        Args:
            func:            Function/ Module name  e.g state.apply
            tgt:             Minion VM Values. It is a List that Looks like [IP,  Hostname]
            args:            Argument to the Function     e.g. networker/automation_cleanup
            pillar:          In case we are running a Salt State file using state.apply function,
                             we can pass variables to it in form of pillars which are python
                             dictionaries
            function_args:   If function is passed in Pillar, it should be function:function_name
                             and the function should return a valid Dictionary

        :return: Salt Response string
        """

        # Preprocess Inputs:
        kwargs = preprocess_kwargs(kwargs)

        # Get all configurations
        c = GetConfigurations()

        # Connect to SALT VM
        salt_ip = c.get_config('local', 'SALT_MASTER_DETAILS', 'SM_IP')
        salt_user = c.get_config('local',  'SALT_MASTER_DETAILS', 'SM_SSH_USER')
        salt_pwd = c.get_config('local',  'SALT_MASTER_DETAILS', 'SM_SSH_PWD')

        self.ssh_obj = SSHUtil(host=salt_ip, username=salt_user,
                               password=salt_pwd, timeout=100)

        salt_func = kwargs.get('func')
        salt_tgt = 'fqdn:{}'.format(kwargs.get('tgt')[1])

        # Check if arguments are passed
        if 'args' in kwargs.keys():
            salt_args = list_2_str(kwargs.get('args'))
        else:
            salt_args = ''

        # Check if Pillars are passed
        if 'pillar' in kwargs.keys():
            salt_pillars = kwargs.get('pillar')
        else:
            salt_pillars = None

        # Generic Salt Command
        if salt_pillars:
            salt_cmd = "sudo salt -G {} {} {} pillar='{}'".format(salt_tgt, salt_func, salt_args, salt_pillars)
        else:
            salt_cmd = "sudo salt -G {} {} {}".format(salt_tgt, salt_func, salt_args)

        result = self.ssh_obj.execute_command(salt_cmd)
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        result['output'] = ansi_escape.sub('', result['output'])
        logger.info("Output of Salt command")
        logger.info(result['output'])

        return result
