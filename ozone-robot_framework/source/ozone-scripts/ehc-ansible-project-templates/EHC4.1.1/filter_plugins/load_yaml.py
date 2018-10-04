# ------------------------------------------------------------------------------
# Copyright (C) 2016-2017 DELL EMC Corporation. All Rights Reserved.

# This software contains the intellectual property of DELL EMC Corporation
# or is licensed to DELL EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of DELL  EMC.

# ------------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import yaml
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.listify import listify_lookup_plugin_terms


def load_yaml(yaml_string):
    '''
    - debug: msg="{{ lookup('file', '') | load_yaml }}"
    '''
    try:
        yaml_data = yaml.safe_load(yaml_string.decode('utf-8'))
    except Exception as ex:
        print("Error converting yaml data %s" % ex)
        return
    return yaml_data

class FilterModule(object):
    ''' load_yaml filter '''

    def filters(self):
        return {
            'load_yaml': load_yaml
        }