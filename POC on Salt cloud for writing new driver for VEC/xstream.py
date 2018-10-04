# Import Python Libs
from __future__ import absolute_import
import os
import time
import json
import pprint
import logging
import decimal
import yaml
import re
import time
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
    '''
	Search for the key in the provider file and returns the value
	'''
    return config.get_cloud_config_value(item,
                    get_configured_provider(),__opts__, search_global=False)

def get_value_from_profile(item, vm_object):
    '''
	Search for the key in the profile file and returns the value
	'''
    return config.get_cloud_config_value(
       item, vm_object, __opts__, default=None
   )

def authenticate(kwargs = None,call=None):
    '''
	Connects to the xstream and get the bearer authentication JSON ouput
	'''
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
    '''
	Returns True, if VM not exists in the Xstream, else returns False
	'''
    list_vms = []
    auth_code = authenticate()
    auth_json = auth_code.json()
    print(auth_json)
    if auth_code.ok:
        print auth_code.get('TenantID', None)
        filter_query = "?$filter=IsRemoved eq false and IsTemplate eq false and TenantID eq '"+ str(auth_json.get('TenantID', None))+ "'"
        filter_query += str("&$select=CustomerDefinedName")
        print("######################3")
        print filter_query
        host = str(get_value_from_provider('url'))
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

def script(vm_):
    '''
    Return the script deployment object
    '''
    script_name = config.get_cloud_config_value('script', vm_, __opts__)
    if not script_name:
        script_name = 'bootstrap-salt'

    return salt.utils.cloud.os_script(
        script_name,
        vm_,
        __opts__,
        salt.utils.cloud.salt_config_to_yaml(
            salt.utils.cloud.minion_config(__opts__, vm_)
        )
    )


def create(vm_):
    '''
	Create the VM on the Xstream, by fetching the template info from profiles file.
	'''
    __utils__['cloud.fire_event'](
        'event',
        'starting create',
        'salt/cloud/{0}/creating'.format(vm_['name']),
        args=__utils__['cloud.filter_event']('creating', vm_, ['name', 'profile', 'provider', 'driver']),
        sock_dir=__opts__['sock_dir'],
        transport=__opts__['transport']
    )

    vm_name = config.get_cloud_config_value(
        'name', vm_, __opts__, default=None)

    folder = config.get_cloud_config_value(
        'folder', vm_, __opts__, default=None
    )
    datacenter = config.get_cloud_config_value(
        'datacenter', vm_, __opts__, default=None
    )
    resourcepool = config.get_cloud_config_value(
        'resourcepool', vm_, __opts__, default=None
    )
    cluster = config.get_cloud_config_value(
        'cluster', vm_, __opts__, default=None
    )
    datastore = config.get_cloud_config_value(
        'datastore', vm_, __opts__, default=None
    )
    host = '10.100.249.55'
    template = config.get_cloud_config_value(
        'template', vm_, __opts__, default=False
    )
    num_cpus = config.get_cloud_config_value(
        'num_cpus', vm_, __opts__, default=None
    )
    cores_per_socket = config.get_cloud_config_value(
        'cores_per_socket', vm_, __opts__, default=None
    )
    memory = config.get_cloud_config_value(
        'memory', vm_, __opts__, default=None
    )
    devices = config.get_cloud_config_value(
        'devices', vm_, __opts__, default=None
    )
    extra_config = config.get_cloud_config_value(
        'extra_config', vm_, __opts__, default=None
    )
    annotation = config.get_cloud_config_value(
        'annotation', vm_, __opts__, default=None
    )
    power = config.get_cloud_config_value(
        'power_on', vm_, __opts__, default=True
    )
    key_filename = config.get_cloud_config_value(
        'private_key', vm_, __opts__, search_global=False, default=None
    )
    deploy = config.get_cloud_config_value(
        'deploy', vm_, __opts__, search_global=True, default=True
    )
    wait_for_ip_timeout = config.get_cloud_config_value(
        'wait_for_ip_timeout', vm_, __opts__, default=20 * 60
    )
    domain = config.get_cloud_config_value(
        'domain', vm_, __opts__, search_global=False, default='local'
    )
    hardware_version = config.get_cloud_config_value(
        'hardware_version', vm_, __opts__, search_global=False, default=None
    )
    guest_id = config.get_cloud_config_value(
        'image', vm_, __opts__, search_global=False, default=None
    )
    customization = config.get_cloud_config_value(
        'customization', vm_, __opts__, search_global=False, default=True
    )
    customization_spec = config.get_cloud_config_value(
        'customization_spec', vm_, __opts__, search_global=False, default=None
    )
    win_password = config.get_cloud_config_value(
        'win_password', vm_, __opts__, search_global=False, default=None
    )
    win_organization_name = config.get_cloud_config_value(
        'win_organization_name', vm_, __opts__, search_global=False, default='Organization'
    )
    plain_text = config.get_cloud_config_value(
        'plain_text', vm_, __opts__, search_global=False, default=False
    )
    win_user_fullname = config.get_cloud_config_value(
        'win_user_fullname', vm_, __opts__, search_global=False, default='Windows User'
    )
    win_run_once = config.get_cloud_config_value(
        'win_run_once', vm_, __opts__, search_global=False, default=None
    )    
    auth_code = authenticate()
    auth_json= auth_code.json()
    host = get_value_from_provider('url')
    with open(r'/etc/salt/cloud.profiles.d/profile.conf', 'r') as yml:
        output = yaml.load(yml)
  
    output['xstream-centos']['vm_template']['CustomerDefinedName']=vm_name
    #post_data= json.dumps(output['xstream-centos']['vm_template'])
    post_data= output['xstream-centos']['vm_template']
    request_header["Authorization"] = str('Bearer %s' % auth_json.get('Token', None))

    print post_data

    if auth_code.ok:
        url = "https://%s/api/v1.3/VirtualMachine/SetVM" % (host)
        response = requests.post(url,
                                 headers=request_header,
                                 json=post_data,
                                 verify=False)
     
    
    time.sleep(60)
    ret = __utils__['cloud.bootstrap'](vm_, __opts__)
    salt.utils.cloud.minion_config(__opts__, vm_)
    return {'vm': vm_name}


def create_vm_on_xstream(kwargs = None,call=None):
    '''
	Create VM on xstream using providers file
	'''
    print kwargs.get('host')
    auth_code = authenticate()
    auth_json= auth_code.json()
    host = get_value_from_provider('url')
    with open(r'/etc/salt/cloud.profiles.d/profile.conf', 'r') as yml:
        output = yaml.load(yml)
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
