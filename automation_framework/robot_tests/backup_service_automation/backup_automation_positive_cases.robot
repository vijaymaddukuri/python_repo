*** Settings ***

Library     auc.generic.salt_call.ExecuteSaltCall
Library     auc.generic.api_call.ExecuteAPICall
Library     auc.generic.log_check.ExecuteLogCheck
Library     auc.generic.parsers.Parsers

*** Variables ***
# REGEX Details
${BKP_LOG REGEX}     Inside: process_backup_message((.|\n)*?) Exit: process_backup_message
${BACKUP_SUCCESS_REGEX}     Successfully created headers for xStream API call
# NAT Details
@{NAT}       10.100.249.48      NVE-1.7.xstest.local

# VM Details
@{VM_SLES12}    10.100.249.81     sles12.xstest.local
@{VM_WIN12R2}     10.100.249.11      iaas4.xstest.local

# API URL Details
${MW_BKP_ENABLE_URL}      http://10.100.249.88:8000/api/v1/service/backup/enable
${TAS_BKP_DISABLE_URL}     http://10.100.249.44:8000/api/v1/backup/disable
${NW_ENABLE_URL}     https://10.100.249.48:9090/nwrestapi/v2/global/clients?fl=hostname,protectionGroups

# IP Details for Checking Hostfile entries
@{NW_HOSTFILE}         10.100.249.48     NVE-1.7.xstest.local
@{DD_HOSTFILE}         1.1.1.4      dd.hostname.xstest.local

*** Test Cases ***

#################################################################################################
 VOCS T39 Backup on Windows 12 R2
#################################################################################################

    # Get Start Time
    ${TEST_START_TIME} =    current time utc

    # ############  Pre-enable check: Minion doesn't have hostfile entries ##################
    ${SALTRESPONSE} =   salt call   func=hosts.has_pair   tgt=@{VM_WIN12R2}  args=@{NW_HOSTFILE}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

    ${SALTRESPONSE} =   salt call   func=hosts.has_pair   tgt=@{VM_WIN12R2}  args=@{DD_HOSTFILE}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

    # ############# Pre-enable check: DNS doesn't have hostfile entries ######################
    ${SALTRESPONSE} =   salt call   func=hosts.has_pair   tgt=@{NAT}  args=@{VM_WIN12R2}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

#    Current Cleanup code cannot uninstall networker
#    # Pre-enable check: Networker is not Installed (Pkg_ver is Optional)
#    ${SALTRESPONSE} =   salt call   func=pkg.list_pkgs    tgt=@{VM_WIN12R2}
#    ${STATUSCODE} =   parse pkg list pkgs   ${SALTRESPONSE}    pkg_name=NetWorker Client     pkg_ver=9.2.1.4.Build.233
#    Should be equal as strings   ${STATUSCODE}   FAIL

    # Enable Backup from Middleware
    ${APIRESPONSE} =   api call    url=${MW_BKP_ENABLE_URL}   auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "iaas4", "RetentionDays": 15, "VirtualMachineIP":"10.100.249.11", "VirtualMachineRID": "vmrid", "TaskID": "task001", "Callback": "string"}
    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Add Wait Time for the request to go through
    asleep   240

    # Post-enable check: Check Networker if backup got enabled
    ${APIRESPONSE} =   api call     url=${NW_ENABLE_URL}     auth=basic     usr=administrator     pwd=Password2!       rtype=GET
    ${STATUSCODE} =   parse networker enable    response=${APIRESPONSE}    vm=@{VM_WIN12R2}    pg_name=Bronze_Filesystem15
    Should be equal as strings   ${STATUSCODE}   PASS

    # ############# Post-enable check: Check for Networker and DD entries in Minion #############
    ${SALTRESPONSE} =   salt call    func=hosts.has_pair    tgt=@{VM_WIN12R2}   args=@{NW_HOSTFILE}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =   salt call    func=hosts.has_pair    tgt=@{VM_WIN12R2}   args=@{DD_HOSTFILE}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # ############## Post-enable check: Check for Minion Entries in DNS Server ##################
    ${SALTRESPONSE} =   salt call    func=hosts.has_pair    tgt=@{NAT}   args=@{VM_WIN12R2}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Post-enable check: Check Worker logs for Passed Callback
    ${LOG} =   get log    service=worker    start_time=${TEST_START_TIME}    exit_pattern=${BKP_LOG REGEX}
    ${STATUSCODE} =   parse log   ${LOG}    regex=${BACKUP_SUCCESS_REGEX}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Remove Host file entry from @{NAT}
    ${SALTRESPONSE} =   salt call    func=hosts.rm_host    tgt=@{NAT}   args=@{VM_WIN12R2}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # ############# Cleanup: Disable Backup ####################################################
    ${APIRESPONSE} =   api call    url=${TAS_BKP_DISABLE_URL}     rtype=POST      body={"hostName": "iaas4.xstest.local"}
    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Cleanup: Remove configurations from Salt
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN12R2}      args=networker/automation_cleanup        pillar=function:fetch_nw_dd_details      function_args=None
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

##########################################################################################################
VOCS T39 Backup on SUSE 12
##########################################################################################################

    # Get Start Time
    ${TEST_START_TIME} =    current time utc

    # ############  Pre-enable check: Minion doesn't have hostfile entries ##################
    ${SALTRESPONSE} =   salt call   func=hosts.has_pair   tgt=@{VM_SLES12}  args=@{NW_HOSTFILE}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

    ${SALTRESPONSE} =   salt call   func=hosts.has_pair   tgt=@{VM_SLES12}  args=@{DD_HOSTFILE}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

    # ############# Pre-enable check: DNS doesn't have hostfile entries ######################
    ${SALTRESPONSE} =   salt call   func=hosts.has_pair   tgt=@{NAT}  args=@{VM_SLES12}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

    # Pre-enable check: Networker is not Installed (Pkg_ver is Optional)
    ${SALTRESPONSE} =   salt call   func=pkg.list_pkgs    tgt=@{VM_SLES12}
    ${STATUSCODE} =   parse pkg list pkgs   ${SALTRESPONSE}     pkg_name=lgtoclnt     pkg_ver=9.1.1.8-1
    Should be equal as strings   ${STATUSCODE}   FAIL

    # Enable Backup from Middleware
    ${APIRESPONSE} =   api call    url=${MW_BKP_ENABLE_URL}   auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "sles12", "RetentionDays": 15, "VirtualMachineIP":"10.100.249.11", "VirtualMachineRID": "vmrid", "TaskID": "task001", "Callback": "string"}
    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Add Wait Time for the request to go through
    asleep   240

    # Post-enable check: Check Networker if backup got enabled
    ${APIRESPONSE} =   api call     url=${NW_ENABLE_URL}     auth=basic     usr=administrator     pwd=Password2!       rtype=GET
    ${STATUSCODE} =   parse networker enable    response=${APIRESPONSE}    vm=@{VM_SLES12}    pg_name=Bronze_Filesystem15
    Should be equal as strings   ${STATUSCODE}   PASS

    # ############# Post-enable check: Check for Networker and DD entries in Minion #############
    ${SALTRESPONSE} =   salt call    func=hosts.has_pair    tgt=@{VM_SLES12}   args=@{NW_HOSTFILE}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =   salt call    func=hosts.has_pair    tgt=@{VM_SLES12}   args=@{DD_HOSTFILE}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # ############## Post-enable check: Check for Minion Entries in DNS Server ##################
    ${SALTRESPONSE} =   salt call    func=hosts.has_pair    tgt=@{NAT}   args=@{VM_SLES12}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Post-enable check: Check Worker logs for Passed Callback
    ${LOG} =   get log    service=worker    start_time=${TEST_START_TIME}    exit_pattern=${BKP_LOG REGEX}
    ${STATUSCODE} =   parse log   ${LOG}    regex=${BACKUP_SUCCESS_REGEX}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Remove Host file entry from @{NAT}
    ${SALTRESPONSE} =   salt call    func=hosts.rm_host    tgt=@{NAT}   args=@{VM_SLES12}
    ${STATUSCODE} =     parse hosts has pair   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # ############# Cleanup: Disable Backup ####################################################
    ${APIRESPONSE} =   api call    url=${TAS_BKP_DISABLE_URL}    rtype=POST    body={"hostName": "sles12.xstest.local"}
    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Cleanup: Remove configurations from Salt
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_SLES12}      args=networker/automation_cleanup        pillar=function:fetch_nw_dd_details      function_args=None
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS
