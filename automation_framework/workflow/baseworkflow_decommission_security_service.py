import sys

from auc.validate_decommission_security.decommission_and_validate_security_tas_api import ExecuteTasDecommissionSecurityAPI
from auc.validate_decommission_security.decommission_and_validate_security_mw_api import ExecuteMwDecommissionSecurityAPI
from utils.context import DataContext
from utils.GetYamlValue import GetYamlValue
from os.path import dirname, abspath

current_dir = dirname(dirname(abspath(__file__)))
sys.path.append(current_dir)


class BaseWorkflowDecommissionSecurityService(object):
    """
    In this class we need to define all procedures which will be used
    in robot file security_automation.robot"""

    def __init__(self, ctx=None):
        """
        Step 1: Create variables for both global and local
        yaml files to store data
        Step 2: Passes the variables names to DataContext
        proc to assign values
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

    def test_execute_tas_decommission_security_api(self, vm_hostname, vm_ip,
                                              vm_id, vm_rid, task_id):
        """
        Description: Enables backup for the VM
        :param vm_hostname: VM in which security is to be enabled
        :param vm_hostname: VM Hostname
        :param vm_ip: VM IP
        :param vm_id: VM ID
        :param vm_RID: VM RID
        :param task_id: task ID
        :return: PASS or FAIL
        """
        self.ctx_in = {'tas_ip': self.configyaml.get_config('TAS_DETAILS',
                                                            'TAS_IP'),
                       'tas_user': self.configyaml.get_config('TAS_DETAILS',
                                                              'TAS_USER'),
                       'tas_pwd': self.configyaml.get_config('TAS_DETAILS',
                                                             'TAS_PWD'),
                       'vm_hostname': vm_hostname,
                       'vm_ip': vm_ip,
                       'vm_id': vm_id,
                       'vm_rid': vm_rid,
                       'task_id': task_id,
                       'nat_ip': self.configyaml.get_config('NAT_VM',
                                                            'SERVER_IP'),
                       'nat_user': self.configyaml.get_config('NAT_VM',
                                                              'SERVER_USERNAME'),
                       'nat_pwd': self.configyaml.get_config('NAT_VM',
                                                             'SERVER_PASSWORD')
                       }

        result = ExecuteTasDecommissionSecurityAPI(
            self.test_execute_tas_decommission_security_api.__name__,
            ctx_in=self.ctx_in, ctx_out="").run()
        return result

    def test_execute_mw_decommission_security_api(self,
                                                 tenant_id, task_id, callback_url,
                                                 vm_hostname, vm_ip, vmid, vm_rid):
        """
        Description: Enables backup for the VM from middleware
        :param linux_policy_id: Linux policy id
        :param win_policy_id: Windows policy id
        :param task_id: Task ID machine password
        :param tenant_id: tenant_id
        :param callback_url: Call back URL
        :param vm_hostname: VM in which security is to be enabled
        :param vm_ip: VM IP
        :param vmid: VM id
        :param vm_rid: VM RID
        :return: PASS or FAIL
        """
        self.ctx_in = {'mw_ip': self.configyaml.get_config('MW_DETAILS',
                                                           'MW_IP'),
                       'mw_user': self.configyaml.get_config('MW_DETAILS',
                                                             'MW_USER'),
                       'mw_pwd': self.configyaml.get_config('MW_DETAILS',
                                                            'MW_PWD'),
                       'vm_hostname': vm_hostname,
                       'vm_ip': vm_ip,
                       'tenant_id': tenant_id,
                       'vmid': vmid,
                       'vm_rid': vm_rid,
                       'swagger_user': self.configyaml.get_config('MW_DETAILS',
                                                                  'SWAGGER_USER'),
                       'swagger_pwd':   self.configyaml.get_config('MW_DETAILS',
                                                                   'SWAGGER_PWD'),
                       'task_id':  task_id,
                       'callback_url':  callback_url
                       }

        result = ExecuteMwDecommissionSecurityAPI(
            self.test_execute_mw_decommission_security_api.__name__,
            ctx_in=self.ctx_in, ctx_out="").run()
        return result
