from robot.api import logger
from utils.GetConfigurations import GetConfigurations
import re


class Functions:
    """
            All Functions needed to generate values for Inputs to Robot Tests are and should come here.
            Feel free to add functions to simplify generating Complex dictionaries like Salt Pillars
    """

    def fetch_nw_dd_details(self):
        """
        Purpose is to generate a Pillar for fetching all Networker and DD details
        :return: Pillar in Dictionary format
        """
        # Get all configurations
        c = GetConfigurations()
        dd = c.get_config('tas', 'networker_server_details', 'DATADOMAIN_SERVERS')
        nw = c.get_config('tas', 'networker_server_details', 'NETWORKER_SERVERS')
        domain = c.get_config('tas', 'networker_server_details', 'DOMAIN_NAME')

        pillar_details = {"nw_dd_fqdn_entry": domain.encode('ascii', 'ignore'),
                          "nw_dd_host_entry": {}}

        # Adding pillar details in 'ip' as a key and 'host' as a value.
        if nw:
            for networker in nw:
                url_obj = re.match('https:\/\/(.*):(.*)', networker["url"], re.M | re.I)
                url_obj = url_obj.group(1)
                pillar_details["nw_dd_host_entry"][url_obj] = \
                    networker["hostname"].encode('ascii', 'ignore')
        if dd:
            for datadomain in dd:
                pillar_details["nw_dd_host_entry"][datadomain["ip"]] = \
                    datadomain["hostname"].encode('ascii', 'ignore')

        return pillar_details
