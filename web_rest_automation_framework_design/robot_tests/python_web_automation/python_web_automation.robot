*** Settings ***
Documentation     Suite description
Library     workflow.baseworkflow.BaseWorkflow
*** Variables ***
${CONF DIR}  ../conf//

*** Test Cases ***
UI LOGIN
    [Documentation]    As a user, I want to search for keywords within Google.com.
    [Tags]      VHC-HE WEB AUTOMATION
    [Setup]    Apply Settings From Files    C:\\Users\\madduv\\PycharmProjects\\veche-ta\\conf\\generic.yaml    C:\\Users\\madduv\\PycharmProjects\\veche-ta\\conf\\specific.yaml
    User Opens Browser
    User Closes Browser
    [Teardown]    Reset Settings