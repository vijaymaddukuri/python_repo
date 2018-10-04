#!/usr/bin/python

# ------------------------------------------------------------------------------
# Copyright (C) 2016-2017 DELL EMC Corporation. All Rights Reserved.

# This software contains the intellectual property of DELL EMC Corporation
# or is licensed to DELL EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of DELL  EMC.

# ------------------------------------------------------------------------------

try:
    import json
except ImportError:
    import simplejson as json

import os
import yaml
import pydevd
import errno
import filelock

DOCUMENTATION = '''
---
module: update_vars
short_description: Update vars file dynamically.
description: 
  - Update vars file dynamically to persist data. Only simple data structure is supported. Complex data structure not supported.
version_added: 2.2
author: Mumshad Mannambeth, @mmumshad
notes: null
requirements: null
options: 
  vars_file: 
    description: Vars file name
    required: True
  update_type: 
    description: Update type
    required: True
    choices: ["set","add","remove","addUnique"]
  base_data_path: 
    description: Base data path to add data to
  data: 
    description: Data to update
    required: True
  create_file: 
    description: Create file if it does not exist
  unique_data: 
    description: Unique data to check in case of 'addUnique'               
'''

EXAMPLES = '''
# Example
module_name:
    parameter1: value1
    parameter2: value2
    parameter3:
        key1: value1
        key2: value2
'''


def get_base_object(data, base_data_path):

    if not base_data_path:
        return data, None

    for path in base_data_path.split(".")[:-1]:
        if isinstance(data, list):
            raise Exception('Data is a list - %s' % data)
        if path not in data:
            data[path] = {}
        data = data[path]

    return data, base_data_path.split(".")[-1]


def dictionary_not_match(data, filter_to_match):

    if not filter_to_match.keys():
        return True

    match = True
    for (key, value) in filter_to_match.iteritems():
        if data[key] != value:
            match = False

    return not match

def main():
    module = AnsibleModule(
        argument_spec = dict(
            # <--Begin Parameter Definition -->
            vars_file=dict(required=True),
            update_type=dict(required=True,type='str',choices=["set","add","remove","addUnique"]),
            base_data_path=dict(type='str'),
            data=dict(required=True,type='str'),
            create_file=dict(type='bool'),
            unique_data=dict(type='dict')
            # <--END Parameter Definition -->
        )
        # <--Begin Supports Check Mode -->
        # <--End Supports Check Mode -->
    )

    # <--Begin Retreiving Parameters  -->
    vars_file = module.params['vars_file']
    update_type = module.params['update_type']
    base_data_path = module.params['base_data_path']
    data = module.params['data']
    create_file = module.params['create_file']
    unique_data = module.params['unique_data']
    # <--End Retreiving Parameters  -->

    base_dir = os.getcwd()

    try:
        data = json.loads(data.replace("'",'"'))
    except Exception as e:
        pass
    
    lock = filelock.FileLock(vars_file + ".lck")
    
    
    try:
        with lock.acquire(timeout = 10):
            if vars_file:
                if os.path.isfile(vars_file):
                    fd = open(vars_file, 'rb')
                    buffer = fd.read()
                    fd.close()
                    yamlData = yaml.safe_load(buffer.decode('utf-8'))
                else:
                    if create_file:
                        yamlData = {}
                    else:
                        raise Exception("File Not Found at path %s" % (base_dir + "/" + vars_file))
            else:
                raise Exception("Variable file not found %s" % vars_file)
    
    
            if not base_data_path:
                yamlData = data
            else:
    
                if not yamlData:
                    yamlData = {}
    
                data_to_update, key = get_base_object(yamlData, base_data_path)
    
                if update_type == 'set':
                    data_to_update[key] = data
                elif update_type == 'add':
    
                    if not key in data_to_update:
                        data_to_update[key] = []
    
                    if not isinstance(data_to_update[key], list):
                        raise Exception("Cannot add as Variable is not an array. Current Value - %s" % (data_to_update[key]))
    
                    data_to_update[key].append(data)
                
                elif update_type == 'addUnique':
    
                    if not unique_data:
                        raise Exception("parameter unique_data is required with addUnique")
    
                    if not key in data_to_update:
                        data_to_update[key] = []
    
                    if not isinstance(data_to_update[key], list):
                        raise Exception("Cannot add as Variable is not an array. Current Value - %s" % (data_to_update[key]))
    
                    # data_to_update[key] = filter(lambda item:dictionary_match(item, unique_data) , data_to_update[key])
    
                    data_to_update[key] = [item for item in data_to_update[key] if dictionary_not_match(item, unique_data)]
    
                    data_to_update[key].append(data)
                    
                elif update_type == 'remove':
                    if not key in data_to_update:
                        raise Exception("Data path not found- No %s in %s" % (key, data_to_update))
    
                    if not isinstance(data_to_update[key], list):
                        raise Exception("Cannot remove as Variable is not an array. Current Value - %s" % (data_to_update[key]))
    
                    data_to_update[key].remove(data)
    
            if not os.path.exists(os.path.dirname(vars_file)):
                try:
                    os.makedirs(os.path.dirname(vars_file))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
    
            # Update file
            fd = open(vars_file, 'wb')
            fd.write(yaml.safe_dump(yamlData, default_flow_style=False, explicit_start=True, width=1000))
            fd.close()
            # Successfull Exit
            module.exit_json(changed=True, msg=yamlData)
    except Exception as e:
        module.fail_json(msg="Error updating good configuration - Error Message - %s" % e)

    # Fail Exit
    module.fail_json(msg="Error updating good configuration. No update made.")


from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
