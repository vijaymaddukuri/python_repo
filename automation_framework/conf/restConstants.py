VM_TEMPLATES='api/v1/vm_templates/'
VIJAY_POLICIES='api/v1/VIJAY_policies/'

# Backup service APIs
API_ENABLE_BACKUP = 'http://{}/api/v1/backup/enable'
API_DISABLE_BACKUP = 'http://{}/api/v1/backup/disable'
API_NW_GET_CLIENTS = 'https://{}/nwrestapi/v2/global/clients' \
                     '?fl=hostname,protectionGroups'

MIDDLEWARE_ENABLE_BACKUP = 'http://{}/api/v1/service/backup/enable'

# Vulnerability Scan Service
API_TRIGGER_VULNERABILITY_SCAN = 'http://{}:{}/api/v1/service/' \
                                 'vulnerability/scan'
JSON_HEADER = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
REST_TIMEOUT = 30
API_VALIDATE_VULNERABILITY_SCAN = 'https://{}/api/3/scans/{}'

# TAS Security
TAS_API_ENABLE_SECURITY = 'http://{}:8000/api/v1/security/enable'
TAS_API_DECOMMISSION_SECURITY = 'http://{}:8000/api/v1/security/decommission'

# Middleware Security
MIDDLEWARE_API_ENABLE_SECURITY = 'http://{}:8000/api/v1/service/security/enable'
MIDDLEWARE_API_DECOMMISSION_SECURITY = 'http://{}:8000/api/v1/service/security/decommission'

# TAS Requests
TAS_SECURITY_REQUEST = "curl -i -X POST \"%s\" -H \"accept: application/json\" -H \"Content-Type: application/json\" " \
                  "-d \"{\\\"LinuxPolicyID\\\": \\\"%s\\\", \\\"WindowsPolicyID\\\": \\\"%s\\\", " \
                       "\\\"VirtualMachineHostName\\\": \\\"%s\\\", \\\"VirtualMachineIPAddress\\\": \\\"%s\\\", " \
                       "\\\"VirtualMachineID\\\": \\\"%s\\\", , \\\"VirtualMachineRID\\\": \\\"%s\\\", " \
                       "\\\"TaskID\\\": \\\"%s\\\"}\""
TAS_SECURITY_DECOMMISSION_REQUEST = "curl -i -X POST \"%s\" -H \"accept: application/json\" -H \"Content-Type: application/json\" " \
                  "-d \"{\\\"VirtualMachineHostName\\\": \\\"%s\\\", \\\"VirtualMachineIPAddress\\\": \\\"%s\\\", " \
                       "\\\"VirtualMachineID\\\": \\\"%s\\\", \\\"VirtualMachineRID\\\": \\\"%s\\\", " \
                       "\\\"TaskID\\\": \\\"%s\\\"}\""



# MOnitoring API
MW_ENABLE_MONITORING = 'http://{}:8000/api/v1/service/monitoring/enable'
TAS_ENABLE_MONITORING = 'http://{}:8000/api/v1/monitoring/enable'

# Config File Names in local conf Folder
MWS = 'mws.yaml'
BWS = 'bws.yaml'
TAS = 'tas.yaml'

