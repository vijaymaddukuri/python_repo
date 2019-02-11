import os.path


VM_TEMPLATES='api/v1/vm_templates/'
VIRTUSTREAM_POLICIES='api/v1/virtustream_policies/'

# Backup service APIs
API_HEALTH_CHECK = 'http://{}:8000/api/v1/healthcheck'
API_ENABLE_BACKUP = 'http://{}:8000/api/v1/backup/enable'
API_DISABLE_BACKUP = 'http://{}:8000/api/v1/backup/disable'
API_NW_GET_CLIENTS = 'https://{}:8000/nwrestapi/v2/global/clients?fl=hostname,protectionGroups'
API_ENABLE_SECURITY = 'http://{}:8000/api/v1/security/enable'
API_ENABLE_MONITORING = 'http://{}:8000/api/v1/monitoring/enable'
API_NETWROKER_VERSION = 'https://{}:9090/nwrestapi'
API_CONSUL_SERVICE = 'http://{}:{}/v1/agent/services'


# Backup Service API header's
BACKUP_SERVICE_HEADER = {'Accept': "application/json", 'Content-Type': "application/json"}
NETWORKER_SERVER_HEADER = {'Accept': 'application/json', 'Content-Type': 'application/json'}

# Middleware Enable Backup API
MIDDLEWARE_ENABLE_BACKUP = 'http://{}:8000/api/v1/service/backup/enable'

# Middleware Header
MIDDLEWARE_SERVICE_HEADER = {'Accept': "application/json", 'Content-Type': "application/json"}
VULNERABILITY_SERVICE_HEADER = {'Accept': "application/json", 'Content-Type': "application/json"}
CONSUL_SERVICE_HEADER = {'Accept': "application/json", 'Content-Type': "application/json"}

# Middleware Enable Security
MIDDLEWARE_ENABLE_SECURITY = 'http://{}:8000/api/v1/service/security/enable'

# Middleware Enable Monitoring
MIDDLEWARE_ENABLE_MONITORING = 'http://{}:8000/api/v1/service/monitoring/enable'

# Middleware Enable Vulnerability
MIDDLEWARE_ENABLE_VULNERABILITY = 'http://{}:8000/api/v1/service/vulnerability/scan'

# Middleware Health Check
MIDDLEWARE_HEALTH_CHECK = 'http://{}:8000/api/v1/healthcheck'

