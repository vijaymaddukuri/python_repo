*** Settings ***
Documentation     Suite description
Library           ehc_e2e.keywords.BaseWorkflow

*** Test Cases ***
[EHC_E2EWF]DEMO - Search keywords with Bing.com
    [Documentation]    As a EHC user, I want to search for keywords within Bing.com.
    [Tags]    E2E WORKFLOW
    [Setup]    Apply Settings From Files    C:\\Data\\Python\\auto_solutions\\frameworks\\ehc\\ehc_e2e\\conf\\generic.yaml    C:\\Data\\Python\\auto_solutions\\frameworks\\ehc\\ehc_e2e\\conf\\specific.yaml
    User Opens Browser
    User Closes Browser
    [Teardown]    Reset Settings

*** Keywords ***
Provided precondition
    Setup system under test
