*** Settings ***
Documentation    Test VIJAY Rest APIs
Library     workflow.baseworkflow_rest.BaseWorkflow
Suite Setup     Initiate Suite

*** Variables ***
${CONF DIR}  C:\\Users\\madduv\\PycharmProjects\\veche-ta\\conf

*** Test Cases ***
CREATE REST SESSION
    start rest session
TEST VIJAY REST API
    test VIJAY api
CLEAN UP
    Reset Settings

*** Keywords ***
Initiate Suite
    Apply Settings From Files       ${CONF DIR}\\generic.yaml       ${CONF DIR}\\rest.yaml