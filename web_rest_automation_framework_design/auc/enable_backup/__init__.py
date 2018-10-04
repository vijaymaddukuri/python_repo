from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req
import utils.service.restlibrary


class EnableBackup(BaseUseCase):
    def test_enable_backup(self):
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
        enable_backup_data = {'hostname': ctx_in.vm_hostname,
                              'retention_period': ctx_in.retention_period,
                              'retention_period_type': ctx_in.retention_period_type}
        try:
            enable_backup_resp = req.post(API_ENABLE_BACKUP.format(self.get_yaml_value("backup_service","backup_service_host")),
                                          data=enable_backup_data,
                                          headers=BACKUP_SERVICE_HEADER,
                                          json=None)

        except Exception as e:
            logger.info("Exception occurred while calling Enable Backup API. \n "
                        "Backup enabling did not happen.\nException: %s" % e)
            logger.error("\nTraceback of exception: \n", exc_info=True)
            return 0

        logger.info("Status Code = %s" % enable_backup_resp.status_code)
        logger.info("Message = %s" % enable_backup_resp.text)
        return enable_backup_resp.status_code

    def run_test(self):
        self.test_enable_backup()
