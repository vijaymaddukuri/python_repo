from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req


class ExecuteDisableBackupAPI(BaseUseCase):
    def test_execute_disable_backup_api(self):
        """
            Function to disable the filesystem backup for a given VM.
            This removes the VM from the bronze filesystem protection group

            Returns:
                Function returns Status Code from the REST API response.
                Following status codes can be returned
                    200: OK
                    404: NOT FOUND
                    401: UNAUTHORIZED
                    500: INTERNAL SERVER ERROR
            """
        disable_backup_data = {'hostName': self.ctx_in['vm_hostname']}
        try:
            disable_backup_resp = req.post(API_DISABLE_BACKUP.format(self.ctx_in['backup_service_host']),
                 json=disable_backup_data,
                 headers=BACKUP_SERVICE_HEADER)
            self.ctx_out = 0
        except Exception as e:
            logger.info("Exception occurred while calling Disable Backup API.\n "
                      "Backup disabling did not happen.\nException: %s" % e)
            self.ctx_out = 0
            raise Exception('failed')
        logger.info("Status Code = %s" % disable_backup_resp.status_code)
        self.ctx_out = disable_backup_resp.status_code
        return disable_backup_resp.status_code

    def run_test(self):
        rc = self.test_execute_disable_backup_api()
        logger.info("Status Code = %s" % rc)
        return rc

    def _finalize_context(self):
        assert self.ctx_out == 200, 'Could not disable backup'
