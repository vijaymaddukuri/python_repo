*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           Selenium2Library
Library           AngularJSLibrary
Library           DateTime
Library           OperatingSystem
Library           XvfbRobot
# http://robotframework.org/Selenium2Library/Selenium2Library.html

*** Variables ***
${SERVER}         localhost:9000
${BROWSER}        Chrome
${DELAY}          0
${VALID USER}     admin@ozone.com
${VALID PASSWORD}    ozone
${LOGIN URL}      http://${SERVER}/
${WELCOME URL}    http://${SERVER}/projects
${PROJECTS URL}    http://${SERVER}/projects
${ERROR URL}      http://${SERVER}/error.html
${TEST WORKFLOW URL}      http://${SERVER}/ansible/run?component=_test_workflow
${SAMPLE INPUT DATA FILE}  browser/input/InputFile.txt

*** Keywords ***
Open Browser To Login Page
    Start Virtual Display    1600    900
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    #Title Should Be    Login Page
    Page Should Contain  Login
    Wait for Angular

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open
    Wait for Angular

Input Username
    [Arguments]    ${username}
    Input Text    model=vm.user.email    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    model=vm.user.password    ${password}

Submit Credentials
    Click Button    xpath=//button[@type='submit']
    Wait for Angular

Dashboard Page Should Be Open
    Location Should Be    ${WELCOME URL}
    # Title Should Be    Welcome Page

Projects Page Should Be Open
    Page Should Contain  Projects


