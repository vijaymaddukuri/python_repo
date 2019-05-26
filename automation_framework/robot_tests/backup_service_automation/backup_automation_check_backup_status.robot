*** Settings ***

Library     auc.generic.salt_call.ExecuteSaltCall
Library     auc.generic.api_call.ExecuteAPICall
Library     auc.generic.log_check.ExecuteLogCheck
Library     auc.generic.parsers.Parsers

*** Variables ***
# VM Details
@{VM_RHEL}            10.100.249.109   NightlyTestVMRHEL74.vslabs.vec.drhm01.fabshop.io

# REGEX Details
${BKP_ENABLE_LOG_REGEX}      Inside: process_backup_message((.|\n)*?) Exit: process_backup_message
${BKP_SUCCESS_REGEX}         Successfully created headers for xStream API call

${BKP_CHECK_LOG_REGEX}       Inside: post of CheckBackupStatus((.|\n)*?) Exit: post of CheckBackupStatus
${BKP_NOT_ENABLED}           Backup was not enabled
${BKP_NOT_TAKEN_WITHIN_24H}  BACKUP031_NO_BACKUP_AVAILABLE
${BKP_TAKEN_WITHIN_24H}      Backup was taken within 24 hours

# API URL Details
${TAMS_BKP_CHECK_URL}      http://10.100.249.84:8000/api/v1/backup/checkstatus
${TAMS_BKP_ENABLE_URL}     http://10.100.249.85:8000/api/v1/backup/enable
${TAMS_BKP_DISABLE_URL}    http://10.100.249.85:8000/api/v1/backup/disable

# Networker APIs
${NW_ON_DEMAND_BACKUP}     https://10.100.249.48:9090/nwrestapi/v2/global/clients/46.0.214.15.0.0.0.0.108.137.189.92.10.100.249.48/op/backup
${NW_ON_DEMAND_BACKUP_NVE2}  https://10.100.249.104:9090/nwrestapi/v2/global/clients/46.0.214.15.0.0.0.0.108.137.189.92.10.100.249.48/op/backup
${NW_CLIENT_DELETE_NVE1}   https://10.100.249.48:9090/nwrestapi/v2/global/clients/46.0.214.15.0.0.0.0.108.137.189.92.10.100.249.48
${NW_CLIENT_DELETE_NVE2}   https://10.100.249.104:9090/nwrestapi/v2/global/clients/46.0.214.15.0.0.0.0.108.137.189.92.10.100.249.48

# API BODY
${TAMS_BKP_ENABLE_JSON_BODY}    body={"VirtualMachineID":"fbc68b7a-e056-4ab4-ab7c-fa56aec055cd","VirtualMachineHostName": "NightlyTestVMRHEL74.vslabs.vec.drhm01.fabshop.io","VirtualMachineIPAddress": "10.100.249.109","VirtualMachineRID": "vmrid","TaskID": "task0001","RetentionDays": 30}
${TAMS_BKP_DISABLE_JSON_BODY}   body={"VirtualMachineID":"fbc68b7a-e056-4ab4-ab7c-fa56aec055cd","VirtualMachineHostName": "NightlyTestVMRHEL74.vslabs.vec.drhm01.fabshop.io","VirtualMachineIPAddress": "10.100.249.109","VirtualMachineRID": "vmrid","TaskID": "task0002"}
${TAMS_BKP_CHECK_JSON_BODY}     body={"VirtualMachineID":"fbc68b7a-e056-4ab4-ab7c-fa56aec055cd","VirtualMachineHostName": "NightlyTestVMRHEL74.vslabs.vec.drhm01.fabshop.io","VirtualMachineIPAddress": "10.100.249.109","VirtualMachineRID": "vmrid","TaskID": "task0003"}
${TAMS_BKP_CHECK_INCORRECT_TASKID_JSON_BODY}     body={"VirtualMachineID":"fbc68b7a-e056-4ab4-ab7c-fa56aec055cd","VirtualMachineHostName": "NightlyTestVMRHEL74.vslabs.vec.drhm01.fabshop.io","VirtualMachineIPAddress": "10.100.249.109","VirtualMachineRID": "vmrid","TaskID": ""}
${NW_ON_DEMAND_BACKUP_JSON_BODY}   body={"policy": "Bronze","workflow": "Filesystem15"}
${NW_ON_DEMAND_BACKUP_NVE2_JSON_BODY}   body={"policy": "Bronze","workflow": "Filesystem15"}

# IP Details for Checking host file entries
@{NW_IP}         10.100.249.48     NVE-1.7.xstest.local

# NAT Details for Jumpbox. This will be used only when Test Automation is run in A0DF setup. For running test automation in local lab this entry can be ignored.
@{NAT}              xx.xx.xx.xx       xxxxxx


*** Test Cases ***
# All the backup check status test cases are performed on 1 VM.
# In 1st test case no backup is scheduled for the VM. Check backup status API returns 404
# In 2nd test case the backup is scheduled for for the VM in 1st NVE. Check backup status API returns 404
# In 3rd test case the on demand backup is enabled for for the VM in 1st NVE. Check backup status API returns 200
# In 5th test case backup is disabled for the VM from 1st NVE. It is scheduled in 2nd NVE via NVE API. Check backup status API returns 404. Take on demand backup in 2nd NVE. Check backup status API returns 200

##########################################################################################################################
 VOCS T-229 Backup Check: API to check Backup responds 404 when backup was NOT enabled for the VM
##########################################################################################################################

    # PRE-REQ: "Backup is not enabled for the VM" so cleanup entries from Networkers
    # Disable backup if it is already enabled
    ${APIRESPONSE} =   api call    url=${TAMS_BKP_DISABLE_URL}      rtype=POST     ${TAMS_BKP_DISABLE_JSON_BODY}

    # Delete client entry from NVE if present
    ${APIRESPONSE} =   api call     url=${NW_CLIENT_DELETE_NVE1}     auth=basic     usr=administrator     pwd=Password3!       rtype=DELETE
    ${APIRESPONSE} =   api call     url=${NW_CLIENT_DELETE_NVE2}     auth=basic     usr=administrator     pwd=xStream2017!     rtype=DELETE

    # TEST STEPS
    # Check backup was never enabled for VM with API response 404
    ${APIRESPONSE} =   api call    url=${TAMS_BKP_CHECK_URL}    rtype=POST      ${TAMS_BKP_CHECK_JSON_BODY}
    ${STATUSCODE} =    parse api status   ${APIRESPONSE}   404
    Should be equal as strings   ${STATUSCODE}   PASS
    asleep   30         # Added wait time for the request to go through

    # Check API response for the correct message
    ${MESSAGE_EXIST} =  response_should_contain_text   response=${APIRESPONSE}   search_text=${BKP_NOT_ENABLED}
    Should be equal as strings     ${MESSAGE_EXIST}    TRUE

############################################################################################################################
VOCS T-228 Backup Check: API to check Backup responds 404 when backup was NOT taken within 24 hours
############################################################################################################################

    # PRE-REQ: Backup should be scheduled
    # Schedule Backup from TAS
    ${APIRESPONSE} =   api call    url=${TAMS_BKP_ENABLE_URL}    rtype=POST      ${TAMS_BKP_ENABLE_JSON_BODY}
    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    asleep   30

    # TEST STEPS:
    # Check backup was scheduled but was not taken within 24 hours with API response 404
    ${APIRESPONSE} =   api call    url=${TAMS_BKP_CHECK_URL}    rtype=POST      ${TAMS_BKP_CHECK_JSON_BODY}
    ${STATUSCODE} =    parse api status   ${APIRESPONSE}   404
    Should be equal as strings   ${STATUSCODE}   PASS
    asleep   30         # Added wait time for the request to go through

    # Check API response for the correct message
    ${MESSAGE_EXIST} =  response_should_contain_text   response=${APIRESPONSE}   search_text=${BKP_NOT_TAKEN_WITHIN_24H}
    Should be equal as strings     ${MESSAGE_EXIST}    TRUE

#######################################################################################################################
VOCS T-226 Backup Check: API to check Backup responds 200 when backup was taken within 24 hours
#######################################################################################################################

    # PRE-REQ: Take on demand backup to enable backup
    # Make sure that the save set is configured such that the enable backup takes less time
    ${APIRESPONSE} =   api call     url=${NW_ON_DEMAND_BACKUP}     auth=basic     usr=administrator     pwd=Password3!       rtype=POST   ${NW_ON_DEMAND_BACKUP_JSON_BODY}
    ${STATUSCODE} =   parse api status    response=${APIRESPONSE}   code=201
    Should be equal as strings   ${STATUSCODE}   PASS
    asleep   120     # Add Wait Time for the backup to be enabled

    # TEST STEP:
    # Check backup was scheduled but was taken within 24 hours with API response 200
    ${APIRESPONSE} =   api call    url=${TAMS_BKP_CHECK_URL}    rtype=POST      ${TAMS_BKP_CHECK_JSON_BODY}
    ${STATUSCODE} =   parse api status   response=${APIRESPONSE}    code=200
    Should be equal as strings   ${STATUSCODE}   PASS
    asleep   30   # Add Wait Time for the request to go through

    # Check API response for the correct message
    ${MESSAGE_EXIST} =  response_should_contain_text   response=${APIRESPONSE}   search_text=${BKP_TAKEN_WITHIN_24H}
    Should be equal as strings     ${MESSAGE_EXIST}    TRUE

    # CLEANUP:
    # Delete client entry from NVE if present
    ${APIRESPONSE} =   api call     url=${NW_CLIENT_DELETE_NVE1}     auth=basic     usr=administrator     pwd=Password3!       rtype=DELETE

    # Remove client from VM
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL}      args=networker/automation_cleanup        pillar=function:fetch_nw_dd_details      function_args=None
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS


#######################################################################################################################
VOCS T-230 Backup Check: Negative Test: Check Backup responds error codes
#######################################################################################################################

    # PRE-REQ: Take on demand backup to enable backup

    # TEST STEP:
    # Check backup returns 400 Bad Request when input parameters are incorrect eg: taskId is blank
    ${APIRESPONSE} =   api call    url=${TAMS_BKP_CHECK_URL}    rtype=POST      ${TAMS_BKP_CHECK_INCORRECT_TASKID_JSON_BODY}
    ${STATUSCODE} =   parse api status   response=${APIRESPONSE}    code=400
    Should be equal as strings   ${STATUSCODE}   PASS
    asleep   30   # Add Wait Time for the request to go through

#######################################################################################################################
VOCS T-252 Backup Check: API to check Backup with multiple Networkers
#######################################################################################################################

    # PRE-REQ: Take on demand backup to enable backup
    # Backup is disabled for the VM from 1st NVE. It is scheduled in 2nd NVE via NVE API. Check backup status API returns 404.
    # Delete client entry from NVE if present
    ${APIRESPONSE} =   api call     url=${NW_CLIENT_DELETE_NVE1}     auth=basic     usr=administrator     pwd=Password3!       rtype=DELETE
    ${APIRESPONSE} =   api call     url=${NW_CLIENT_DELETE_NVE2}     auth=basic     usr=administrator     pwd=xStream2017!     rtype=DELETE

    # Remove client from VM
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL}      args=networker/automation_cleanup        pillar=function:fetch_nw_dd_details      function_args=None
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${APIRESPONSE} =   api call     url=${NW_ON_DEMAND_BACKUP_NVE2}     auth=basic     usr=administrator     pwd=xStream2017!       rtype=POST   ${NW_ON_DEMAND_BACKUP__NVE2_JSON_BODY}
    ${STATUSCODE} =   parse api status    response=${APIRESPONSE}   code=201
    Should be equal as strings   ${STATUSCODE}   PASS
    asleep   120     # Add Wait Time for the backup to be enabled

    # TEST STEP:
    # Take on demand backup in 2nd NVE. Check backup status API returns 200
    # Check if NVE2 is selected by check backup status API
    ${APIRESPONSE} =   api call    url=${TAMS_BKP_CHECK_URL}    rtype=POST      ${TAMS_BKP_CHECK_JSON_BODY}
    ${STATUSCODE} =   parse api status   response=${APIRESPONSE}    code=200
    Should be equal as strings   ${STATUSCODE}   PASS
    asleep   30   # Add Wait Time for the request to go through

    # CLEANUP:
    # Delete client entry from NVEs if present
    ${APIRESPONSE} =   api call     url=${NW_CLIENT_DELETE_NVE1}     auth=basic     usr=administrator     pwd=Password3!       rtype=DELETE
    ${APIRESPONSE} =   api call     url=${NW_CLIENT_DELETE_NVE2}     auth=basic     usr=administrator     pwd=xStream2017!     rtype=DELETE

    # Remove client from VM
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL}      args=networker/automation_cleanup        pillar=function:fetch_nw_dd_details      function_args=None
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS