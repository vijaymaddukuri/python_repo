*** Settings ***

Library     workflow.baseworkflow_backup_service.BaseWorkflowBackupService

*** Variables ***
${STATUS}    0 
${STATUSCODE}   0
${VM_RHEL}    RHEL7.xstest.local
${VM_SLES}    SLES12.xstest.local
${VM_INVALID}   INVALID.xstest.local
${BRONZE_FILESYSTEM_15}    Bronze_Filesystem15
${BRONZE_FILESYSTEM_30}    Bronze_Filesystem30
${BACKUP_SERVICE_HOST}       10.100.249.44:8000
${NETWORKER_SERVER}     10.100.249.48:9090
${NW_USER}      administrator
${NW_PWD}       Password!1

*** Test Cases ***
Test VOCS T1 Enable Backup on RHEL OS 15 days retention
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    15    Day
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0

Test VOCS T5 and T6 Changing Retention Period from 15 to 30 days RHEL OS
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate disable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    30    Day
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0

Test VOCS T7 Disable Backup On RHELOS 30days Retention
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate disable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0

Test VOCS T8 Enable Backup On SUSE OS 30days Retention
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_SLES}    30    Day
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_SLES}  ${BRONZE_FILESYSTEM_30}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0

Test VOCS T13 Changing Retention Period from 30 to 15 days SLES OS
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_SLES}
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate disable of backup     ${NETWORKER_SERVER}   ${VM_SLES}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_SLES}    15    Day
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_SLES}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0

Test VOCS 14 Disable Backup On SLES OS 15 days Retention
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_SLES}
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate disable of backup     ${NETWORKER_SERVER}   ${VM_SLES}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0

Test VOCS T15 Repeated Enable Backup with same Retention Period
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    15    Day
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    15    Day
    Should Be Equal as integers    ${STATUSCODE}   400
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate disable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0

Test VOCS T16 Repeated Enable Backup with different Retention Period
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    15    Day
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    30    Day
    Should Be Equal as integers    ${STATUSCODE}   400
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate disable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   0

Test VOCS T17 Repeated Disable Backup
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    15    Day
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}
    Should Be Equal as integers    ${STATUSCODE}   404

Test VOCS T23 Enable Backup for Invalid Hostname
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_INVALID}    15    Day
    Should Be Equal as integers    ${STATUSCODE}   500

Test VOCS T24 Disable Backup for Invalid Hostname
    ${STATUSCODE} =   execute disable backup api    ${BACKUP_SERVICE_HOST}      ${VM_INVALID}
    Should Be Equal as integers    ${STATUSCODE}   404

Test VOCS T43 Enable Backup for Invalid Retention Period
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    -1    Day
    Should Be Equal as integers    ${STATUSCODE}   500
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    0    Day
    Should Be Equal as integers    ${STATUSCODE}   500
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    14    Day
    Should Be Equal as integers    ${STATUSCODE}   500
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    16    Day
    Should Be Equal as integers    ${STATUSCODE}   500
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    29    Day
    Should Be Equal as integers    ${STATUSCODE}   500
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    31    Day
    Should Be Equal as integers    ${STATUSCODE}   500
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    30000    Day
    Should Be Equal as integers    ${STATUSCODE}   500
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1

Test VOCS T44 Disable Backup for Invalid Retention Period Type
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    30    Y
    Should Be Equal as integers    ${STATUSCODE}   400
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    30    d
    Should Be Equal as integers    ${STATUSCODE}   400
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
    ${STATUSCODE} =   execute enable backup api    ${BACKUP_SERVICE_HOST}      ${VM_RHEL}    30    Days
    Should Be Equal as integers    ${STATUSCODE}   400
    ${STATUS} =     validate enable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}   ${NW_USER}      ${NW_PWD}
    Should Be Equal as integers    ${STATUS}   1
