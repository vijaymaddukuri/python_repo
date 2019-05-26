# Prerequisite to execute this robot file
#   - RHEL and SLES 12 Minion should be up and running
#   - TAS and Middleware VMs should up and running

*** Settings ***

Library     workflow.baseworkflow_enable_security_service.BaseWorkflowSecurityService
Library     workflow.baseworkflow_decommission_security_service.BaseWorkflowDecommissionSecurityService
Library     workflow.baseworkflow_run_salt_state_n_verify.BaseWorkflowRunSaltStateNVerify

*** Variables ***
${LINUX_POLICY_ID}      19
${WIN_POLICY_ID}        6
${TENANT_ID}            266905b0-4aa8-4710-bda3-1ae7111088e6
${TASKID}               79385
${CALLBACKURL}          https://rubicondev.service-now.com/api/79385/middleware

${RHEL_VM_IP}           10.250.9.61
${RHEL_VMID}            266905b0-4aa8-4710-bda3-1ae7111088e6
${RHEL_VMRID}           rhelvmrid
${RHEL_HOSTNAME}        rhel72test
${RHEL_MINION_ID}       rhel72test.0d435dfb81d3451fa772538cb8c9ed44

${SLES_VM_IP}           10.250.9.12
${SLES_VMID}            266905b0-4aa8-4710-bda3-1ae7111088e6
${SLES_VMRID}           slesvmrid
${SLES_HOSTNAME}        a0dffr014xvm012
${SLES_MINION_ID}       a0dffr014xvm012.eup01.xstream360.cloud

${WIN12_VM_IP}           10.250.9.10
${WIN12_VMID}            266905b0-4aa8-4710-bda3-1ae7111088e6
${WIN12_VMRID}           win12vmrid
${WIN12_HOSTNAME}        Win2012R2VM
${WIN12_MINION_ID}       windows-latest.420220421C6D9F010EC2A62ABB833367

${WIN16_VM_IP}           10.250.9.60
${WIN16_VMID}            266905b0-4aa8-4710-bda3-1ae7111088e6
${WIN16_VMRID}            win16vmrid
${WIN16_HOSTNAME}        windows-2016-A
${WIN16_MINION_ID}       windows-2016.EBA820422D79E4DB18772BD91BC08907

${LOGIN_TYPE}               remote
${STATUS_STATE_FILE}        trend/status
${STATUS_VALIDATE_STRING}   "DSM installation validation"
${UNINSTALL_STATE_FILE}     trend/uninstall
${UNINSTALL_STATUS_STRING}  "Uninstall DSM agent"

*** Test Cases ***

Positive Test - VOCS T111 Initiate Enable Security API from TAS on RHEL
    # uninstall DSM agent
    ${STATUSCODE} =   generic run salt state cleanup or validate   ${RHEL_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${RHEL_HOSTNAME}	${RHEL_VM_IP}		${RHEL_VMID}	${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

    # Enable Security from TAS
    ${STATUSCODE} =   execute tas enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${RHEL_HOSTNAME}    ${RHEL_VM_IP}   ${RHEL_VMID}     ${RHEL_VMRID}   ${TASKID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Validate DSM  agent installtion on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate     ${RHEL_MINION_ID}      ${LOGIN_TYPE}   ${STATUS_STATE_FILE}    ${STATUS_VALIDATE_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${RHEL_HOSTNAME}	${RHEL_VM_IP}		${RHEL_VMID}	${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

Positive Test - VOCS T70 Initiate Enable Security API from Middleware on RHEL

    # Uninstall DSM agent on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate   ${RHEL_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${RHEL_HOSTNAME}	${RHEL_VM_IP}		${RHEL_VMID}	${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

    # Initiate Enable Security API from Middleware on RHEL
    ${STATUSCODE} =   execute mw enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}   ${RHEL_HOSTNAME}    ${RHEL_VM_IP}   ${RHEL_VMID}   ${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Validate DSM agent installtion on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate     ${RHEL_MINION_ID}      ${LOGIN_TYPE}   ${STATUS_STATE_FILE}    ${STATUS_VALIDATE_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${RHEL_HOSTNAME}	${RHEL_VM_IP}		${RHEL_VMID}	${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

Positive Test - VOCS T112 Initiate Enable Security API from TAS on SLES

    # Uninstall DSM agent on SLES Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate   ${SLES_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${SLES_HOSTNAME}	${SLES_VM_IP}		${SLES_VMID}	${SLES_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

    # Initiate Enable Security API from TAS on SLES
    ${STATUSCODE} =   execute tas enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${SLES_HOSTNAME}    ${SLES_VM_IP}    ${SLES_VMID}     ${SLES_VMRID}   ${TASKID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Validate DSM agent installtion on SLES Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate     ${SLES_MINION_ID}      ${LOGIN_TYPE}   ${STATUS_STATE_FILE}    ${STATUS_VALIDATE_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${SLES_HOSTNAME}	${SLES_VM_IP}		${SLES_VMID}	${SLES_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

Positive Test - VOCS T71 Initiate Enable Security API from Middleware on SLES

    # Uninstall DSM agent on SLES Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate   ${SLES_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${SLES_HOSTNAME}	${SLES_VM_IP}		${SLES_VMID}	${SLES_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

    # Initiate Enable Security API from Middleware on SLES
    ${STATUSCODE} =   execute mw enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}   ${SLES_HOSTNAME}    ${SLES_VM_IP}   ${SLES_VMID}    ${SLES_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Validate DSM agent installtion on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate     ${SLES_MINION_ID}      ${LOGIN_TYPE}   ${STATUS_STATE_FILE}    ${STATUS_VALIDATE_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${SLES_HOSTNAME}	${SLES_VM_IP}		${SLES_VMID}	${SLES_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

Positive Test - VOCS T160 Initiate Enable Security API from TAS on WINDOWS 2012 R2
    # uninstall DSM agent
    ${STATUSCODE} =   generic run salt state cleanup or validate   ${WIN12_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${WIN12_HOSTNAME}	${WIN12_VM_IP}		${WIN12_VMID}	${WIN12_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

    # Enable Security from TAS
    ${STATUSCODE} =   execute tas enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${WIN12_HOSTNAME}    ${WIN12_VM_IP}      ${WIN12_VMID}     ${WIN12_VMRID}   ${TASKID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Validate DSM  agent installtion on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate     ${WIN12_MINION_ID}      ${LOGIN_TYPE}   ${STATUS_STATE_FILE}    ${STATUS_VALIDATE_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${WIN12_HOSTNAME}	${WIN12_VM_IP}		${WIN12_VMID}	${WIN12_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

Positive Test - VOCS T170 Initiate Enable Security API from Middleware on WINDOWS 2012 R2

    # Uninstall DSM agent on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate   ${WIN12_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${WIN12_HOSTNAME}	${WIN12_VM_IP}		${WIN12_VMID}	${WIN12_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Initiate Enable Security API from Middleware on RHEL
    ${STATUSCODE} =   execute mw enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}   ${WIN12_HOSTNAME}    ${WIN12_VM_IP}   ${WIN12_VMID}    ${WIN12_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Validate DSM agent installtion on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate     ${WIN12_MINION_ID}      ${LOGIN_TYPE}   ${STATUS_STATE_FILE}    ${STATUS_VALIDATE_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${WIN12_HOSTNAME}	${WIN12_VM_IP}		${WIN12_VMID}	${WIN12_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

Positive Test - VOCS T161 Initiate Enable Security API from TAS on WINDOWS 2016
    # uninstall DSM agent
    ${STATUSCODE} =   generic run salt state cleanup or validate   ${WIN16_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${WIN16_HOSTNAME}	${WIN16_VM_IP}		${WIN16_VMID}	${WIN16_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

    # Enable Security from TAS
    ${STATUSCODE} =   execute tas enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${WIN16_HOSTNAME}    ${WIN16_VM_IP}    ${WIN16_VMID}     ${WIN16_VMRID}   ${TASKID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Validate DSM  agent installtion on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate     ${WIN16_MINION_ID}      ${LOGIN_TYPE}   ${STATUS_STATE_FILE}    ${STATUS_VALIDATE_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${WIN16_HOSTNAME}	${WIN16_VM_IP}		${WIN16_VMID}	${WIN16_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

Positive Test - VOCS T171 Initiate Enable Security API from Middleware on WINDOWS 2016

    # Uninstall DSM agent on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate   ${WIN16_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${WIN16_HOSTNAME}	${WIN16_VM_IP}		${WIN16_VMID}	${WIN16_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

    # Initiate Enable Security API from Middleware on RHEL
    ${STATUSCODE} =   execute mw enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}   ${WIN16_HOSTNAME}    ${WIN16_VM_IP}   ${WIN16_VMID}    ${WIN16_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS

    # Validate DSM agent installtion on Minion
    ${STATUSCODE} =   generic run salt state cleanup or validate     ${WIN16_MINION_ID}      ${LOGIN_TYPE}   ${STATUS_STATE_FILE}    ${STATUS_VALIDATE_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${WIN16_HOSTNAME}	${WIN16_VM_IP}		${WIN16_VMID}	${WIN16_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS


Postive Test - VOCS T201 Initiate Decommission Security API from Middleware on RHEL
    ${STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		rhel.dummy.local	${RHEL_VM_IP}		${RHEL_VMID}	${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS

Positive Test - VOCS T206 Initiate Decommission Security API from TAS on SLES
    ${STATUSCODE} =   test execute tas decommission security api   ${SLES_HOSTNAME}    ${SLES_VM_IP}   ${SLES_VMID}    ${SLES_VMRID}    ${TASKID}
    Should be equal as strings    ${STATUSCODE}   PASS

Negative Test - VOCS T110 Initiate Enable Security API from TAS on RHEL with wrong VM details

    # Uninstall DSM agent on RHEL Minion
    ${STATUSCODE} =  generic run salt state cleanup or validate    ${RHEL_MINION_ID}   ${LOGIN_TYPE}    ${UNINSTALL_STATE_FILE}     ${UNINSTALL_STATUS_STRING}
    ${DECOMMISSION_STATUSCODE} =   test execute mw decommission security api   ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}		${RHEL_HOSTNAME}	${RHEL_VM_IP}		${RHEL_VMID}	${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   PASS
    Should be equal as strings    ${DECOMMISSION_STATUSCODE}   PASS

    # Initiate Enable Security API from TAS on RHEL with wrong VM details
    ${STATUSCODE} =   execute tas enable security api   123      148    rhel.dummy.local    1.3.3.3     ${RHEL_VMID}     ${RHEL_VMRID}   ${TASKID}
    Should be equal as strings    ${STATUSCODE}   FAIL

Negative Test - VOCS T75 Initiate Enable Security API from Middleware on RHEL with wrong VM details
    ${STATUSCODE} =   execute mw enable security api   123      1555    ${TENANT_ID}    ${TASKID}   ${CALLBACKURL}   rhel.dummy.local    1.3.3.3   ${RHEL_VMID}     ${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   FAIL

Negative Test - VOCS T77 Initiate Enable Security API from Middleware on RHEL with wrong task ID
    ${STATUSCODE} =   execute mw enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${TENANT_ID}    1111   ${CALLBACKURL}   ${RHEL_HOSTNAME}    ${RHEL_VM_IP}   ${RHEL_VMID}    ${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   FAIL

Negative Test - VOCS T78 Initiate Enable Security API from Middleware on RHEL with wrong call back url
    ${STATUSCODE} =   execute mw enable security api   ${LINUX_POLICY_ID}      ${WIN_POLICY_ID}    ${TENANT_ID}    ${TASKID}   https://dummy/api/1111/middleware   ${RHEL_HOSTNAME}    ${RHEL_VM_IP}   ${RHEL_VMID}     ${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   FAIL

Negative Test - VOCS T202 Initiate Decommission Security API from Middleware on RHEL with wrong tenant id
    ${STATUSCODE} =   test execute mw decommission security api   b5f1628c-e8d6-4873-9db5-e18572ee9398    ${TASKID}   ${CALLBACKURL}		rhel.dummy.local	1.3.3.3		${RHEL_VMID}	${RHEL_VMRID}
    Should be equal as strings    ${STATUSCODE}   FAIL

Negative Test - VOCS T203 Initiate Decommission Security API from TAS on SLES with wrong IP
    ${STATUSCODE} =   test execute tas decommission security api   rhel.dummy.local    1.3.3.3    ${RHEL_VMID}	   ${RHEL_VMRID}    ${TASKID}
    Should be equal as strings    ${STATUSCODE}   FAIL
