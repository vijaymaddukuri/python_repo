import sys
from auc.enable_monitoring.enable_monitoring_tas import ExecuteEnableMonitoring
from auc.enable_monitoring.enable_and_validate_monitoring_middleware import EnableAndValidateMonitoringMiddleware
from auc.enable_monitoring.validate_on_minion import ValidateMonitoring
from auc.enable_monitoring.cleanup_monitoring_on_minion import CleanupMonitoring
from utils.context import DataContext
from utils.GetYamlValue import GetYamlValue
from os.path import dirname, abspath

current_dir = dirname(dirname(abspath(__file__)))
sys.path.append(current_dir)


class BaseWorkflowFoMonitoring(object):
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
        self.configyaml = GetYamlValue()

    def reset_settings(self):
        """
        Description: At the end of the test, reset the variables to none
        :return: None
        """
        self.wf_context = None
        self.gc_context = None
        self.ctx = None

    def execute_and_validate_enable_monitoring_mw_api(self, vm_id, vm_hostname, vm_ip, callback, task_id):
        """
        Function to Enable Monitoring on the target VM.

        :return:
            Function returns status code from the REST API response and the messages
            200: OK
            500: INTERNAL SERVER ERROR
        """
        ctx_dict = {'tenant_id': self.configyaml.get_config('MW_DETAILS', 'TENANT_ID'),
                    'mw_ip': self.configyaml.get_config('MW_DETAILS', 'MW_IP'),
                    'mw_user': self.configyaml.get_config('MW_DETAILS', 'MW_USER'),
                    'mw_pwd': self.configyaml.get_config('MW_DETAILS', 'MW_PWD'),
                    'vm_uuid': vm_id,
                    'vm_hostname': vm_hostname,
                    'vm_ip': vm_ip,
                    'callback': callback,
                    'task_id': task_id,
                    'swagger_user': self.configyaml.get_config('MW_DETAILS', 'SWAGGER_USER'),
                    'swagger_pwd': self.configyaml.get_config('MW_DETAILS', 'SWAGGER_PWD')
                    }
        status = EnableAndValidateMonitoringMiddleware(
            self.execute_and_validate_enable_monitoring_mw_api.__name__,
            ctx_in=ctx_dict, ctx_out="").run()
        return status

    def execute_enable_monitoring_tas_api(self, vm_id, vm_hostname, vm_ip):
        """
        Function to Enable Monitoring on the target VM.

        :return:
            Function returns status code from the REST API response and the messages
            200: OK
            500: INTERNAL SERVER ERROR
        """
        ctx_dict = {'tas_ip': self.configyaml.get_config('TAS_DETAILS', 'TAS_IP'),
                    'vm_uuid': vm_id,
                    'vm_hostname': vm_hostname,
                    'vm_ip': vm_ip
                    }
        status_code = ExecuteEnableMonitoring(
            self.execute_enable_monitoring_tas_api.__name__,
            ctx_in=ctx_dict, ctx_out="").run()
        return status_code

    def cleanup_monitoring_api(self, minion_hostname):
        """
            Function to Cleanup/Uninstall Monitoring on the target VM.

            :return:
            True  : Cleanup done successfully
            False : Cleanup failed
        """
        ctx_dict = {'minion_hostname': minion_hostname}

        status = CleanupMonitoring(
            self.cleanup_monitoring_api.__name__,
            ctx_in=ctx_dict, ctx_out="").run()
        return status

    def validate_monitoring_api(self, target_host, user, password):
        """
        Function to Validate Enable Monitoring on the target VM.

        :return:
            Function returns status based on Monitoring/Nimbus service status :
                1: ACTIVE
                0: OTHERWISE
        """
        ctx_dict = {'target_host': target_host,
                    'user': user,
                    'password': password
                    }
        status = ValidateMonitoring(
            self.validate_monitoring_api.__name__,
            ctx_in=ctx_dict, ctx_out="").run()
        return status
