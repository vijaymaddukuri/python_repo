*** Settings ***
Documentation     A test suite with tests for project creation.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

Resource          resource.robot

*** Test Cases ***
Valid Login
    Input Username    ${VALID USER}
    Input Password    ${VALID PASSWORD}
    Submit Credentials
    Dashboard Page Should Be Open

Create New Project
    Go To Projects Page
    Create New Project

Update Project Design
    Update Project Design

Run Test Workflow
    Run Test Workflow

*** Keywords ***
Go To Projects Page
    Wait for Angular
    Click Link  xpath=//a[@href='/projects']
    Wait for Angular
    Projects Page Should Be Open

Create New Project
    ${date} =  Get Current Date  result_format=%d%m%H%M%S
    Wait for Angular
    Click Link  xpath=//a[@href='/projects/new']
    Page Should Contain     New Project
    Input Text    model=project.name    Project1_${date}
    Click Element  model=project.type
    Click Element  xpath=//md-option[@value='EHC4.1']
    Click Button  submitButton
    # Wait for Angular
    Projects Page Should Be Open

Update Project Design
    Click Link  xpath=//a[@href='/design']
    # Wait for Angular
    Page Should Contain     3. Upload Data
    Click Link  xpath=//md-list/a[@href='/import']/md-list-item
    Page Should Contain     Upload
    Click Button  xpath=//button[@ng-click='edit()']
    # Wait for Angular
    ${TextFileContent}=    Get File    ${SAMPLE INPUT DATA FILE}
    Input Text  xpath=//textarea  ${TextFileContent}
    # Wait for Angular
    [Timeout]    10min
    Click Button  submitButton
    # Wait for Angular
    Wait Until Element Is Not Visible  submitButton

Run Test Workflow
    Go To    ${TEST WORKFLOW URL}
    Wait Until Element Is Enabled  submitButton
    Click Button  xpath=//play-button[@action='executePlaybook($event)']
    Sleep  20
    # Wait for Angular  timeout=30
    Page Should Contain Element  model=selectedJob.job  timeout=30
    Page Should Contain  100%
    Capture Page Screenshot  filename=selenium-workflow-complete-screenshot-{index}.png
#    Click Link  xpath=//a[@href='/configure']
#    Page Should Contain     Deploy
#    Page Should Contain     MASTER EHC 41 DEPLOY AND CONFIGURE
