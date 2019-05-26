#!/bin/bash
import yaml
import os
import re
import socket
import datetime
import sys
import logging
import time
from xml.dom import minidom
import fileinput


# set up logging to file
logfilename='/tmp/ova_startup_script.log'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename=logfilename, filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


BACKUP_KEYS = [('MASTER_IP', "salt_master_details"), ("MASTER_API_PORT", "salt_master_details"),
               ("MASTER_API_USERNAME", "salt_master_details"), ("MASTER_API_PASSWORD", "salt_master_details"),
               ("MASTER_SALT_BASE_LOCATION", "salt_master_details"), ("SSH_PORT_NUMBER", "salt_master_details"),
               ("DSM_IP", "trendmicro_server_details"), ("DSM_TENANT_ID", "trendmicro_server_details"),
               ("DSM_TENANT_PWD", "trendmicro_server_details"), ("DSM_PORT", "trendmicro_server_details"),
               ("DSM_API_SECRET_KEY", "trendmicro_server_details"),
               ("NIMSOFT_HUB_IP", "nimsoft_server_details"), ("NIMSOFT_HUB_NAME", "nimsoft_server_details"),
               ("NIMSOFT_HUB_ROBOT_NAME", "nimsoft_server_details"), ("NIMSOFT_DOMAIN", "nimsoft_server_details"),
               ("NIMSOFT_HUB_USERNAME", "nimsoft_server_details"), ("NIMSOFT_HUB_PASSWORD", "nimsoft_server_details"),
               ("NETWORKER_SERVER_COUNT", "networker_server_details"), ("DOMAIN_NAME", "networker_server_details")]
MIDDLEWARE_KEYS = [('RABBIT_MQ_IP', "rabbitmq"), ("RABBIT_MQ_USERNAME", "rabbitmq"), ("RABBIT_MQ_PASSWORD", "rabbitmq")]
WORKER_KEYS = [('RABBIT_MQ_IP', "rabbitmq"), ("RABBIT_MQ_USERNAME", "rabbitmq"), ("RABBIT_MQ_PASSWORD", "rabbitmq"),
               ('CONSUL_IP', "consul"), ("CONSUL_PORT", "consul"), ("XSTREAM_KEY", "xstream"), ("XSTREAM_SECRET", "xstream"),
               ("VSCAN_SERVER_USERNAME", "vulnerability"), ("VSCAN_SERVER_PASSWORD", "vulnerability"),
               ("VSCAN_SERVER_URL", "vulnerability"), ("NIMSOFT_DOMAIN", "nimsoft_server_details"),
               ("NIMSOFT_IM_API_USERNAME", "nimsoft_server_details"),
               ("NIMSOFT_IM_API_PASSWORD", "nimsoft_server_details"), ("NIMSOFT_IM_API_URL", "nimsoft_server_details")]

def get_folder_name(root_folder, folder_string):
    result = []
    reg_compile = re.compile(folder_string)
    for dirpath, dirnames, filenames in os.walk(root_folder):
        result = result + [dirname for dirname in dirnames if reg_compile.match(dirname)]
    if len(result) > 0:
        return result[0]
    else:
        return ""

BACKUP_CONFIG_FILE_PATH = "/opt/tas/" + get_folder_name("/opt/tas/", "tenant_automation_service") + "/config.yaml"
MIDDLEWARE_CONFIG_FILE_PATH = "/opt/middleware/" + get_folder_name("/opt/middleware/", "middleware_service") + "/config.yaml"
WORKER_CONFIG_FILE_PATH = "/opt/middleware/" + get_folder_name("/opt/middleware/", "worker") + "/config.yaml"


class OVAManager:
    def __init__(self, env_file_name):
        self.default_gateway = ""
        self.hostname = ""
        self.ip_address = ""
        self.primary_dns = ""
        self.subnet_mask = ""
        self.user_password = ""
        self.http_proxy = ""
        self.http_proxy_port = ""
        self.bbserver_ip = ""
        self.bbserver_port = ""
        self.tenant_id = ""
        self.networker_dict = {}
        self.datadomain_dict = {}
        self.networker_servers = []
        self.datadomain_servers = []

        xmldoc = minidom.parse(env_file_name)
        self.itemlist = xmldoc.getElementsByTagName('Property')

    def parsehostparameters(self):

        dummy_ip = "0.0.0.0"
        logging.info('Reading and Parsing Host Parameters...')

        for s in self.itemlist:
            attr = s.attributes['oe:key'].value
            val = s.attributes['oe:value'].value
            if (str(attr) == 'Default_Gateway' ):
                self.default_gateway = s.attributes['oe:value'].value
                logging.info("Setting Default_Gateway as " + self.default_gateway)
            elif (str(attr) == 'Hostname' ):
                self.hostname = s.attributes['oe:value'].value
                logging.info("Setting Hostname as " + self.hostname)
            elif (str(attr) == 'IP_Address' ):
                self.ip_address = s.attributes['oe:value'].value
                logging.info("Setting IP_Address as " + self.ip_address)
            elif (str(attr) == 'Primary_DNS'):
                self.primary_dns = s.attributes['oe:value'].value
                logging.info("Setting Primary_DNS as " + self.primary_dns)
            elif (str(attr) == 'Subnet_Mask'):
                self.subnet_mask = s.attributes['oe:value'].value
                logging.info("Setting Subnet_Mask as " + self.subnet_mask)
            elif (str(attr) == 'Http_Proxy'):
                self.http_proxy = s.attributes['oe:value'].value
                logging.info("Setting Http_Proxy as " + self.http_proxy)
            elif (str(attr) == 'Http_Proxy_Port'):
                self.http_proxy_port = s.attributes['oe:value'].value
                logging.info("Setting Http_Proxy_Port as " + self.http_proxy_port)
            elif (str(attr) == 'bbserver_ip'):
                self.bbserver_ip = s.attributes['oe:value'].value
                logging.info("Setting BB Server IP as " + self.bbserver_ip)
            elif (str(attr) == 'bbserver_port'):
                self.bbserver_port = s.attributes['oe:value'].value
                logging.info("Setting BB Server port as " + self.bbserver_port)
            elif (str(attr) == 'tenant_id'):
                self.tenant_id = s.attributes['oe:value'].value
                logging.info("Setting Tenant Id as " + self.tenant_id)
            elif ('NETWORKER1' in str(attr)) and s.attributes['oe:value'].value:
                self.set_ovaparameters_to_dict("NETWORKER1_", self.networker_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('NETWORKER2' in str(attr)) and s.attributes['oe:value'].value:
                self.set_ovaparameters_to_dict("NETWORKER2_", self.networker_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('NETWORKER3' in str(attr)) and s.attributes['oe:value'].value:
                self.set_ovaparameters_to_dict("NETWORKER3_", self.networker_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('NETWORKER4' in str(attr)) and s.attributes['oe:value'].value:
                self.set_ovaparameters_to_dict("NETWORKER4_", self.networker_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('NETWORKER5' in str(attr)) and s.attributes['oe:value'].value:
                self.set_ovaparameters_to_dict("NETWORKER5_", self.networker_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('DATADOMAIN1' in str(attr)) and s.attributes['oe:value'].value and s.attributes['oe:value'].value != dummy_ip:
                self.set_ovaparameters_to_dict("DATADOMAIN1_", self.datadomain_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('DATADOMAIN2' in str(attr)) and s.attributes['oe:value'].value and s.attributes['oe:value'].value != dummy_ip:
                self.set_ovaparameters_to_dict("DATADOMAIN2_", self.datadomain_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('DATADOMAIN3' in str(attr)) and s.attributes['oe:value'].value and s.attributes['oe:value'].value != dummy_ip:
                self.set_ovaparameters_to_dict("DATADOMAIN3_", self.datadomain_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('DATADOMAIN4' in str(attr)) and s.attributes['oe:value'].value and s.attributes['oe:value'].value != dummy_ip:
                self.set_ovaparameters_to_dict("DATADOMAIN4_", self.datadomain_dict, str(attr),
                                               s.attributes['oe:value'].value)
            elif ('DATADOMAIN5' in str(attr)) and s.attributes['oe:value'].value and s.attributes['oe:value'].value != dummy_ip:
                self.set_ovaparameters_to_dict("DATADOMAIN5_", self.datadomain_dict, str(attr),
                                               s.attributes['oe:value'].value)

        self.networker_servers = list(self.networker_dict.values())
        logging.info("Setting Networker details as " + str(self.networker_servers))

        self.datadomain_servers = list(self.datadomain_dict.values())
        logging.info("Setting DataDomain details as " + str(self.datadomain_servers))

        logging.info('Completed Parsing Host Parameters...')
        return

    def set_ovaparameters_to_dict(self, key, dict, attr_name, attr_value):
        name = attr_name.replace(key, "").replace("_", "").lower()
        key = key.replace("_", "").lower()
        if key in dict:
            dict[key].update({name: attr_value})
        else:
            dict[key] = {name: attr_value}

    def parseinput(self):
        logging.info('Reading and Parsing Input Contents...')

        self.parsehostparameters()

        if os.path.isfile(BACKUP_CONFIG_FILE_PATH):
            self.__fill_config__(BACKUP_CONFIG_FILE_PATH, self.itemlist, BACKUP_KEYS)
            self.__fill_config_networker__(BACKUP_CONFIG_FILE_PATH, self.itemlist)
        if os.path.isfile(MIDDLEWARE_CONFIG_FILE_PATH):
            self.__fill_config__(MIDDLEWARE_CONFIG_FILE_PATH, self.itemlist, MIDDLEWARE_KEYS)
        if os.path.isfile(WORKER_CONFIG_FILE_PATH):
            self.__fill_config__(WORKER_CONFIG_FILE_PATH, self.itemlist, WORKER_KEYS)

        logging.info('Completed Parsing Input Contents...')
        return

    def __search_key__(self,key_name, key_list):
        try:
            key_value = dict(key_list)[key_name]
        except KeyError as e:
            return None, None

        return key_name, key_value

    def __fill_config__(self, config_file_path, xml_nodes, keys_list):
        with open(config_file_path, 'r') as conf:
            config_file = yaml.load(conf)

        for s in xml_nodes:
            attr = s.attributes['oe:key'].value
            val = s.attributes['oe:value'].value

            key_name, key_section = self.__search_key__(str(attr), keys_list)
            if key_name:
                key_value = s.attributes['oe:value'].value
                config_file[key_section][key_name] = key_value
                logging.info("Setting " + key_name + " as " + key_value)

        with open(config_file_path, 'w') as conf:
            conf.write(yaml.dump(config_file, default_flow_style=False))

    def __fill_config_networker__(self, config_file_path, xml_nodes):
        with open(config_file_path, 'r') as conf:
            config_file = yaml.load(conf)

        config_file["networker_server_details"]["NETWORKER_SERVERS"] = self.networker_servers
        config_file["networker_server_details"]["DATADOMAIN_SERVERS"] = self.datadomain_servers

        with open(config_file_path, 'w') as conf:
            conf.write(yaml.dump(config_file, default_flow_style=False))

    def sethostname(self):
        cmd = "echo " + self.hostname + " > /etc/hostname "
        logging.info("Setting hostname running command : " + cmd)
        os.system(cmd)
        return

    def setip(self):
        logging.info("Setting IP address in /etc/sysconfig/network-scripts/ifcfg-ens160")
        cmd1 = "echo IPADDR=" + self.ip_address + " >> /etc/sysconfig/network-scripts/ifcfg-ens160"
        cmd2 = "echo NETMASK=" + self.subnet_mask + " >> /etc/sysconfig/network-scripts/ifcfg-ens160"
        cmd3 = "echo GATEWAY=" + self.default_gateway + " >> /etc/sysconfig/network-scripts/ifcfg-ens160"
        os.system(cmd1)
        os.system(cmd2)
        os.system(cmd3)
        logging.info("Updating the DNS entry in /etc/resolv.conf")
        cmd1 = "echo nameserver " + self.primary_dns + " >>  /etc/resolv.conf"
        os.system(cmd1)
        return

    def checkip(self):
        logging.info("IP Address "+socket.gethostbyname(socket.gethostname())+" is active on the VM, "+ socket.gethostname())
        return

    def setproxy(self):
        cmd1 ="echo \'http_proxy=\"http://" + self.http_proxy + ":" + self.http_proxy_port + "\"\' >> /etc/environment"
        cmd2 ="echo \'https_proxy=\"https://" + self.http_proxy + ":" + self.http_proxy_port + "\"\' >> /etc/environment"
        logging.info("Running command :" + cmd1 )
        os.system(cmd1)
        logging.info("Running command :" + cmd2 )
        os.system(cmd2)
        return

    def set_bbclient_toml(self, toml_file_path):
        with fileinput.FileInput(toml_file_path, inplace=True) as toml_file:
            for line in toml_file:
                print(line.replace("$1", str(self.bbserver_ip)).replace("$2", str(self.bbserver_port))
                      .replace("$3", str(self.tenant_id)).replace("$4", str(self.ip_address)), end='')

#Main Body
if __name__ == "__main__":
    service = sys.argv[1]

    statefilename = '/home/tas/firstboot'
    filename = '/tmp/ova_env.xml'


    logging.info("Saving inputs to " + filename)
    cmd = "vmtoolsd --cmd \"info-get guestinfo.ovfenv\" > " + filename
    logging.info("Running command :  " + cmd)
    os.system(cmd)

    ova_manager = OVAManager(filename)

    if os.path.isfile(statefilename):
        logging.info("Starting the Firstboot Configurations...")

        #Update config.yaml
        ova_manager.parseinput()

        # Perform Ova configurations
        ova_manager.sethostname()
        ova_manager.setip()
        #Commenting proxy as we dont have in OVA form
        #ova_manager.setproxy()

        # set BB Client toml fie
        if os.path.isfile(BACKUP_CONFIG_FILE_PATH):
            ova_manager.set_bbclient_toml("/etc/bridgeburner/client/bridgeburner.toml")

        # Remove Firstboot file once all First Boot Configurations are completed
        os.remove(statefilename)

        logging.info("Completed all First Boot Ova Configurations; Preparing to reboot")
        os.system("cat /dev/null > ~/.bash_history")

        os.system("reboot")

    else:
        logging.info("Starting the Subsequent Boot Configurations...")
        ova_manager.checkip()