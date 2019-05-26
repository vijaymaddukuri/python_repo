# Salt ping retries count to check job is running.
SALT_JOB_RUNNING_RETRIES = 3
# Salt ping retries timeout on saltmaster in seconds.
SALT_JOB_RETRIES_TIMEOUT = 60
# Monitoring Service Error Messages
KEY_NIMSOFT_CLIENT = "nimsoft_client_details"
KEY_NIMSOFT_SERVER = "nimsoft_server_details"
INSTALL_NIMSOFT_RESPONSE_STEPS_WINDOWS = {
    0: "MON003_PKG_COPY_FAILED_ERROR",
    1: "MON005_HUB_CONNECTION_FAILED",
    2: "MON004_INSTALLATION_PROCESS_FAILED",
    3: "MON011_PROBE_CONFIG_ERROR",
    4: "MON007_SERVICE_START_ERROR"
}
INSTALL_NIMSOFT_RESPONSE_STEPS_LINUX = {
    0: "MON003_PKG_COPY_FAILED_ERROR",
    1: "MON002_EXTRACT_TAR_FAILED",
    2: "MON005_HUB_CONNECTION_FAILED",
    3: "MON006_SET_PERMISSION_FAILED",
    4: "MON004_INSTALLATION_PROCESS_FAILED",
    5: "MON011_PROBE_CONFIG_ERROR",
    6: "MON007_SERVICE_START_ERROR"

}

UNINSTALL_NIMSOFT_RESPONSE_STEPS_LINUX = {
    0: "MON0016_SERVICE_STOP_ERROR",
    1: "MON0015_UNINSTALLATION_PROCESS_FAILED"
}

CLEANUP_NIMSOFT_RESPONSE_STEPS_LINUX = {
    0: "MON0017_REMOVE_DIRECTORY_ERROR"
}

UNINSTALL_NIMSOFT_RESPONSE_STEPS_WINDOWS = {
    0: "MON0016_SERVICE_STOP_ERROR",
    1: "MON0015_UNINSTALLATION_PROCESS_FAILED",
    2: "MON0018_REMOVE_PACKAGES_ERROR"
}

MONITORING_ERRORS = {
    "MON000_SALT_SERVER_ERROR": "",
    "MON001_INVALID_HOSTNAME": "Please check the hostname you have entered. "
                               "In case the hostname is correct, please contact your administrator",
    "MON002_EXTRACT_TAR_FAILED": "Process of extracting binaries"
                                 "for Monitoring robot has failed.",
    "MON003_PKG_COPY_FAILED_ERROR": "Process to copy Monitoring robot "
                                    "package on the VM failed.",
    "MON004_INSTALLATION_PROCESS_FAILED": "Process to install Monitoring robot "
                                          "package on the VM failed.",
    "MON005_HUB_CONNECTION_FAILED": "Verfication process to connect HUB "
                                    "from robot VM over tcp has failed.",
    "MON006_SET_PERMISSION_FAILED": "Process to set execution permission"
                                    "for nimldr on the VM failed.",
    "MON007_SERVICE_START_ERROR": "Process to start the Monitoring "
                                  "service on the VM failed.",
    "MON008_UNKNOWN_SALT_API_RESPONSE": "Response received after executing "
                                    "the salt net api, the command is not proper.",
    "MON009_UNABLE_INSTALL": "Unable to install monitoring robot on VM",
    "MON010_SALT_CONFIGURATION_ISSUE": "unable to apply states on VM. "
                                       "check salt-master configurations.",
    "MON011_PROBE_CONFIG_ERROR": "Unable to copy Probe configurations",
    "MON012_UNABLE_TO_FETCH_KERNEL_TYPE": "Unable to fetch the os kernel, response return object is empty",
    "MON013_CHECK_VM_STATUS": "Please check the VM IP you have entered. "
                              "In case the VM IP is correct, please contact your administrator",
    "MON0014_UNABLE_UNINSTALL": "Unable to uninstall monitoring robot on VM",
    "MON0015_UNINSTALLATION_PROCESS_FAILED": "Process to uninstall Monitoring robot "
                                          "package on the VM failed.",
    "MON0016_SERVICE_STOP_ERROR": "Process to stop the Monitoring "
                                  "service on the VM failed.",
    "MON0017_REMOVE_DIRECTORY_ERROR": "Process to remove the nimldr "
                                  "package on the VM failed.",
    "MON0018_REMOVE_PACKAGES_ERROR": "Process to remove the "
                                  "packages on the VM failed since the specified packages are already absent.",
    "MON500_INTERNAL_SERVER_ERROR": "Unexpected error occurred."
                                    "Please contact administrator."
}
