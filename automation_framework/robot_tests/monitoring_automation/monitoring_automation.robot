*** Settings ***
Library     workflow.baseworkflow_monitoring.BaseWorkflowFoMonitoring
Library     workflow.baseworkflow_run_salt_state_n_verify.BaseWorkflowRunSaltStateNVerify

Library     auc.generic.salt_call.ExecuteSaltCall
Library     auc.generic.api_call.ExecuteAPICall
Library     auc.generic.log_check.ExecuteLogCheck
Library     auc.generic.parsers.Parsers

# Prerequisites :
#   1. The minion VM has salt-minion installed and is up and running.
#   2. The Nimsoft Server is up and running.
#   3. TAS is up and running
#   4. Middleware is up and able to reach TAS.
#   5. Salt Master identifies the Minion and has the Nimsoft Installer file in the correct path

*** Variables ***
${MW_MON_ENABLE_URL}      http://10.100.249.88:8000/api/v1/service/monitoring/enable
${TAS_MON_ENABLE_URL}     http://10.100.249.44:8000/api/v1/monitoring/enable

# VM Details
@{VM_SLES12}       10.100.249.56        nightlyslesvm
@{VM_WIN12R2}      10.100.249.111       windowstemplate
@{VM_RHEL7}        10.100.249.109       NightlyTestVMRHEL74.vslabs.vec.drhm01.fabshop.io
@{VM_RHEL72}       10.100.249.106       NightlyTestVMRHEL72.xtest.local
@{VM_RHEL73}       10.100.249.106       NightlyTestVMRHEL73.xtest.local
@{VM_RHEL69}       10.100.249.96        NightlyTestVMRHEL69.vslabs.vec.drhm01.fabshop.io
@{VM_RHEL71}       10.100.249.6         NightlyTestVMRhel71.vslabs.vec.drhm01.fabshop.io
@{VM_WIN16}        10.100.249.14        test2016wndows

${MONITORING_ERROR_REGEX}       error_message

*** Test Cases ***

Test VOCS-T83 Validate Enable Monitoring from Middleware on RHEL7.4 VM

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL7}      args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL7}      args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Get Start Time
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_MON_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "NightlyTestVMRHEL74", "VirtualMachineIPAddress": "10.100.249.109", "VirtualMachineRID": "vmrid", "Callback": "https://callback.com", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      200
    Sleep    100 seconds
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL7}     args=nimsoft/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS


Test VOCS-T95 Validate Enable Monitoring from Middleware on SLES

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_SLES12}      args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply      ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_SLES12}      args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Get Start Time
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_MON_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "nightlyslesvm", "VirtualMachineIPAddress": "10.100.249.56", "VirtualMachineRID": "vmrid", "Callback": "https://callback.com", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      200
    Sleep    100 seconds
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_SLES12}     args=nimsoft/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T172 Validate Enable Monitoring from Middleware on Windows12R2

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN12R2}     args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN12R2}     args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Get Start Time
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_MON_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "windowstemplate", "VirtualMachineIPAddress": "10.100.249.111", "VirtualMachineRID": "vmrid", "Callback": "https://callback.com", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      200
    Sleep    100 seconds
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN12R2}    args=nimsoft/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS


Test VOCS-T95 Validate Monitoring on all supported OS platforms from Middleware on RHEL7.2

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL72}    args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL72}    args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Get Start Time
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_MON_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "NightlyTestVMRHEL72", "VirtualMachineIPAddress": "10.100.249.106", "VirtualMachineRID": "vmrid", "Callback": "https://callback.com", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      200
    Sleep    100 seconds
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL72}   args=nimsoft/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T95 Validate Monitoring on all supported OS platforms from Middleware on RHEL7.3

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL73}    args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL73}    args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Get Start Time
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_MON_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "NightlyTestVMRHEL73", "VirtualMachineIPAddress": "10.100.249.107", "VirtualMachineRID": "vmrid", "Callback": "https://callback.com", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      200
    Sleep    100 seconds
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL73}   args=nimsoft/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T95 Validate Monitoring on all supported OS platforms from Middleware on RHEL69
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL69}    args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL69}    args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Get Start Time
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_MON_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "vmrid", "Callback": "https://callback.com", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      200
    Sleep    100 seconds
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL69}   args=nimsoft/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T95 Validate Monitoring on all supported OS platforms from Middleware on RHEL71
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL71}    args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL71}    args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Get Start Time
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_MON_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "NightlyTestVMRhel71", "VirtualMachineIPAddress": "10.100.249.6", "VirtualMachineRID": "vmrid", "Callback": "https://callback.com", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      200
    Sleep    100 seconds
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RHEL71}   args=nimsoft/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T95 Validate Monitoring on all supported OS platforms from Middleware on Win2016
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN16}    args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN16}    args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    # Get Start Time
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_MON_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "test2016wndows", "VirtualMachineIPAddress": "10.100.249.14", "VirtualMachineRID": "vmrid", "Callback": "https://callback.com", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      200
    Sleep    100 seconds
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN16}   args=nimsoft/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS


    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN16}    args=nimsoft/uninstall
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_WIN16}    args=nimsoft/cleanup
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS


Test VOCS-T102 Validate failure when Incorrect VM details are provided
    ${APIRESPONSE} =   api call    url=${TAS_MON_ENABLE_URL}    rtype=POST     body={"VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "rhel7312", "VirtualMachineIPAddress": "10.120.249.200", "VirtualMachineRID": "vmrid", "TaskID": "1234"}
    ${STATUSCODE} =   response should contain text      ${APIRESPONSE}    ${MONITORING_ERROR_REGEX}
    Should be equal as strings   ${STATUSCODE}   True

Test VOCS-T154 Validate Failure when Invalid IP is provided
    ${APIRESPONSE} =   api call    url=${TAS_MON_ENABLE_URL}    rtype=POST     body={"VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "rhel7312", "VirtualMachineIPAddress": "10.100.256.68", "VirtualMachineRID": "vmrid", "TaskID": "1234"}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      400

Test VOCS-T97 Validate Monitoring on a powered Off VM
    ${APIRESPONSE} =   api call    url=${TAS_MON_ENABLE_URL}    rtype=POST     body={"VirtualMachineID": "c921215f-ac8b-40f3-a9a6-7878ae1f036a", "VirtualMachineHostName": "rhel7312", "VirtualMachineIPAddress": "10.100.249.200", "VirtualMachineRID": "vmrid", "TaskID": "1234"}
    ${STATUSCODE} =   response should contain text      ${APIRESPONSE}    ${MONITORING_ERROR_REGEX}
    Should be equal as strings   ${STATUSCODE}   True
