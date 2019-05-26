# Salt ping retries count to check job is running.
SALT_JOB_RUNNING_RETRIES = 3
# Salt ping retries timeout on saltmaster in seconds.
SALT_JOB_RETRIES_TIMEOUT = 60

DSM_COMPUTER_URL = 'api/computers'
DSM_COMPUTER_LIST_URL = '{}/search'.format(DSM_COMPUTER_URL)
DSM_API_VERSION = 'v1'

#Security Service Error Messages
SECURITY_ERRORS = {
    "SEC001_SALT_CONNECTION_ERROR": "",
    "SEC002_TREND_MICRO_AGENT_DOWNLOAD_FAILURE": "Downloading From DSM server failed",
    "SEC003_TREND_MICRO_AGENT_INSTALL_FAILURE": "Installation of trend micro agent failed",
    "SEC004_ENABLE_SECURITY_FAILED": "Activation of security feature on VM failed",
    "SEC005_UNKNOWN_SALT_API_RESPONSE": "Response received after executing the salt net api command is not proper",
    "SEC006_SALT_CONFIGURATION_ISSUE": "unable to apply states on VM. "
                                       "check salt-master configurations.",
    "SEC007_AGENT_DEPLOY_SCRIPT_COPY_FAILED": "Copy of power shell script agentDeploymentScript "
                                                "to windows minion failed",
    "SEC008_CHECK_VM_STATUS": "Please check the VM IP you have entered. "
                              "In case the VM IP is correct, please contact your administrator",
    "SEC009_DSM_API": "DSM server API call failed while enabling security. "
                      "Please contact your administrator",
    "SEC010_SECURITY_ENABLED": "Security is already enabled, but DSM does not have entry of the VM. "
                      "Please contact your administrator.",
    "SEC500_INTERNAL_SERVER_ERROR": "Unexpected error occurred. "
                                    "Please contact administrator."
}
