import os.path

VM_TEMPLATES='api/v1/vm_templates/'
VIRTUSTREAM_POLICIES='api/v1/virtustream_policies/'

# Backup service APIs
API_ENABLE_BACKUP = 'https://{}/api/v1/backup/enable'
API_DISABLE_BACKUP = 'https://{}/api/v1/backup/disable'

# Backup Service API header's
BACKUP_SERVICE_HEADER = {'Accept': "application/json",
                         'Content-Type': "application/json"}
API_NW_GET_CLIENTS = 'https://{}/nwrestapi/v2/global/clients?fl=hostname,protectionGroups'
NETWORKER_SERVER_HEADER = {'Content-Type': "application/json", 'Authorizaton':
    "Basic YWRtaW5pc3RyYXRvcjpQYXNzd29yZDEh"}
# Update the os.path usage
YAML_FILE_PATH = os.path.join(os.getcwd(), "conf\backup_service.yaml")


# Middleware Enable Backup API
MIDDLEWARE_ENABLE_BACKUP = 'https://{}/api/v1/service/backup/enable'
MIDDLEWARE_SERVICE_HEADER = {'Accept': "application/json", 'Content-Type': "application/json"}
