from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req


class ValidateEnableBackup(BaseUseCase):
    def get_vm_protection_groups(self):
        """
        Function to get the vm's protection groups details

        Returns:
            Function returns list of Protection groups for the given VM
        """
        # TODO: change after testing
        try:
            nw_api_resp = req.get(API_NW_GET_CLIENTS,
                                  headers=NETWORKER_SERVER_HEADER)

        except Exception as e:
            logger.info("Exception occurred while calling Networker API. "
                        "\nException: %s" % e)
            logger.error("\nTraceback of exception: \n", exc_info=True)
            return 0
        nw_api_resp_data = nw_api_resp.json()
        vm_list = [i["hostname"] for i in
                   nw_api_resp_data["clients"]]
        vm_index = vm_list.index(ctx_in.vm_hostname)
        vm_protection_group = nw_api_resp_data["clients"][vm_index]["protectionGroups"][0]
        return vm_protection_group

    def test_validate_enable_of_backup(self):
        """
        Function to verify that the vm is present in the given protection group

        Returns:
            Function returns True if VM is present in the given protection
            group else it returns False
        """

        vm_protection_group = self.get_vm_protection_groups()
        logger.info("Protection Groups = %s" % vm_protection_group)
        if ctx_in.expected_protection_group == vm_protection_group:
            return True
        else:
            return False

    def run_test(self):
        self.test_validate_ensable_of_backup()
