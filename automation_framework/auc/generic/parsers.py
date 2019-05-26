from robot.api import logger
import re
import json

class Parsers:
    """
        All Parsers for API and SALT response are and should come here. Basic Parsers
        are already provided. But Feel free to add new parsers as you seem fit.
    """

    # ---------------------------Salt Parsers (Reusable)----------------------------------------
    def parse_hosts_has_pair(self, resp):
        response = resp['output']
        if 'True' not in response:
            return 'FAIL'
        else:
            return 'PASS'

    def parse_pkg_list_pkgs(self, resp, pkg_name, pkg_ver='0.0.0.0'):
        response = resp['output']
        if pkg_name in response and (pkg_ver == '0.0.0.0' or pkg_ver in response):
            return 'PASS'
        else:
            return 'FAIL'

    def parse_state_apply(self, resp):
        response = resp['output']
        success = re.search(r'Succeeded: (\d*)', response, re.M | re.I)
        failure = re.search(r'Failed:    (\d*)', response, re.M | re.I)
        if int(success.group(1)) > 0 and int(failure.group(1)) == 0:
            return 'PASS'
        else:
            return 'FAIL'

    # ------------------------Service Response Parsing (Reusable)---------------------------------
    def parse_api_status(self, response, code=200):
        if response.status_code != code:
            return 'FAIL'
        else:
            return 'PASS'

    # Parse Logs (reusable):
    def parse_log(self, response, regex):
        success = re.search(regex, response, re.M | re.I)
        if success:
            return 'PASS'
        else:
            return 'FAIL'

    def parse_salt_response(self, response):
        if response['status']:
            return 'PASS'
        else:
            return 'FAIL'

    # ------------------------------ Add your Parsers here !!-------------------------------------

    def parse_networker_enable(self, response, vm, pg_name):
        for host in response['clients']:
            if host['hostname'].lower() == vm[1].lower() and pg_name in host['protectionGroups']:
                return 'PASS'
        return 'FAIL'

    #Parsing the response of GET Networker Client Details to check Backup Scheduled Status
    def parse_schedule_backup_status(self, response):
        logger.info(response)
        try:
            response = json.dumps(response)
            final_response = json.loads(response)
        except Exception as e:
            logger.error("Exception {} while loading response JSON".format(e))
        return final_response['clients'][0]['scheduledBackup']

    #Fetch Status Code and JSON from response
    def get_response_code(self, response):
        return response.status_code

    def get_response_json(self, response):
        return response.json()

    #Search for text/substring in response
    def response_should_contain_text(self, response, search_text):
        return True if search_text in str(response) else False
