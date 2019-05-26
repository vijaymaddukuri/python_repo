import logging
from utils.GetYamlValue import GetYamlValue
from utils.SSHUtils import SSHUtil

logger = logging.getLogger(__name__)


class SALTUtil(object):
    """
    Class to Execute salt state files
    """

    def execute_salt_state(self, login_type, state_file, service_resp_str, vm_minion_id):
        """
        Function to verify Agent is installed or not on VM.
        Returns:
            Function returns PASS or FAIL
        """
        configyaml = GetYamlValue()
        sm_user = configyaml.get_config('SALT_MASTER_DETAILS', 'SM_SSH_USER')
        sm_ip = configyaml.get_config('SALT_MASTER_DETAILS', 'SM_IP')
        sm_pwd = configyaml.get_config('SALT_MASTER_DETAILS', 'SM_SSH_PWD')
        result = 'PASS'
        logger.info("Validating {} ".format(service_resp_str))
        if login_type == "remote":
            nat_ip = configyaml.get_config('NAT_VM', 'SERVER_IP')
            nat_user = configyaml.get_config('NAT_VM', 'SERVER_USERNAME')
            nat_pwd = configyaml.get_config('NAT_VM', 'SERVER_PASSWORD')

            ssh_obj = SSHUtil(host=nat_ip, username=nat_user,
                              password=nat_pwd, timeout=100)

            salt_cmd = "sudo salt {} state.apply {}".format(vm_minion_id, state_file)

            command = 'sshpass -p {smPwd} ssh -l {smUser} {smIP} {cmd}' \
                      .format(smPwd=sm_pwd, smUser=sm_user,
                              smIP=sm_ip, cmd=salt_cmd)
        else:
            ssh_obj = SSHUtil(sm_ip, sm_user, sm_pwd)
            command = "salt '{}' state.apply {}".format(vm_minion_id, state_file)

        logger.info('############################')
        script_output = ssh_obj.execute_command(command)

        logger.info("Output of salt script status execution")
        logger.info(script_output['output'])

        if "Failed:    0" in script_output['output']:
            logger.info("{} is successful".format(service_resp_str))
        else:
            message = "{} is failed".format(service_resp_str)
            logger.info(message)
            result = 'FAIL'
        return result
