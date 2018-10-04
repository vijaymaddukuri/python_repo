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


def prepare_user_credentials(user_dict, ad_domain_name_with_backslash):
    '''
    - debug: msg="{{ user_dict | prepare_user_credentials(ad_domain_name_with_backslash) }}"
    '''
    result = {}
    for user, credential in user_dict.iteritems():
        result[ad_domain_name_with_backslash + credential ['username']] = credential['password']

    return result

class FilterModule(object):
    ''' Combine Dict in List '''

    def filters(self):
        return {
            'prepare_user_credentials': prepare_user_credentials
        }