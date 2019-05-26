from auc import (ExecuteEnableBackupAPI, ExecuteDisableBackupAPI, ValidateEnableBackup,
                 ValidateDisableBackup, MiddlewareEnableBackup, ValidateEnableBackupFromWorkerLogs)
from utils.context import DataContext


class BaseWorkflowBackupService(object):
    """
    In this class we need to define all procedures which will be used
    in robot file backup_automation.robot"""

    def __init__(self, ctx=None):
        """
        Step 1: Create variables for both global and local yaml files to store data
        Step 2: Passes the variables names to DataContext proc to assign values
        Args:
        :param ctx:
        """
        self._GC_TAG = 'GC'
        self._WORKFLOW_TAG = 'WORKFLOW'
        if not ctx or not hasattr(ctx, self._GC_TAG):
            self.ctx = DataContext(None, self._GC_TAG)
            self.ctx.update_context(None, self._WORKFLOW_TAG)

        self.wf_context = getattr(self.ctx, self._WORKFLOW_TAG)
        self.gc_context = getattr(self.ctx, self._GC_TAG)

    def reset_settings(self):
        """
        Description: At the end of the test, reset the variables to none
        :return: None
        """
        self.wf_context = None
        self.gc_context = None
        self.ctx = None

    def execute_enable_backup_api(self, backup_service_host, vm_hostname, retention_period, retention_period_type):
        """
        Description: Enables backup for the VM

        :param backup_service_host: Hostname or IP of backup service host
        :param vm_hostname: Hostname of VM in which backup is to be enabled
        :param retention_period: Retention period for backup
        :param retention_period_type: Retention period type like Day/Year/
            Month/Decade. Default value = Day

        :return: Response code of API call
        """
        self.ctx_in = {'backup_service_host': backup_service_host,
                       'vm_hostname': vm_hostname,
                       'retention_period': retention_period,
                       'retention_period_type': retention_period_type
                       }

        sc = ExecuteEnableBackupAPI(
            self.execute_enable_backup_api.__name__,
            ctx_in=self.ctx_in, ctx_out="").run()
        return sc

    def execute_disable_backup_api(self, backup_service_host, vm_hostname):
        """
        Description: Disables backup for the VM

        :param backup_service_host: Hostname or IP of backup service host
        :param vm_hostname: Hostname of VM in which backup is to be disabled

        :return: Response code of API call
        """
        self.ctx_in = {'backup_service_host': backup_service_host,
                       'vm_hostname': vm_hostname
                       }

        sc = ExecuteDisableBackupAPI(
            self.execute_disable_backup_api.__name__,
            ctx_in=self.ctx_in, ctx_out="").run()
        return sc

    def validate_enable_of_backup(self, networker_server, vm_hostname, expected_protection_group, nw_user, nw_pwd):
        """
        Description: Validate Enables backup for the VM

        :param networker_server: Hostname or IP of networker server
        :param vm_hostname: Hostname of VM in which enable backup is to be checked
        :param expected_protection_group: Protection group in which
            VM needs to be checked
        :param nw_user: networker server username
        :param nw_pwd: networker server password

        :return: Status 0 if backup for VM is enabled in
            expected protection group else Status 1
        """
        self.ctx_in = {'networker_server': networker_server,
                       'vm_hostname': vm_hostname,
                       'expected_protection_group': expected_protection_group,
                       'nw_user': nw_user,
                       'nw_pwd': nw_pwd
                       }

        sc = ValidateEnableBackup(
            self.validate_enable_of_backup.__name__,
            ctx_in=self.ctx_in, ctx_out="").run()
        return sc

    def validate_disable_of_backup(self, networker_server, vm_hostname, expected_protection_group, nw_user, nw_pwd):
        """
        Description: Validate Disable backup for the VM

        :param networker_server: Hostname or IP of networker server
        :param vm_hostname: Hostname of VM for which disable backup is to be checked
        :param expected_protection_group: Protection group in which
            VM needs to be checked
        :param nw_user: networker server username
        :param nw_pwd: networker server password

        :return: Status 0 if backup for VM is disabled in
            expected protection group else Status 1
        """
        self.ctx_in = {'networker_server': networker_server,
                       'vm_hostname': vm_hostname,
                       'expected_protection_group': expected_protection_group,
                       'nw_user': nw_user,
                       'nw_pwd': nw_pwd
                       }

        sc = ValidateDisableBackup(
            self.validate_disable_of_backup.__name__,
            ctx_in=self.ctx_in, ctx_out="").run()
        return sc

    def execute_middleware_enable_backup(self, mw_service_host, tenant_id, vm_id, hostname, retention_days, callback_url):
        """
                    Description: Validate the backup status in the Worker logs

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
        ctx_dict = {'mw_service_host': mw_service_host, 'tenant_id': tenant_id, 'vm_id': vm_id, 'hostname': hostname,
                    'retention_days': retention_days, 'callback_url': callback_url}
        sc = MiddlewareEnableBackup(self.execute_middleware_enable_backup.__name__,
                                    ctx_in=ctx_dict, ctx_out="").run()
        return sc

    def execute_validate_enable_backup_from_worker_logs(self, mw_service_host, mw_service_user, mw_service_password,
                                                        log_file_path, search_text):
        """
                Description: Validate the backup status in the Worker logs

                :param mw_server_host: Hostname or IP of the middleware server
                :param mw_server_user_: Username of the middleware server
                :param mw_server_password: Password od the middleware server
                :param log_file_path: File path in which the worker logs exist
                :param search_text: Validation message which needs to be searched
                    in the worker logs


                :return: Status True if the search_text is found in the worker logs
                False if its is not found
                """
        ctx_dict = {'mw_service_host': mw_service_host, 'mw_service_user': mw_service_user,
                    'mw_service_password': mw_service_password, 'log_file_path': log_file_path,
                    'search_text': search_text}
        status = ValidateEnableBackupFromWorkerLogs(self.execute_validate_enable_backup_from_worker_logs.__name__,
                                                    ctx_in=ctx_dict, ctx_out="").run()
        return status
