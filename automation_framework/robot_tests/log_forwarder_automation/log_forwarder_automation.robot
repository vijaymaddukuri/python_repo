*** Settings ***
Library     auc.generic.salt_call.ExecuteSaltCall
Library     auc.generic.api_call.ExecuteAPICall
Library     auc.generic.log_check.ExecuteLogCheck
Library     auc.generic.parsers.Parsers

# Prerequisites :
#   1. The minion VM has salt-minion installed and is up and running.
#   2. The Deployment Server is up and running.
#   3. TAS is up and running
#   4. Middleware is up and able to reach TAS.
#   5. Salt Master identifies the Minion and has the Splunk Forwarder Installer file in the correct path

*** Variables ***
${MW_LOG_ENABLE_URL}      http://10.100.249.88:8000/api/v1/service/logforwarder/enable
${TAS_LOG_ENABLE_URL}     http://10.100.249.44:8000/api/v1/logforwarder/enable
${MW_LOG_DISABLE_URL}     http://10.100.249.88:8000/api/v1/service/logforwarder/disable
${TAS_LOG_DISABLE_URL}    http://10.100.249.44:8000/api/v1/logforwarder/disable

# VM Details
@{VM_RhelPR}       10.100.249.96         NightlyTestVMRHEL69.vslabs.vec.drhm01.fabshop.io
@{VM_Windows}      10.100.249.14         test2016wndows
@{VM_DUMMY}        10.250.9.1            SLES12SP.virtu

*** Test Cases ***

Test VOCS-T208 Validate Enable Log forwarding for all supported os platforms(RHEL)
    ${APIRESPONSE} =   api call    url=${MW_LOG_DISABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
	sleep     1 minute

    ${APIRESPONSE} =   api call    url=${MW_LOG_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
    ${STATUS} =    parse api status    ${APIRESPONSE}
    Should be equal as strings   ${STATUS}   PASS

    sleep    8 minutes

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RhelPR}     args=splunkuf/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T208 Validate Enable Log forwarding for all supported os platforms(Windows)
    ${APIRESPONSE} =   api call    url=${MW_LOG_DISABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "FF222042DE0ABC62E8156875EBA3D54D", "VirtualMachineHostName": "test2016wndows", "VirtualMachineIPAddress": "10.100.249.14", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
	sleep       1 minute
    ${APIRESPONSE} =   api call    url=${TAS_LOG_ENABLE_URL}     rtype=POST     body={"VirtualMachineID": "FF222042DE0ABC62E8156875EBA3D54D", "VirtualMachineHostName": "test2016wndows", "VirtualMachineIPAddress": "10.100.249.14", "VirtualMachineRID": "1234", "TaskID": "79385"}
    sleep    8 minutes

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_Windows}     args=splunkuf/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T207 Validate Log Forwarder "Enable" fails when the target VM is powered OFF
    ${APIRESPONSE} =   api call    url=${TAS_LOG_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "TestVM", "VirtualMachineIPAddress": "10.250.9.1", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

Test VOCS-T209 Validate log forwarder enable on the VM for which log forwarder is already enabled
    ${APIRESPONSE} =   api call    url=${TAS_LOG_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
    ${STATUS} =    parse api status    ${APIRESPONSE}
    Should be equal as strings   ${STATUS}   FAIL


Test VOCS-T210 Validate failure message when Incorrect VM details are provided
    ${APIRESPONSE} =   api call    url=${TAS_LOG_ENABLE_URL}    rtype=POST     body={"VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "SLES12SP", "VirtualMachineIPAddress": "10.250.9.1", "VirtualMachineRID": "12345", "TaskID": "12345"}
    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

Test VOCS-T217 Validate Error message when VM is unreachable (all scenarios)
    ${APIRESPONSE} =   api call    url=${TAS_LOG_ENABLE_URL}    rtype=POST     body={"VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "SLES12SP", "VirtualMachineIPAddress": "10.250.9.1", "VirtualMachineRID": "12345", "TaskID": "12345"}
    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

Test VOCS-T212 Validate Log Forwarder "Disable" fails when the target VM is powered OFF
    ${APIRESPONSE} =   api call    url=${TAS_LOG_DISABLE_URL}    rtype=POST     body={"VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "SLES12SP", "VirtualMachineIPAddress": "10.250.9.1", "VirtualMachineRID": "12345", "TaskID": "12345"}
    sleep      1 minute
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_Windows}     args=splunkuf/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

Test VOCS-T221 Validate Log forwarding disable for all supported os platforms(RHEL)
    ${APIRESPONSE} =   api call    url=${MW_LOG_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
	sleep    8 minutes

    ${APIRESPONSE} =   api call    url=${MW_LOG_DISABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
    ${STATUS} =    parse api status    ${APIRESPONSE}
    Should be equal as strings   ${STATUS}   PASS

    sleep    1 minute

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RhelPR}     args=splunkuf/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T208 Validate Disable Log forwarding from tas for all supported os platforms (RHEL)
    ${APIRESPONSE} =   api call    url=${TAS_LOG_ENABLE_URL}     rtype=POST     body={"VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "1234", "TaskID": "79385"}

	sleep    8 minutes

    ${STATUSCODE} =   parse api status   ${APIRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL

Test VOCS-T213 Validate Disable log forwarder disable on the VM for which log forwarder is already disabled
    ${APIRESPONSE} =   api call    url=${MW_LOG_DISABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
    sleep    1 minute

    ${APIRESPONSE} =   api call    url=${MW_LOG_DISABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "f3ace9fb6989445e9ef1e21192a30173", "VirtualMachineHostName": "NightlyTestVMRHEL69", "VirtualMachineIPAddress": "10.100.249.96", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}
    sleep    1 minute

    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_RhelPR}     args=splunkuf/status
    ${STATUSCODE} =      parse salt response    ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   PASS

Test VOCS-T221 Validate Log forwarding for all supported os platforms(Windows)
    ${APIRESPONSE} =   api call    url=${MW_LOG_ENABLE_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID": "9bdcead0-e40c-11e8-9f32-f2801f1b9fd1", "VirtualMachineID": "FF222042DE0ABC62E8156875EBA3D54D", "VirtualMachineHostName": "test2016wndows", "VirtualMachineIPAddress": "10.100.249.14", "VirtualMachineRID": "1234", "Callback": "https://rubicondev.service-now.com/api/79385/middleware", "TaskID": "79385"}

	sleep     8 minutes
    ${APIRESPONSE} =   api call    url=${TAS_LOG_DISABLE_URL}     rtype=POST     body={"VirtualMachineID": "FF222042DE0ABC62E8156875EBA3D54D", "VirtualMachineHostName": "test2016wndows", "VirtualMachineIPAddress": "10.100.249.14", "VirtualMachineRID": "1234", "TaskID": "79385"}
    sleep     1 minute
    ${SALTRESPONSE} =    salt call    func=state.apply     tgt=@{VM_Windows}     args=splunkuf/status
    ${STATUSCODE} =      parse state apply   ${SALTRESPONSE}
    Should be equal as strings   ${STATUSCODE}   FAIL












