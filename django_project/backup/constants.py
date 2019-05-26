# Salt ping retries count.
SALT_PING_NO_OF_RETRIES = 4
# Salt ping retries timeout on saltmaster in seconds.
SALT_PING_RETRIES_TIMEOUT = 60
# Salt ping retries count to check job is running.
SALT_JOB_RUNNING_RETRIES = 3
# Salt ping retries timeout on saltmaster in seconds.
SALT_JOB_RETRIES_TIMEOUT = 60

## Network APIs
NW_CLIENT_URL = '/nwrestapi/v2/global/clients/'

INSTALL_NETWORKER_RESPONSE_STEPS = {
    0: "Process to copy networker agent "
       "package on the VM failed due to : ",
    1: "Process to install networker agent "
       "package on the VM failed due to : ",
    2: "Process to start the networker "
       "service on the VM failed due to : ",
    3: "Process to enable auto start in windows "
       "service on the VM failed due to : "
}

CLEANUP_NETWORKER_RESPONSE_STEPS = {
    0: "BACKUP022_NW_DD_ENTRY_REMOVE_ERROR",
    1: "BACKUP023_FILE_CLEANUP_ERROR",
    2: "BACKUP024_NW_UNINSTALL_ERROR"
}

COMMENT_NETWORKER_RESPONSE_STEPS = {
    0: "BACKUP025_NW_DD_ENTRY_REMOVE_ERROR"
}


BACKUP_ERRORS = {
    "BACKUP001_SALT_CONNECTION_ERROR": "",
    "BACKUP002_NETWORKER_AGENT_RPM_COPY_FAILURE": "Networker agent installation rpm copy to minion VM failed",
    "BACKUP003_NETWORKER_AGENT_INSTALL_FAILURE": "Installation of networker agent on minion VM failed",
    "BACKUP004_NETWORKER_AGENT_SERVICE_START_FAILURE": "Starting of networker agent service failed",
    "BACKUP005_GET_MINION_IP_FAILED": "Uable to get ip of minion VM",
    "BACKUP006_ADD_DNS_HOST_ENTRY_FAILURE": "Adding DNS host entry failed",
    "BACKUP007_NO_NETWORKER_SELECTED": "No Networker server available to process this request. "
                                       "Please Contact your administrator",
    "BACKUP008_INVALID_RETENTION_PERIOD": "Invalid retention period type. Currently the supported value is 'Day'",
    "BACKUP009_PG_NOT_FOUND": "Invalid retention period. Currently the supported values are '15 Day' and '30 Day'",
    "BACKUP010_CHECK_HOSTNAME": "Please check the hostname you have entered. "
                                "In case the hostname is correct, please contact your administrator",
    "BACKUP011_CLIENT_NOT_CONFIGURED": "Backup is not enabled for this VM",

    "BACKUP012_UNKNOWN_SALT_API_RESPONSE": "Response received after executing the "
                                           "salt net api command is not proper",
    "BACKUP013_SALT_CONFIGURATION_ISSUE": "unable to apply states on VM. "
                                          "check salt-master configurations.",
    "BACKUP014_DNS_ENTRY_FAILURE": "Unable to add DNS entry",
    "BACKUP015_SALT_EXECUTION_ERROR": "Response received after executing the salt net api command is not proper",
    "BACKUP016_CLIENT_INFORMATION_NOT_FOUND": "Unable to find VM details from Backup Server."
                                       " Please contact administrator.",
    "BACKUP017_PAUSE_SERVICE_FAILURE": "Action to Pause backup service for the VM failed.",
    "BACKUP018_RESUME_SERVICE_FAILURE": "Action to Resume backup service for the VM failed.",
    "BACKUP019_DISABLE_SERVICE_FAILURE": "Action to Disable backup service for the VM failed.",
    "BACKUP020_DECOMMISSION_SERVICE_FAILURE": "Action to Decommission backup service for the VM failed.",
    "BACKUP500_INTERNAL_SERVER_ERROR": "Unexpected error occurred."
                                       " Please contact administrator.",
    "BACKUP021_EMPTY_RESPONSE": "Response is Empty",
    "BACKUP022_NW_DD_ENTRY_REMOVE_ERROR": "Process to delete NW and DD entries on the VM failed due to : ",
    "BACKUP023_FILE_CLEANUP_ERROR": "Process to delete NW Files on the VM failed due to : ",
    "BACKUP024_NW_UNINSTALL_ERROR": "Process of uninstalling NW on VM failed due to : ",
    "BACKUP025_NW_DD_ENTRY_REMOVE_ERROR": "Process to commenting Minion host entry on the networker failed due to : ",
}

