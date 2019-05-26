*** Settings ***
Library  lib.api_caller.py

*** Variables ***
${API_URL}      http://127.0.0.1:5000/api/v1/domain/


*** Test Cases ***
T1 Test a Multiple of 3 maps to Domain A and assigns role Bing
    ${API_RESPONSE} =   api_call    ${API_URL}    9
    Should be equal as String     ${API_RESPONSE}     The mapped domain is : A , And The role is : Bing

T2 Test a Multiple of 5 maps to Domain B and assigns role Bang
    ${API_RESPONSE} =   api_call    ${API_URL}    25
    Should be equal as String     ${API_RESPONSE}     The mapped domain is : B , And The role is : Bang

T3 Test a Multiple of both 3 and 5 maps to Domain A and B and assigns role Boom
    ${API_RESPONSE} =   api_call    ${API_URL}    15
    Should be equal as String     ${API_RESPONSE}     The mapped domain is : A and B , And The role is : Boom

T4 Test a Multiple of Neither 3 nor 5 doesn't map to any domain and assigns role Meh
    ${API_RESPONSE} =   api_call    ${API_URL}    15
    Should be equal as String     ${API_RESPONSE}     The mapped domain is : None , And The role is : Meh



