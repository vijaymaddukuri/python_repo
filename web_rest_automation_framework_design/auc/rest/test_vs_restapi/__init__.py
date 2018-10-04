from auc.baseusecase import BaseUseCase


class TestVsRestapi(BaseUseCase):
    """
    Description: Gets the VM ID with the template name
    """
    def get_vmid_by_template(self):
        """
        Description: To get the VM ID
        """
        self.vm_id = self.ctx_in.session.get_vmid_by_name(*self.vm_template_details)
        self.policy_id = self.ctx_in.session.get_policy_id_by_name(*self.vs_policy_details)

    def run_test(self):
        """
        Description: Execute the above procedure to VM template info
        """
        self.get_vmid_by_template()


    def _validate_context(self):
        """
        Description: Validate the inputs passed to this function
        """
        if self.ctx_in:
            self.vm_template_details = [self.ctx_in.vm_details.hostname, self.ctx_in.vm_template.template1]
            self.vs_policy_details = [self.ctx_in.vm_details.hostname, self.ctx_in.vs_policy.policy]

    def _finalize_context(self):
        """
        :return: Returns the VM ID and policy ID
        """
        assert self.vm_id, 'Not able to get VM ID'
        assert self.policy_id, 'Not able to get Policy_id'
        setattr(self.ctx_out, 'vm_id', self.vm_id)