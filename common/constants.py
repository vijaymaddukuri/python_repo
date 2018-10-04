CONFIG_FILE_PATH = "config.yaml"

LOG_FILENAME = "salt.log"

WAIT_TIME_BETWEEN_REQUESTS = 3  # in seconds

KEY_XSTREAM = "xstream"
KEY_GITHUB = "github"
KEY_CHPAPI = "chpapi"
KEY_DEADBOLT = "deadbolt"
KEY_SALT_MASTER = "salt_master_details"
KEY_NETWORKER_SERVER = "networker_server_details"
KEY_NETWORKER_CLIENT = "networker_client_details"

# Grain data to upload into minion
GRAIN_DATA = {}

VM_TEMPLATE={}

#Class details for Abstraction class
ABSTRACT_CLASS_DETAILS = {
    "XSTREAM_CLASS_NAME" : "XstreamManager",
    "XSTREAM_CLASS_PATH" : "iaas.xstream",
    "CHPAPI_CLASS_NAME" : "CHPAPIManager",
    "CHPAPI_CLASS_PATH" : "iaas.chpapi"
}

# Protection Groups Mapped to retention Time periods
PROTECTION_GROUPS = {
    "Day":
    {
        15: "Bronze-Filesystem15",
        30: "Bronze_Filesystem30"
    },
    "Decade":
    {

    },
    "Month":
    {

    },
    "Quarter":
    {

    },
    "Week":
    {

    },
    "Year":
    {

    }
}

# Backup Service Error Messages
BACKUP_SERVICE_ERRORS = {
    500: "Unexpected error occurred, please contact administrator.",
    401: "You are unauthorized to make this request.",
    404: "Resource doesn't exist",
    "PG_NOT_FOUND": "Invalid retention period."
                    " Currently the supported values are '15 Day' and '30 Day'",
    "CHECK_HOSTNAME": "Please check the hostname you have entered. "
                      "In case the hostname is correct, please contact your administrator",
    "SYNC_FAILURE": "Unable to sync files on the VM.",
    "CLIENT_NOT_CONFIGURED": "Backup is not enabled for this VM",
    "INVALID_TYPE": "Invalid retention period type. Currently the supported value is 'Day'"
}
