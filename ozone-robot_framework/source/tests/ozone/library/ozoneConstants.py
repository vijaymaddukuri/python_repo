# -*- coding: utf-8 -*-

#
class OSType(object):
    LINUX, WINDOWS = range(2)

REMOTE_EXECUTION_PARAMS = {
    'orch_vm': {
        'tmpdir': 'C:\\ehc',
        'prefix': 'EHCAutoPrefix',
        'suffix': 'EHCAutoSuffix',
        'encoding': 'utf-8'
    },
    'execution_vm': {
        OSType.LINUX: {
            'tmpdir': '/tmp',
            'prefix': 'EHCAutoPrefix',
            'suffix': 'EHCAutoSuffix',
        },
        OSType.WINDOWS: {
            'tmpdir': 'C:\\ehc',
            'prefix': "EHCAutoPrefix",
            'suffix': "EHCAutoSuffix",
        },
    },
}

REMOTE_SHELL_PATH = {
    OSType.LINUX: {
        'shell': '/bin/sh',
    },
    OSType.WINDOWS: {
        'shell': 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe',
        'shell_encoding': 'utf-16',
    },
}

#Pick up latest Ozone ova build
OVAPREFIX='EHC-Automation-Tool-dev-build-'
OVASUFFIX='.ova'
OVA_DEPLOY_TIMEOUT = 30 * 60

#Get Ozone token
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json, application/octet-stream'}
OZONE_AUTH_URL = 'auth/local'

#Configure Ozone worker VM
FILE_NAME='bat/configureAgent2.bat'
REMOTE_FILE_PATH=r'C:\Users\Administrator\Desktop\configureAgent2.bat'
SUCCESS_MESSAGE_AGENT='Agent Started'

#Create project in Ozone
OZONE_PROJECT_URL = 'api/projects'

#Config user Password
CONFIG_USER_PASSWORD_BODY = {
    "oldPassword": "",
    "newPassword": ""
}

#config master password
CONFIG_MASTER_PASSWORD_BODY = {"masterPassword": ""}
OZONE_CONFIG_URL = 'api/system/password'
OZONE_VERIFY_URL = 'api/system/password/isset'

#start service
OZONE_SERVICE_URL = "api/system/services/start"

#Get id by user name
OZONE_USER_URL = "api/users"

#Validate system in Ozone
OZONE_SYSTEM_URL='api/system/services'
OZONE_SYSTEM_AGENT_URL='api/system/agent'

#upload input template
OZONE_UPDATE_VAR='api/projects/update_ansible_variable_files'

#execute ansible job
OZONE_ANSIBLE_DATA = {
        'type': '',
        'refid': '',  # Project ID + Playbook name
        'project': '',
        # use tags to specify task to run
        # NOTE: all tasks must be tagged and all tags to run must be specified here. Else task won't run.
        'tags': '',
        # List all hosts to limit execution to. Note: Lists all hosts involved here.  This is list from inventory file.
        'limit_to_hosts': '',
        'verbose': 'verbose',
        'check_mode': 'No_Check'}

OZONE_EXECUTE_ANSIBLE_JOB='api/ansible/execute'
OZONE_GET_ANSIBLE_JOB='api/ansible/'

