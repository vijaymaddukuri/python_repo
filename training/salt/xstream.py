# Import Python Libs
from __future__ import absolute_import
import os
import time
import json
import pprint
import logging
import decimal
from practice import yaml_script
# Import Salt Libs
import salt.utils.cloud
import salt.config as config
from salt.exceptions import (
    SaltCloudConfigError,
    SaltCloudNotFound,
    SaltCloudSystemExit,
    SaltCloudExecutionFailure,
    SaltCloudExecutionTimeout
)
from salt.ext.six import string_types

# Import Third Party Libs
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Import 3rd-party libs
import salt.ext.six as six

# Get logging started
log = logging.getLogger(__name__)

__virtualname__ = 'xstream'

request_header = {'Accept': "application/json", 'Content-Type': "application/json"}

# Only load in this module if the DIGITAL_OCEAN configurations are in place
def __virtual__():
    '''
    Check for DigitalOcean configurations
    '''
    if get_configured_provider() is False:
        return False


    return __virtualname__


def get_configured_provider():
    '''
    Return the first configured instance.
    '''
    print("get_config")
    return config.is_provider_configured(
        __opts__,
        __active_provider_name__ or __virtualname__,
        ('url','password','user',)
    )

def get_value_from_provider(item):
    return config.get_cloud_config_value(item,
                    get_configured_provider(),__opts__, search_global=False)

def get_value_from_profile(item, vm_object):
    return config.get_cloud_config_value(
       item, vm_object, __opts__, default=None
   )

def authenticate(kwargs = None,call=None):
    user = get_value_from_provider('user')
    passwd = get_value_from_provider('password')
    host = get_value_from_provider('url')
    url = "https://%s/api/v1.3/Auth" % (host)
    response = requests.post(url,
                           json = {"username": user, "password": passwd},
                           headers = request_header,
                           verify=False)
    token = response.json().get('Token', None)
    return response


def check_vm_name_exists(vm_name):
    list_vms = []
    auth_code = authenticate()
    auth_json = auth_code.json()
    if auth_code.ok:
        print auth_json.get('TenantID', None)
        filter_query = "?$filter=IsRemoved eq false and IsTemplate eq false and TenantID eq '"+ str(auth_json.get('TenantID', None))+ "'"
        filter_query += "&$select=CustomerDefinedName"
        print("######################3")
        print filter_query
        host = get_value_from_provider('url')
        url = "https://%s/api/v1.3/VirtualMachine/" + filter_query % (host)
        request_header["Authorization"] = str('Bearer %s' % auth_json.get('Token', None))
        response = requests.get(url,
                                headers=request_header, verify=False)
        list_dic_vms = response.json()
        list_vms_names = [ a_vm["CustomerDefinedName"] for a_vm in list_dic_vms if "CustomerDefinedName" in a_vm]
        if vm_name in list_vms_names:
            return True
        else:
            return False
    return False

def create(vm_):
    #vm_name=get_value_from_provider('vmHost')
    vm_name = config.get_cloud_config_value(
        'name', vm_, __opts__, default=None)
    auth_code = authenticate()
    auth_json= auth_code.json()
    host = get_value_from_provider('url')
    with open(r'/etc/salt/cloud.profiles.d/profile.conf', 'r') as yml:
        output = yaml_script.load(yml)
    #post_data = json.dumps(output)
    output['xstream-centos']['vm_template']['CustomerDefinedName']=vm_name
    #post_data= json.dumps(output['xstream-centos']['vm_template'])
    post_data= output['xstream-centos']['vm_template']
    request_header["Authorization"] = str('Bearer %s' % auth_json.get('Token', None))
    print post_data
    print request_header
    if auth_code.ok:
        url = "https://%s/api/v1.3/VirtualMachine/SetVM" % (host)
        response = requests.post(url,
                                 headers=request_header,
                                 json=post_data,
                                 verify=False)
    print response.text
    return {'vm': vm_name}




def create_vm_on_xstream(kwargs = None,call=None):
    print kwargs.get('host')
    auth_code = authenticate()
    auth_json= auth_code.json()
    host = get_value_from_provider('url')
    with open(r'/etc/salt/cloud.profiles.d/profile.conf', 'r') as yml:
        output = yaml_script.load(yml)
    #post_data = json.dumps(output)
    output['xstream-centos']['vm_template']['CustomerDefinedName']=kwargs.get('host')
    #post_data= json.dumps(output['xstream-centos']['vm_template'])
    post_data= output['xstream-centos']['vm_template']
    request_header["Authorization"] = str('Bearer %s' % auth_json.get('Token', None))
    print post_data
    print request_header
    if auth_code.ok:
        url = "https://%s/api/v1.3/VirtualMachine/SetVM" % (host)
        response = requests.post(url,
                                 headers=request_header,
                                 json=post_data,
                                 verify=False)
    print response.text
    return kwargs

