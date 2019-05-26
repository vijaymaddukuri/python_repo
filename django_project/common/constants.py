CONFIG_FILE_PATH = "config.yaml"

LOG_FILENAME = "salt.log"

WAIT_TIME_BETWEEN_REQUESTS = 3  # in seconds

KEY_SALT_MASTER = "salt_master_details"
KEY_NETWORKER_SERVER = "networker_server_details"
KEY_NETWORKER_CLIENT = "networker_client_details"
KEY_TRENDMICRO_CLIENT = "trendmicro_client_details"
KEY_TRENDMICRO_SERVER = "trendmicro_server_details"
KEY_NIMSOFT_CLIENT = "nimsoft_client_details"
KEY_NIMSOFT_SERVER = "nimsoft_server_details"
KEY_SALT_RETRY_CONFIG_VALUES = "salt_retries_config_values"
WORKER_PROCS = "workers"
HUB_NAME = "NIMSOFT_HUB_NAME"
REQUEST_TIMEOUT = "request_timeout_details"

# Grain data to upload into minion
GRAIN_DATA = {}

VM_TEMPLATE = {}

# Backup Service Error Messages
BACKUP_SERVICE_ERRORS = {
    500: "Unexpected error occurred. Please contact administrator.",
    401: "You are unauthorized to make this request.",
    404: "Resource doesn't exist",
    "PG_NOT_FOUND": "Invalid retention period."
                    " Currently the supported values are '15 Day' and '30 Day'",
    "CHECK_HOSTNAME": "Please check the hostname you have entered. "
                      "In case the hostname is correct, please contact your administrator",
    "SYNC_FAILURE": "Unable to sync files on the Client VM.",
    "CLIENT_NOT_CONFIGURED": "Backup is not enabled for this VM",
    "INVALID_TYPE": "Invalid retention period type. Currently the supported value is 'Day'",
    "NO_NETWORKER": "No Networker server available to process this request. Please Contact your administrator"
}
# salt error messages
SALT_MINION_ERRORS = {
    "CHECK_JOB": "Another job has been running for a while please try after some other time ",
    "NO_JOB_ON_MINION": "No job is running on machine, ready to do a job on minion",
    "STATE_RUNNING": "The function 'state.apply' is running already, please wait for some time",
    "MINION_CONNECTION": 'Unable to connect to the Client VM. Please ensure the machine is up'
                         ', configured with the salt master and minion service is running.',
    "LOGIN": 'Unable to establish connection with the salt master machine. '
             'Please ensure the machine is up and '
             'Salt Master/Salt NetApi services are running.',
    "FETCH_KERNEL": "Unable to fetch the kernel type, response return object is empty"
}

# salt master errors
SALT_MASTER_ERROR = {
    'SALT001_CONNECTION_ERROR': 'Unable to establish connection with the salt master '
                                'machine. Please ensure the machine is up and Salt '
                                'Master/Salt NetApi services are running.',
    'SALT002_LOGIN_ERROR': 'Unable to login to the salt master '
                           'machine with the given username and password',
    'SALT003_EMPTY_MINION_RESPONSE': "Unable to fetch the Minion name, response return object is empty",
    'SALT004_MINION_NOT_RESPONDING': "Minion is not responding to Master, "
                                     "please Check if salt minion service is up and running."
}

# CMDS Constants.
TAS_SVC_CHECK_CMD = "systVIJAYtl status tas.service | grep Active | grep -v grep | awk '{print $2}'"
TAS_NO_OF_PROCESSES = "systVIJAYtl status tas.service | grep ONBFactory.wsgi | grep -v grep | wc -l"

# Log Configurations
MONITORING_LOG_ID = "|*MONITORING_APP*|"
BACKUP_LOG_ID = "|*BACKUP_APP*|"
SECURITY_LOG_ID = "|*SECURITY_APP*|"
