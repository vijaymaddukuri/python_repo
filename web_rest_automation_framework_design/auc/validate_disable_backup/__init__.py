from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req


class ValidateDisableBackup(BaseUseCase):
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

    def test_validate_disable_of_backup(self):
        """
        Function to verify that the backup is disabled for given VM

        Returns:
            Function returns True if VM does not have any protection group
            i.e. Backup is disabled for VM
        """
        vm_protection_group = self.get_vm_protection_groups()
        logger.info("Protection Groups = %s" % vm_protection_group)
        if vm_protection_group == []:
            # Backup is disabled
            return True
        else:
            # Backup is not disabled. VM present in some protection group
            return False

    def run_test(self):
        self.test_validate_disable_of_backup()
