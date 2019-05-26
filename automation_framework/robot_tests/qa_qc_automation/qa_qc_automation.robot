*** Settings ***
Library     auc.generic.api_call.ExecuteAPICall
Library     auc.generic.log_check.ExecuteLogCheck
Library     auc.generic.parsers.Parsers

*** Variables ***
${MW_URL}       http://10.100.249.84:8000/api/v1/service/system/validate
${TAS_URL}      http://10.100.249.85:8000/api/v1/system/validate

${QA_QC_SUCCESS_REGEX}
${QA_QC_LOG_END_REGEX}      Exit: process_system_validation_message


*** Test Cases ***
VOCS-T190 Validate QA-QC Middleware API returns error for malformed Payload
    [Documentation]      In this test case we are trying to validate malformed request error when a manatory field is
    ...                  missing in the payload. Make sure you have all valid details in request and body and any one
    ...                  mandatory field missing
    ${APIRESPONSE} =   api call    url=${MW_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID":"0c130b61-7581-429e-a51a-d77ba142ef8b","VirtualMachineIPAddress":"10.100.249.250","Callback":"callback.servicenow.com","VirtualMachineRID":"NightlyTestVMRHEL74","TaskID":"RITM209090932","Methods":[{"TestId":0,"ExpectedResult":12}]}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      400
    ${RESPONSE_JSON} =  get response json   ${APIRESPONSE}
    ${STATUS} =    response should contain text    ${RESPONSE_JSON}    This field is required
    should be equal as strings   ${STATUS}     True

VOCS-T195 Validate QA-QC Middleware API runs successfully and callback is generated in logs
    [Documentation]      In this test case we are validating that a Middleware request runs successfully and the worker
    ...                  logs have the success message. Make sure you have all valid details in request and body
    ${TEST_START_TIME} =    current time utc
    ${APIRESPONSE} =   api call    url=${MW_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID":"0c130b61-7581-429e-a51a-d77ba142ef8b","VirtualMachineIPAddress":"10.100.249.109","Callback":"callback.servicenow.com","VirtualMachineRID":"NightlyTestVMRHEL74","TaskID":"RITM209090932","Methods":[{"TestName": "check_date","TestId":0}]}
    ${LOG} =   get log    service=worker    start_time=${TEST_START_TIME}    exit_pattern=${QA_QC_LOG_END_REGEX}
    ${STATUSCODE} =   parse log   ${LOG}    regex=${QA_QC_SUCCESS_REGEX}
    Should be equal as strings   ${STATUSCODE}   PASS

VOCS-T200 Validate QA-QC Middleware API returns error when invalid details(IP/RID) is provided
    [Documentation]    In this test case we validate the Invalid IP/RID error. Make sure you have all valid details
     ...               in request and body and a Invalid ID or RID
    ${APIRESPONSE} =   api call    url=${MW_URL}    auth=basic    usr=middleware    pwd=Password1    rtype=POST     body={"TenantID":"0c130b61-7581-429e-a51a-d77ba142ef8b","VirtualMachineIPAddress":"10.100.249.256","Callback":"callback.servicenow.com","VirtualMachineRID":"NightlyTestVMRHEL74","TaskID":"RITM209090932","Methods":[{"TestName": "check_date","TestId":0,"ExpectedResult":12}]}
    ${STATUS_CODE} =   get response code    ${APIRESPONSE}
    should be equal as integers      ${STATUS_CODE}      400
    ${RESPONSE_JSON} =  get response json   ${APIRESPONSE}
    ${STATUS} =    response should contain text    ${RESPONSE_JSON}    Enter a valid
    should be equal as strings   ${STATUS}     True
