*** Settings ***
Library     ../workflow/baseworkflow_backup_service

Suite Setup     Initiate Suite

*** Variables ***
${CONF DIR}  C:\\Users\\gargs8\\TAveche\\conf
${STATUS}   0
${VM_RHEL}    HOSTNAME_VM_RHEL
${VM_SUSE}    HOSTNAME_VM_SUSE
${BRONZE_FILESYSTEM_15}    Bronze-Filesystem15
${BRONZE_FILESYSTEM_30}    Bronze-Filesystem30

*** Keywords ***
Initiate Suite
    Apply Settings From Files       ${CONF DIR}\\generic.yaml       ${CONF DIR}\\rest.yaml

*** Test Cases ***
Test VOCS T1 Enable Backup On RHEL OS 15days Retention
${STATUSCODE} =   enable_backup    ${VM_RHEL}    15    D
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate enable of backup     ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}
Run Keyword If '${STATUS}' == True


Test VOCS T5 and T6 Changing Retention Period from 15 to 30 days RHEL OS
${STATUSCODE} =   disable_backup    ${VM_RHEL}
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate disable of backup     ${VM_RHEL}
Run Keyword If '${STATUS}' == True
${STATUSCODE} =   enable_backup    ${VM_RHEL}    30    D
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate enable of backup     ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}
Run Keyword If '${STATUS}' == True
 

Test VOCS T7 Disable Backup On RHELOS 30days Retention
${STATUSCODE} =   disable_backup    ${VM_RHEL}
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate disable of backup     ${VM_RHEL}
Run Keyword If '${STATUS}' == True
 

Test VOCS T8 Enable Backup On SUSE OS 30days Retention
${STATUSCODE} =   enable_backup    ${VM_RHEL}    15
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate enable of backup     ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}
Run Keyword If '${STATUS}' == True
 

Test VOCS T13 Changing Retention Period from 30 to 15 days SUSE OS
${STATUSCODE} =   disable_backup    ${VM_RHEL}
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate disable of backup     ${VM_RHEL}
Run Keyword If '${STATUS}' == True
${STATUSCODE} =   enable_backup    ${VM_RHEL}    15    D
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate enable of backup     ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}
Run Keyword If '${STATUS}' == True
${STATUSCODE} =   disable_backup    ${VM_RHEL}
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate disable of backup     ${VM_RHEL}
Run Keyword If '${STATUS}' == True


Test VOCS T15 Repeated Enable Backup with same Retention Period
${STATUSCODE} =   enable_backup    ${VM_RHEL}    15    D
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate enable of backup     ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}
Run Keyword If '${STATUS}' == True
${STATUSCODE} =   enable_backup    ${VM_RHEL}    15    D
Run Keyword If '${STATUSCODE}' == 400
${STATUS} =     validate enable of backup     ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}
Run Keyword If '${STATUS}' == False
${STATUSCODE} =   disable_backup    ${VM_RHEL}
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate disable of backup     ${VM_RHEL}
Run Keyword If '${STATUS}' == True
 

Test VOCS T16 Repeated Enable Backup with different Retention Period
${STATUSCODE} =   enable_backup    ${VM_SUSE}    15    D
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate enable of backup     ${VM_RHEL}  ${BRONZE_FILESYSTEM_15}
Run Keyword If '${STATUS}' == True
 
${STATUSCODE} =   enable_backup    ${VM_SUSE}    30    D
Run Keyword If '${STATUSCODE}' == 400
${STATUS} =     validate enable of backup     ${VM_RHEL}  ${BRONZE_FILESYSTEM_30}
Run Keyword If '${STATUS}' == False


Test VOCS T17 Repeated Disable Backup
${STATUSCODE} =   disable_backup    ${VM_SUSE}
Run Keyword If '${STATUSCODE}' == 200
${STATUS} =     validate disable of backup     ${VM_SUSE}
Run Keyword If '${STATUS}' == True
${STATUSCODE} =   disable_backup    ${VM_SUSE}
Run Keyword If '${STATUSCODE}' == 400
${STATUS} =     validate disable of backup     ${VM_SUSE}
Run Keyword If '${STATUS}' == True
 

Test VOCS T23 Enable Backup for Invalid Hostname
${STATUSCODE} =   enable_backup    INVALIDHOSTNAME    30    D
Run Keyword If '${STATUSCODE}' == 404


Test VOCS T24 Disable Backup for Invalid Hostname
${STATUSCODE} =   disable_backup    INVALIDHOSTNAME
Run Keyword If '${STATUSCODE}' == 404


Test VOCS T43 Disable Backup for Invalid Retention Period
${STATUSCODE} =   enable_backup    ${VM_SUSE}    -1    D
Run Keyword If '${STATUSCODE}' == 404
${STATUSCODE} =   enable_backup    ${VM_SUSE}    0    D
Run Keyword If '${STATUSCODE}' == 404
${STATUSCODE} =   enable_backup    ${VM_SUSE}    14    D
Run Keyword If '${STATUSCODE}' == 404
${STATUSCODE} =   enable_backup    ${VM_SUSE}    16    D
Run Keyword If '${STATUSCODE}' == 404
${STATUSCODE} =   enable_backup    ${VM_SUSE}    29    D
Run Keyword If '${STATUSCODE}' == 404
${STATUSCODE} =   enable_backup    ${VM_SUSE}    31    D
Run Keyword If '${STATUSCODE}' == 404
${STATUSCODE} =   enable_backup    ${VM_SUSE}    70000    D
Run Keyword If '${STATUSCODE}' == 404
 

Test VOCS T44 Disable Backup for Invalid Retention Period Type
${STATUSCODE} =   enable_backup    ${VM_SUSE}    15    Y
Run Keyword If '${STATUSCODE}' == 404
${STATUSCODE} =   enable_backup    ${VM_SUSE}    15    d
Run Keyword If '${STATUSCODE}' == 404
${STATUSCODE} =   enable_backup    ${VM_SUSE}    15    Days
Run Keyword If '${STATUSCODE}' == 404
