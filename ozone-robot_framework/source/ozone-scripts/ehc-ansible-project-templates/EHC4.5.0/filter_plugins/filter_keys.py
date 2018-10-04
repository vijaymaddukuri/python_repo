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

import pydevd
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.listify import listify_lookup_plugin_terms


def filter_keys(data, keys):
    '''
    - debug: msg="{{ instance | filter_keys(keys) }}"
    '''
    result = {}
    for key, value in data.iteritems():
        if key in keys:
            result[key] = value

    return result

class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'filter_keys': filter_keys
        }