import self as self

from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req


class MiddlewareEnableBackup(BaseUseCase):
    def middlware_enable_backup(self, tenant_id, vm_id, hostname, retention_days, callback_url):
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
        enable_backup_data = {'TenantID': tenant_id,
                              'VirtualMachineID': vm_id,
                              'VirtualMachineHostname': hostname,
                              'RetentionDays': retention_days,
                              'Callback': callback_url
                              }
        try:
            enable_backup_resp = req.post(MIDDLEWARE_ENABLE_BACKUP.format(
             self.get_yaml_value("backup_service", "backup_service_host")),
             data=enable_backup_data,
             headers=MIDDLEWARE_SERVICE_HEADER, json=None)

        except Exception as e:
            logger.info("Exception occurred while calling Enable Backup API. \n "
                        "Backup enabling did not happen.\nException: %s" % e)
            return 0

        logger.info("Status Code = %s" % enable_backup_resp.status_code)
        logger.info("Message = %s" % enable_backup_resp.text)
        return enable_backup_resp.status_code

    def run_test(self, tenant_id, vm_id, hostname, retention_days, callback_url):
        self.middlware_enable_backup(tenant_id, vm_id, hostname, retention_days, callback_url)
