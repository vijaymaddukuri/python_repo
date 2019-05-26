*** Settings ***

Library     auc.generic.salt_call.ExecuteSaltCall
Library     auc.generic.api_call.ExecuteAPICall
Library     auc.generic.log_check.ExecuteLogCheck
Library     auc.generic.parsers.Parsers
Suite Setup    Run Prerequisites

*** Variables ***
# API URL Details
${MW_BKP_ENABLE_URL}            http://10.100.249.88:8000/api/v1/service/backup/enable
${TAS_PAUSE_API_URL}      http://10.100.249.44:8000/api/v1/backup/pause
${TAS_RESUME_API_URL}      http://10.100.249.44:8000/api/v1/backup/resume
${NW_GET_CLIENTS_INFO_URL}      https://10.100.249.48:9090/nwrestapi/v2/global/clients?q=hostname

# VM Details
${VM_SLES12_HOSTNAME}    sles12
${VM_WIN12R2_HOSTNAME}    iaas4

*** Keywords ***
Run Prerequisites
     #Prerequisite : Enable Backup On the SLES 12 VM
     ${APIRESPONSE} =   api call    url=${MW_BKP_ENABLE_URL}   auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "sles12", "RetentionDays": 15,"Callback": "string"}
     sleep  10
     ${STATUSCODE} =   parse api status    ${APIRESPONSE}
     Should be equal as strings   ${STATUSCODE}    PASS
     #Prerequisite : Enable Backup On the WINDOWS 2012 VM
     ${APIRESPONSE} =   api call    url=${MW_BKP_ENABLE_URL}   auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "iaas4", "RetentionDays": 15,"Callback": "string"}
     sleep  10
     ${STATUSCODE} =   parse api status    ${APIRESPONSE}
     Should be equal as strings   ${STATUSCODE}    PASS

*** Test Cases ***
VOCS-T177 Validate Backup is Paused when the TAS Backup Pause API is called

    #Run PAUSE API on SLES12
    ${APIRESPONSE} =   api call    url=${TAS_PAUSE_API_URL}     rtype=POST      body={"VirtualMachineHostName": "sles12","VirtualMachineIPAddress": "10.100.249.81", "VirtualMachineID":"c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineRID": "dummy", "TaskID": "1234"}
    sleep  10
    ${STATUSCODE} =   parse api status    ${APIRESPONSE}
    Should be equal as strings    ${STATUSCODE}    PASS
    #Vaidate Pause from Networker Client
    ${FINAL_URL} =    catenate   SEPARATOR=:     ${NW_GET_CLIENTS_INFO_URL}     ${VM_SLES12_HOSTNAME}
    LOG TO CONSOLE   ${FINAL_URL}
    ${APIRESPONSE} =   api call    url=${FINAL_URL}     auth=basic    usr=administrator    pwd=Password2!     rtype=GET
    ${STATUSCODE} =  parse_schedule_backup_status    ${APIRESPONSE}
    Should be equal as strings    ${STATUSCODE}    False
    #Run PAUSE API on WINDOWS2012 VM
    ${APIRESPONSE} =   api call    url=${TAS_PAUSE_API_URL}     rtype=POST      body={"VirtualMachineHostName": "iaas4", "VirtualMachineIPAddress": "10.100.249.11", "VirtualMachineID":"c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineRID": "dummy", "TaskID": "1234"}
    Sleep  10
    ${STATUSCODE} =   parse api status    ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}    PASS
    #Vaidate Pause from Networker Client
    ${FINAL_URL} =    catenate    SEPARATOR=:    ${NW_GET_CLIENTS_INFO_URL}     ${VM_WIN12R2_HOSTNAME}
    LOG TO CONSOLE  ${FINAL_URL}
    ${APIRESPONSE} =    api call    url=${FINAL_URL}     auth=basic    usr=administrator    pwd=Password2!     rtype=GET
    ${STATUS} =   parse_schedule_backup_status    ${APIRESPONSE}
    Should be equal as strings   ${STATUS}    False


VOCS-T178 Validate Backup is Resumed when the TAS Backup Resume API is called
    #Run Resume API on SLES12 VM
    ${APIRESPONSE} =   api call    url=${TAS_RESUME_API_URL}     rtype=POST      body={"VirtualMachineHostName": "sles12", "VirtualMachineIPAddress": "10.100.249.81", "VirtualMachineID":"c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineRID": "dummy", "TaskID": "1234"}
    sleep  10
    ${STATUSCODE} =   parse api status    ${APIRESPONSE}
    should be equal as strings     ${STATUSCODE}    PASS
    #Vaidate Pause from Networker Client
    ${FINAL_URL} =    catenate    SEPARATOR=:     ${NW_GET_CLIENTS_INFO_URL}     ${VM_SLES12_HOSTNAME}
    LOG TO CONSOLE     ${FINAL_URL}
    ${APIRESPONSE} =    api call    url=${FINAL_URL}     auth=basic    usr=administrator    pwd=Password2!     rtype=GET
    ${STATUS} =   parse_schedule_backup_status    ${APIRESPONSE}
    Should be equal as strings   ${STATUS}    True
    #Run RESUME API on WINDOWS 2012 VM
    ${APIRESPONSE} =   api call    url=${TAS_RESUME_API_URL}     rtype=POST      body={"VirtualMachineHostName": "iaas4", "VirtualMachineIPAddress": "10.100.249.11", "VirtualMachineID":"c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineRID": "dummy", "TaskID": "1234"}
    sleep  10
    ${STATUSCODE} =   parse api status    ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}    PASS
    #Vaidate Pause from Networker Client
    ${FINAL_URL} =    catenate     SEPARATOR=:    ${NW_GET_CLIENTS_INFO_URL}     ${VM_WIN12R2_HOSTNAME}
    LOG TO CONSOLE     ${FINAL_URL}
    ${APIRESPONSE} =    api call    url=${FINAL_URL}     auth=basic    usr=administrator    pwd=Password2!     rtype=GET
    ${STATUS} =   parse_schedule_backup_status    ${APIRESPONSE}
    Should be equal as strings   ${STATUS}    True

VOCS-T187 Validate Backup Resume API gives proper error when VM doesnt have backup paused
    ${APIRESPONSE} =  api call    url=${TAS_RESUME_API_URL}     rtype=POST      body={"VirtualMachineHostName": "sles12", "VirtualMachineIPAddress": "10.100.249.81", "VirtualMachineID":"c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineRID": "dummy", "TaskID": "1234"}
    sleep  10
    ${STATUSCODE} =   parse api status    ${APIRESPONSE}
    should be equal as strings     ${STATUSCODE}    FAIL

VOCS-T186 Validate Backup Pause API gives proper error when VM doesnt have backup enabled
    ${APIRESPONSE} =   api call    url=${TAS_PAUSE_API_URL}     rtype=POST      body={"VirtualMachineHostName": "invalid","VirtualMachineIPAddress": "10.100.249.124", "VirtualMachineID":"c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineRID": "dummy", "TaskID": "1234"}
    sleep  10
    ${STATUSCODE} =   parse api status    ${APIRESPONSE}
    Should be equal as strings    ${STATUSCODE}    FAIL



