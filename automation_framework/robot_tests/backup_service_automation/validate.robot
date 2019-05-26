*** Settings ***
Library     workflow.baseworkflow_backup_service.BaseWorkflowBackupService

*** Variables ***
${CONF DIR}  C:\\Users\\gargs8\\TAveche\\conf
${STATUS}   0
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
    Log     $(STATUS)
    Should Be Equal as integers    ${STATUS}   0

Test VOCS T7 Disable Backup On RHELOS 30days Retention
    ${STATUSCODE} =   execute disable backup api      ${BACKUP_SERVICE_HOST}      ${VM_RHEL}
    Should Be Equal as integers    ${STATUSCODE}   200
    ${STATUS} =     validate disable of backup     ${NETWORKER_SERVER}   ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}   ${NW_USER}      ${NW_PWD}
    Log     $(STATUS)
    Should Be Equal as integers    ${STATUS}   0
