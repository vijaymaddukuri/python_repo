from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req


class MiddlewareEnableBackup(BaseUseCase):
    def test_execute_middleware_enable_backup(self):
        """
        Function to enable the filesystem backup for a given VM.

        Args:
        tenant_id (mandatory): String	tenant  uuid in xstream
        vm_id (mandatory): String    vm uuid in xstream
        hostname (mandatory): String  hostname of the vm
        retention_days (mandatory): Int   no. of retention days
        callback_url (mandatory): String
        Returns:
            Function returns Status Code from the REST API response.
            Following status codes can be returned
                200: OK
                404: NOT FOUND
                401: UNAUTHORIZED
                500: INTERNAL SERVER ERROR
        """
        enable_backup_data = {'TenantID': self.ctx_in['tenant_id'],
                              'VirtualMachineID': self.ctx_in['vm_id'],
                              'VirtualMachineHostName': self.ctx_in['hostname'],
                              'RetentionDays': self.ctx_in['retention_days'],
                              'Callback': self.ctx_in['callback_url']
                              }
        try:
            enable_backup_resp = req.post(MIDDLEWARE_ENABLE_BACKUP.format(self.ctx_in['mw_service_host']),
            json=enable_backup_data,
            headers=MIDDLEWARE_SERVICE_HEADER)
            self.ctx_out = True
        except Exception as e:
            logger.info("Exception occurred while calling Enable Backup API. \n "
                        "Backup enabling did not happen.\nException: %s" % e)
            self.ctx_out = False
            return 0

        logger.info("Status Code = %s" % enable_backup_resp.status_code)
        logger.info("Message = %s" % enable_backup_resp.text)
        self.ctx_out = enable_backup_resp.status_code
        return enable_backup_resp.status_code

    def run_test(self):
        sc = self.test_execute_middleware_enable_backup()
        return sc

    def _finalize_context(self):
        assert self.ctx_out == 200, 'Could not enable backup'
