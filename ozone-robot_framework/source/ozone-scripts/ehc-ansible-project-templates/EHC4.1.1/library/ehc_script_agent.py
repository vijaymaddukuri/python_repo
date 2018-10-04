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

import redis
import json
import uuid
import os

DOCUMENTATION = '''
---
module: ehc_script_agent
short_description: Send and received Redis Pub Sub
description: 
  - Send and received Redis Pub Sub
version_added: 2.2
author: Mumshad Mannambeth @mmumshad
notes: null
requirements: null
options: 
  package_name: 
    description: Package Name
    required: True
  module_name: 
    description: Module Name
    required: True
  method_name: 
    description: Method Name
    required: True
  method_params: 
    description: Method Parameters
    required: True
  redis_timeout:
    description: Timeout to wait for messages back from Script Agent
    required: False
  redis_host:
    description: Redis Server Host
    required: False
  redis_port:
    description: Redis Server Port
    required: False
  redis_password:
    description: Redis Password
    required: False
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

def main():
    module = AnsibleModule(
        argument_spec = dict(
            # <--Begin Parameter Definition -->
            package_name=dict(required=True),
            module_name=dict(required=True),
            method_name=dict(required=True, type='str'),
            method_params=dict(required=True, type='dict'),
            no_log=dict(required=False, default=False),
            redis_timeout=dict(required=False, default=3600),
            redis_password=dict(required=False),
            redis_host=dict(required=False, default='localhost'),
            redis_port=dict(required=False, default='6379'),
            # <--END Parameter Definition -->
        )
        # <--Begin Supports Check Mode -->
        # <--End Supports Check Mode -->
    )

    # <--Begin Retreiving Parameters  -->
    package_name = module.params['package_name']
    module_name = module.params['module_name']
    method_name = module.params['method_name']
    method_params = module.params['method_params']
    no_log = module.params['no_log']
    redis_timeout = module.params['redis_timeout']
    redis_host = module.params['redis_host']
    redis_port = module.params['redis_port']
    redis_password = os.getenv('OZONE_REDIS_PASSWORD')
    # <--End Retreiving Parameters  -->
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
        p = r.pubsub()

        unique_id = uuid.uuid4()

        p.subscribe('python:results:' + str(unique_id))
        run_data = {
            'module_name': package_name + "." + module_name,
            'method_name': method_name,
            'method_params': method_params,
            'unique_id': str(unique_id),
            'no_log': no_log
        }
        r.publish('python:run', json.dumps(run_data))

        for message in p.listen():
            if message['type'] == 'message':
                p.close()
                try:
                    json_data = json.loads(message['data'])
                except Exception as e:
                    json_data = "Unable to convert data to json format"

                if json_data and isinstance(json_data, dict) and 'exitCode' in json_data and json_data['exitCode'] > 0:
                    module.fail_json(msg=json_data['traceback'], data=json_data)

                module.exit_json(msg=message, data=json_data)

        # message = p.get_message(timeout=int(redis_timeout))
        # p.close()
        # try:
        #     json_data = json.loads(message['data'])
        # except Exception as ex:
        #     json_data = "Unable to convert data to json format - %s" % ex
        #
        # if json_data and isinstance(json_data, dict) and 'exitCode' in json_data and json_data['exitCode'] > 0:
        #     module.fail_json(msg=json_data['traceback'], data=json_data)
        #
        # if json_data and isinstance(json_data, dict) and 'err_message' in json_data:
        #     module.fail_json(msg=json_data['err_message'], data=json_data)
        #
        # module.exit_json(msg=message, data=json_data)

        # Successfull Exit

    except Exception as e:
        # Fail Exit
        module.fail_json(msg="Error Message - %s" % str(e),redis_timeout=redis_timeout)


from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
