from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import requests as req

from requests.auth import HTTPBasicAuth


class ValidateDisableBackup(BaseUseCase):
    def get_vm_protection_groups(self):
        """
        Function to get the vm's protection groups details

        Returns:
            Function returns list of Protection groups for the given VM
        """
        try:
            nw_api_resp = req.get(API_NW_GET_CLIENTS.format(self.ctx_in['networker_server']),
                headers=NETWORKER_SERVER_HEADER,
                auth=HTTPBasicAuth(self.ctx_in['nw_user'], self.ctx_in['nw_pwd']), verify=False)
        except Exception as e:
            logger.info("Exception occurred while calling Networker API. "
                        "\nException: %s" % e)
            raise Exception('Networker API call failed')
        nw_api_resp_data = nw_api_resp.json()
        vm_list = [i["hostname"] for i in nw_api_resp_data["clients"]]
        try:
            vm_index = vm_list.index(self.ctx_in['expected_protection_group'])
            if vm_index:
                logger.info("VM is in the list. "
                      "Validation of Disable backup failed")
                return 1
        except ValueError as e:
            logger.info("VM is not in the list. "
                        "Validation of Disable backup is success")
            logger.info("Exception: %s" % e)
            return 0
        except Exception as e:
            logger.info("Exception occurred while fetching VM list. "
                        "Exception %s " % e)
            return 1
        return 1

    def test_validate_disable_of_backup(self):
        """
        Function to verify that the vm is not present in the given protection group

        :return: Status 0 if backup for VM is disabled in
            expected protection group else Status 1
        """
        resp = self.get_vm_protection_groups()
        if resp == 0:
            self.ctx_out = 0
            return 0
        else:
            self.ctx_out = 1
            return 1

    def run_test(self):
        sc = self.test_validate_disable_of_backup()
        logger.info("Validate Disable Backup Status Code = %s" % sc)
        return sc

    def _finalize_context(self):
        assert self.ctx_out == 0, "Failed to validate disable backup"