*** Settings ***
Library     ../workflow/baseworkflow
Library  ../workflow/backupautomationbaseworkflow.py
Library     ../workflow/baseworkflow
Library  ../workflow/backupautomationbaseworkflow.py
Library     ../workflow/baseworkflow
Library  ../workflow/backupautomationbaseworkflow.py

*** Variables ***
${TENANT_ID_1}    TENANT_ID_1
${TENANT_ID_2}    TENANT_ID_2
${VM_ID_1}    VM_ID_1
${VM_ID_2}    VM_ID_2
${VM_1}    HOSTNAME_VM_1
${VM_2}    HOSTNAME_VM_2
${CALLBACK_URL}    CALLBACK_URL
${STATUSCODE}    0

*** Test Cases ***
Test VOCS T22 Enable Backup for VM's on multiple tenants
${STATUSCODE} =  middleware_enable_backup    ${TENANT_ID_1} ${VM_ID_1} ${VM_1} 15 ${CALLBACK_URL}
Run Keyword If ${STATUSCODE} == 200
${STATUSCODE} =  middleware_enable_backup    ${TENANT_ID_2} ${VM_ID_2} ${VM_2} 15 ${CALLBACK_URL}
Run Keyword If ${STATUSCODE} == 200
Sleep 10

Test VOCS T25 Success Response for Enable Backup
${STATUSCODE} =  middleware_enable_backup    ${TENANT_ID_1} ${VM_ID_1} ${VM_1} 15 ${CALLBACK_URL}
Run Keyword If ${STATUSCODE} == 200
Sleep 10

Test VOCS T27 Enable Backup for Invalid Tenant ID
${STATUSCODE} =  middleware_enable_backup    invalidtenantid  ${VM_ID_1} ${VM_1} 15 ${CALLBACK_URL}
Run Keyword If ${STATUSCODE} == 404
Sleep 5

Test VOCS T29 Enable Backup for Invalid Retention Days
${STATUSCODE} =  middleware_enable_backup    ${TENANT_ID_1}  ${VM_ID_1} ${VM_1} 1000000 ${CALLBACK_URL}
Run Keyword If ${STATUSCODE} == 404
Sleep 5



