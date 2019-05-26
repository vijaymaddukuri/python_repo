from auc.baseusecase import BaseUseCase
from robot.api import logger
import paramiko


class ValidateEnableBackupFromWorkerLogs(BaseUseCase):
    """
            Description: Validate Disable backup for the VM

            :param mw_server_host: Hostname or IP of the middleware server
            :param mw_server_user_: Username of the middleware server
            :param mw_server_password: Password od the middleware server
            :param log_file_path: File path in which the worker logs exist
            :param search_text: Validation message which needs to be searched
                in the worker logs

            :return: Status True if the search_text is found in the worker logs
                False if its is not found
            """
    def test_validate_enable_backup_from_worker_logs(self):
        mw_server_host = self.ctx_in['mw_server_host']
        mw_server_user = self.ctx_in['mw_server_user']
        mw_server_password = self.ctx_in['mw_server_password']
        log_file_path = self.ctx_in['log_file_path']
        search_text = self.ctx_in['search_text']
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.connect(mw_server_host, mw_server_user, mw_server_password)
            sftp_client = ssh_client.open_sftp()
            remote_file = sftp_client.open(log_file_path)
            try:
                with open(remote_file, 'rb') as lf:
                    found = False if len([line for line in lf.readlines() if search_text in line])\
                                     == 0 else True
                    self.ctx_out = True
                    self.ctx_out = found
                    return found
            finally:
                remote_file.close()

        except(IOError, ValueError) as e:
                logger.debug("Exception while reading file,Exception: %s" % e)
                return None

    def run_test(self):
        self.test_validate_enable_backup_from_worker_logs()

    def _finalize_context(self):
        assert self.ctx_out == True, 'Could not read from worker logs'
