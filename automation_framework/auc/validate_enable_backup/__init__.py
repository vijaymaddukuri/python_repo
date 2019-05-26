from auc.baseusecase import BaseUseCase
from robot.api import logger
from conf.restConstants import *
import urllib2
import ssl
import json


class ValidateEnableBackup(BaseUseCase):

    def test_validate_enable_of_backup(self):
        """
        Description: Get the VM protection group for the given VM hostname

        :return: VM protection group name for the given VM hostname
        """
        credentials = ("%s:%s" % (self.ctx_in['nw_user'], self.ctx_in['nw_pwd'])).encode('base64').replace('\n', '')
        NETWORKER_SERVER_HEADER['Authorization'] = 'Basic ' + credentials
        try:
            nw_api_resp = urllib2.Request(API_NW_GET_CLIENTS.format(self.ctx_in['networker_server']),
                headers=NETWORKER_SERVER_HEADER)
            response = urllib2.urlopen(url=nw_api_resp,
                                       context=ssl._create_unverified_context())
            logger.info("nw_api_resp: %s" % nw_api_resp)
            self.ctx_out = 0
        except Exception as e:
            logger.info("Exception occurred while calling Networker API. "
                        "\nException: %s" % e)
            self.ctx_out = 1
            raise Exception('Networker API call failed')
        nw_api_resp_data = json.loads(response.read())
        logger.info("response : %s" % response)
        logger.info("response.read() : %s" % response.read())
        logger.info("nw_api_resp_data : %s " % nw_api_resp_data)
        status = len([ ele for ele in nw_api_resp_data['clients'] if ele['hostname'] == self.ctx_in['vm_hostname'] and ele['protectionGroups'][0] == self.ctx_in['expected_protection_group']])
        sc = 1
        if status != 0:
            logger.info("Validation passed")
            sc = 0
        return sc

    def run_test(self):
        sc = self.test_validate_enable_of_backup()
        logger.info("Status Code = %s" % sc)
        return sc

    def _finalize_context(self):
        assert self.ctx_out == 0, "Failed to validate enable backup"