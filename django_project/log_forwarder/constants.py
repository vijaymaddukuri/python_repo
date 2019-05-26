# Log Monitoring Service Error Messages
KEY_SPLUNK_CLIENT = "splunk_client_details"
KEY_SPLUNK_SERVER = "splunk_server_details"
LOG_FORWARDER_ID = "|*LOG_FORWARDER_APP*|"

INSTALL_SPLUNK_RESPONSE_STEPS = {"windows": {0: "LOG_FWRDR002_PKG_COPY_FAILED_ERROR",
                                             1: "LOG_FWRDR003_INSTALL_FAILED"
                                             },
                                 "linux": {0: "LOG_FWRDR003_INSTALL_FAILED",
                                             1: "LOG_FWRDR004_CHANGE_OWNER_FAILED",
                                             2: "LOG_FWRDR005_FIRST_START_FAILED",
                                             3: "LOG_FWRDR006_DEPLOYMENT_SERVER_CONNECTION_FAILED",
                                             4: "LOG_FWRDR004_CHANGE_OWNER_FAILED",
                                             5: "LOG_FWRDR007_SERVICE_START_ERROR"
                                             }
                                 }

LOG_FORWARDER_ERROR = {
    "LOG_FWRDR000_SALT_SERVER_ERROR": "",
    "LOG_FWRDR001_INVALID_HOSTNAME": "Please check the hostname you have entered. "
                                   "In case the hostname is correct, please contact your administrator",
    "LOG_FWRDR002_PKG_COPY_FAILED_ERROR": "Process to copy Splunk Forwarder "
                                        "package on the VM failed.",
    "LOG_FWRDR003_INSTALL_FAILED":  "Process to install Splunk Forwarder "
                                  "package on the VM failed.",
    "LOG_FWRDR004_CHANGE_OWNER_FAILED": "Process to set splunk as owner to Splunk Forwarder "
                                      "service on the VM failed.",
    "LOG_FWRDR005_FIRST_START_FAILED": "First time start after Splunk Forwarder installed "
                                     "on VM failed",
    "LOG_FWRDR006_DEPLOYMENT_SERVER_CONNECTION_FAILED": "Registration process to connect Deployment "
                                    "server from forwarder VM has failed.",
    "LOG_FWRDR007_SERVICE_START_ERROR": "Process to start the Splunk Forwarder "
                                      "service on the VM failed.",
    "LOG_FWRDR008_UNKNOWN_SALT_API_RESPONSE": "Response received after executing "
                                            "the salt net api, the command is not proper.",
    "LOG_FWRDR009_UNABLE_INSTALL": "Unable to install splunk forwarder on VM",
    "LOG_FWRDR010_SALT_CONFIGURATION_ISSUE": "unable to apply states on VM. "
                                           "check salt-master configurations.",
    "LOG_FWRDR011_UNABLE_TO_FETCH_KERNEL_TYPE": "Unable to fetch the os kernel"
                                              ", response return object is empty.",
    "LOG_FWRDR012_CHECK_VM_STATUS": "Please check the VM IP you have entered. "
                                  "In case the VM IP is correct, please contact your administrator",
    "LOG_FWRDR500_INTERNAL_SERVER_ERROR": "Unexpected error occurred."
                                    "Please contact administrator."
}
