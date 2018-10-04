*** Settings ***
Documentation     A test suite with a single test for valid login.
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
    Projects Page Should Be Open
