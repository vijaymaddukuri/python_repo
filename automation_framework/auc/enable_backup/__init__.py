from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req


class ExecuteEnableBackupAPI(BaseUseCase):
    def test_execute_enable_backup_api(self):
        """
        Function to enable the filesystem backup for a given VM.
        This adds the VM in the bronze filesystem protection group

        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        enable_backup_data = {'hostName': self.ctx_in['vm_hostname'],
                              'retentionPeriod': self.ctx_in['retention_period'],
                              'retentionPeriodType': self.ctx_in['retention_period_type']
                              }
        try:
            enable_backup_resp = req.post(API_ENABLE_BACKUP.format(self.ctx_in['backup_service_host']),
                                          json=enable_backup_data,
                                          headers=BACKUP_SERVICE_HEADER)
            self.ctx_out = True
        except Exception as e:
            logger.info("Exception occurred while calling Enable Backup API. \n "
                        "Backup enabling did not happen.\nException: %s" % e)
            self.ctx_out = False
            raise Exception("Exception: %s" % e)
        logger.info("Status Code = %s" % enable_backup_resp.status_code)
        self.ctx_out = enable_backup_resp.status_code
        return enable_backup_resp.status_code

    def run_test(self):
        rc = self.test_execute_enable_backup_api()
        logger.info("Status Code = %s" % rc)
        return rc

    def _finalize_context(self):
        assert self.ctx_out == 200, 'Could not enable backup'
