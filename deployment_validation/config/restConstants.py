import os.path


VM_TEMPLATES='api/v1/vm_templates/'
VIJAY_POLICIES='api/v1/VIJAY_policies/'

# Backup service APIs
TAS_API_HEALTH_CHECK = 'http://{}:8000/api/v1/healthcheck'
TAS_API_ENABLE_BACKUP = 'http://{}:8000/api/v1/backup/enable'
TAS_API_DISABLE_BACKUP = 'http://{}:8000/api/v1/backup/disable'
TAS_API_ENABLE_SECURITY = 'http://{}:8000/api/v1/security/enable'
TAS_API_ENABLE_MONITORING = 'http://{}:8000/api/v1/monitoring/enable'
API_NETWROKER_VERSION = 'https://{}:9090/nwrestapi'
API_CONSUL_SERVICE = 'http://{}:{}/v1/agent/services'


# Middleware Enable Backup API
MIDDLEWARE_API_ENABLE_BACKUP = 'http://{}:8000/api/v1/service/backup/enable'

# Middleware Header
JSON_HEADER = {'Accept': "application/json", 'Content-Type': "application/json"}

# Middleware Enable Security
MIDDLEWARE_API_ENABLE_SECURITY = 'http://{}:8000/api/v1/service/security/enable'

# Middleware Enable Monitoring
MIDDLEWARE_API_ENABLE_MONITORING = 'http://{}:8000/api/v1/service/monitoring/enable'

# Middleware Enable Vulnerability
MIDDLEWARE_API_ENABLE_VULNERABILITY = 'http://{}:8000/api/v1/service/vulnerability/scan'

# Middleware Health Check
MIDDLEWARE_API_HEALTH_CHECK = 'http://{}:8000/api/v1/healthcheck'

# Middleware Header
VUNERABILITY_JSON = {'Accept': "application/json", 'Content-Type': "application/json"}

# TAS Requests
TAS_BACKUP_REQUEST = "curl -X POST \"%s\" -H \"accept: application/json\" -H \"Content-Type: application/json\" " \
               "-d \"{\\\"hostName\\\": \\\"%s\\\", \\\"retentionPeriod\\\": %d, " \
                  "\\\"retentionPeriodType\\\": \\\"%s\\\"}\""

TAS_SECURITY_REQUEST = "curl -X POST \"%s\" -H \"accept: application/json\" -H \"Content-Type: application/json\" " \
                  "-d \"{\\\"LinuxPolicyID\\\": \\\"%s\\\", \\\"WindowsPolicyID\\\": \\\"%s\\\", " \
                       "\\\"VirtualMachineHostName\\\": \\\"%s\\\", \\\"VirtualMachineIPAddress\\\": \\\"%s\\\"}\""

TAS_MONITORING_REQUEST = "curl -X POST \"%s\" -H \"accept: application/json\" -H \"Content-Type: application/json\" " \
               "-d \"{\\\"VirtualMachineID\\\": \\\"%s\\\", " \
                  "\\\"VirtualMachineHostName\\\": \\\"%s\\\", \\\"VirtualMachineIPAddress\\\": \\\"%s\\\"}\""

# Salt Master Connectivity
SALT_MASTER_CONNECTIVITY = "curl -si {ip}:{port}/login -H \"accept: application/json\" -d username='{user}' -d password='{pwd}' -d eauth='pam'"

# Upload File
UPOAD_FILE_USING_CURL = "sudo curl --insecure --user {User}:{Password} -T {localFilePath} sftp://{IP}:{remoteFilePath}"

