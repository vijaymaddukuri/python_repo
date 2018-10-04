from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req


class DisableBackup(BaseUseCase):
    def test_disable_backup(self):
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
        disable_backup_data = {'hostname': ctx_in.vm_hostname}

        try:
            disable_backup_resp = req.post(API_DISABLE_BACKUP.format(
                self.get_yaml_value("backup_service", "backup_service_host")),
                 data=disable_backup_data,
                 headers=BACKUP_SERVICE_HEADER, json=None)

        except Exception as e:
            logger.info("Exception occurred while calling Disable Backup API.\n "
                      "Backup disabling did not happen.\nException: %s" % e)
            logger.error("\nTraceback of exception: \n", exc_info=True)
            return 0

        logger.info("Status Code = %s" % disable_backup_resp.status_code)
        logger.info("Message = %s" % disable_backup_resp.text)
        return disable_backup_resp.status_code

    def run_test(self):
        self.test_disable_backup()
