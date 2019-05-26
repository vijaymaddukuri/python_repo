*** Settings ***
#Import the updateconfig class with the service name(TAS or Middleware or worker)
Library     utils.UpdateConfig.UpdateConfig     TAS
#Library  utils.UpdateConfig.UpdateConfig    Middleware
#Library  utils.UpdateConfig.UpdateConfig    Worker

*** Variables ***
# Need to pass the key for which value need to updated, key should in the below format
# Example:  If we want to change the Yml['networker_server_details']['NETWORKER_MAX_JOBS'], we need to pass
# the parent key "networker_server_details" followed by child key "NETWORKER_MAX_JOBS"

# networker_server_details:
#    ADD_HOSTNAME_SCRIPT_PATH: networker/add_hosts
#    NETWORKER_MAX_CLIENTS: '1000'
#    NETWORKER_MAX_JOBS: '1000'
#    NETWORKER_SERVERS:
${KEYS}     networker_server_details NETWORKER_MAX_JOBS
# The value which need to be updated.
${VALUE}    105


*** Test Cases ***
Update Yaml
  # Testcase to update the config.yaml
  update yaml file    ${KEYS}     ${VALUE}
  # Clean up to revert the changes in config.yaml to the default values
  cleanup




