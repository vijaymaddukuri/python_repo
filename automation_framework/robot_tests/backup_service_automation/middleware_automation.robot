*** Settings ***
Library    workflow.baseworkflow_backup_service.BaseWorkflowVulnerabilityService

*** Variables ***
${MW_SERVICE_HOST}    10.100.249.88:8000
${MW_SERVER}      10.100.249.88
${MW_SERVER_USER}    root
${MW_SERVER_PASSWORD}     Password1
${WORKER_LOGS_PATH}      /var/log/middleware/backup_worker.log
${TENANT_ID_1}    9f92203e-313c-4b35-88ff-ff00a9d77153
${TENANT_ID_2}    9f92203e-313c-4b35-88ff-ff00a9d77153 
${VM_ID_1}    8E87A82F-D40C-4200-A62E-A8E12291B0BD 
${VM_ID_2}    8E87A82F-D40C-4200-A62E-A8E12291B0BD 
${VM_1}    SLES12.xstest.local 
${VM_2}    SLES12.xstest.local 
${CALLBACK_URL}   http://10.100.249.7:3000 
${STATUSCODE}    0
${STATUS}       False
${VALIDATION_MESSAGE_1}        {"BackupStatus": "Successfully processed the backup request."}
${VALIDATION_MESSAGE_2}        {"BackupStatus": "Exception occurred while processing backup request."}

#TO DO : The "execute validate enable backup from worker logs" needs to be tested once the setup is available

*** Test Cases ***
Test VOCS T22 Enable Backup for VM's on multiple tenants
	${STATUSCODE} =  execute middleware enable backup    ${MW_SERVICE_HOST}     ${TENANT_ID_1}    ${VM_ID_1}    ${VM_1}     15    ${CALLBACK_URL}
	Should Be Equal as integers    ${STATUSCODE}    200
	${STATUSCODE} =  execute middleware enable backup    ${MW_SERVICE_HOST}     ${TENANT_ID_2}    ${VM_ID_2}    ${VM_2}     15    ${CALLBACK_URL}
	Should Be Equal as integers    ${STATUSCODE}    200
    ${STATUS} =   execute validate enable backup from worker logs    ${MW_SERVER}    ${MW_SERVER_USER}   ${MW_SERVER_PASSWORD}   ${WORKER_LOGS_PATH}   ${VALIDATION_MESSAGE_1}
	should be equal as strings  ${STATUS}   True
	sleep  10

Test VOCS T25 Success Response for Enable Backup
	${STATUSCODE} =  execute middleware enable backup    ${MW_SERVICE_HOST}     ${TENANT_ID_1}    ${VM_ID_1}    ${VM_1}     15     ${CALLBACK_URL}
	Should Be Equal as integers    ${STATUSCODE}    200
	${STATUS} =   execute validate enable backup from worker logs    ${MW_SERVER}    ${MW_SERVER_USER}   ${MW_SERVER_PASSWORD}   ${WORKER_LOGS_PATH}   ${VALIDATION_MESSAGE_1}
	should be equal as strings  ${STATUS}   True
	sleep   10

Test VOCS T27 Enable Backup for Invalid Tenant ID
	${STATUSCODE} =  execute middleware enable backup    ${MW_SERVICE_HOST}     invalidtenantid    ${VM_ID_1}    ${VM_1}    15     ${CALLBACK_URL}
	Should Be Equal as integers    ${STATUSCODE}    400
	${STATUS} =   execute validate enable backup from worker logs    ${MW_SERVER}    ${MW_SERVER_USER}   ${MW_SERVER_PASSWORD}   ${WORKER_LOGS_PATH}   ${VALIDATION_MESSAGE_2}
	should be equal as strings  ${STATUS}   True
	sleep   5

Test VOCS T29 Enable Backup for Invalid Retention Days
	${STATUSCODE} =  execute middleware enable backup    ${MW_SERVICE_HOST}     ${TENANT_ID_1}     ${VM_ID_1}    ${VM_1}     1000000     ${CALLBACK_URL}
	Should Be Equal as integers    ${STATUSCODE}    200
	${STATUS} =   execute validate enable backup from worker logs    ${MW_SERVER}    ${MW_SERVER_USER}   ${MW_SERVER_PASSWORD}   ${WORKER_LOGS_PATH}   ${VALIDATION_MESSAGE_2}
	should be equal as strings  ${STATUS}   True
	sleep  5



