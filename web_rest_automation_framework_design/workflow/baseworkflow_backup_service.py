from auc import (EnableBackup, DisableBackup, ValidateEnableBackup,
                 ValidateDisableBackup, MiddlewareEnableBackup, ValidateEnableBackupFromWorkerLogs)


class BaseWorkflowBackupService(object):
    """
    In this class we need to define all procedures which will be used
    in robot file backup_automation.robot
    """
    def enable_backup(self, vm_hostname, retention_period, retention_period_type):
        """
        Description: Enables backup for the VM
        """
        EnableBackup(
            self.test_virtustream_api.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def disable_backup(self, vm_hostname):
        """
        Description: Disables backup for the VM
        """
        DisableBackup(
            self.test_virtustream_api.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def validate_enable_of_backup(self, vm_hostname, expected_protection_group):
        """
        Description: Validates backup enabled for the VM
        """
        ValidateEnableBackup(
            self.test_virtustream_api.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def validate_disable_of_backup(self, vm_hostname):
        """
        Description: Validates backup disabled for the VM
        """
        ValidateDisableBackup(
            self.test_virtustream_api.__name__,
            ctx_in=self.wf_context,
            ctx_out=self.wf_context
        ).run()

    def apply_settings_from_files(self, global_file, *workflow_files):
        """
        Description: Collects the data from each YAML file and forms the dictionary
        Args:
        :param global_file: generic yaml file path
        :param workflow_files: Path of Specific yaml file
        :return: Dictionary with all the parameters
        """
        self.ctx.update_context(global_file, self._GC_TAG)

        for yaml_file in workflow_files:
            # YAML Data in all files is appended to the dictionary
            self.ctx.update_context(yaml_file, self._WORKFLOW_TAG)

    def middleware_enable_backup(self):
        MiddlewareEnableBackup(self.middlewware_enable_backup.__name__,
                               ctx_in=self.wf_context, ctx_out=self.wf_context).run()

    def validate_enable_backup_from_worker_logs(self):
        ValidateEnableBackupFromWorkerLogs(self.validate_enable_backup_from_worker_logs.__name__,
                                           ctx_in=self.wf_context, ctx_out=self.wf_context).run()

