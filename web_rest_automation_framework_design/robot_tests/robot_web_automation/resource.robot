*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           Selenium2Library

*** Variables ***
${SERVER}         localhost:3000
${BROWSER}        Firefox
${DELAY}          1
${VALID USER}     demo
${VALID PASSWORD}    mode
${LOGIN URL}      http://${SERVER}/page1
${Page1 URL}      http://${SERVER}/page1
${WELCOME URL}    http://${SERVER}/welcome.html
${ERROR URL}      http://${SERVER}/error.html
${Page2 URL}      http://${SERVER}/page2

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open

Login Page Should Be Open
    Title Should Be    Login Page

Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    username_field    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    password_field    ${password}

Submit Credentials
    Click Button    login_button

Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Welcome Page


VM Template Page Should Be Open
    Title Should Be    Web Page Design

Open Browser To Page1
    Open Browser    ${Page1 URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Open Browser To Page2
    Open Browser    ${Page2 URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Click on the element
    [Arguments]     ${locator}
    Click Element   ${locator}

Select the checkbox
    [Arguments]     ${locator}
    Select Checkbox     ${locator}

validate the text with attribute name
    [Arguments]     ${locator}  ${attribute}    ${expectedString}
    ${output}   get element attribute   ${locator}  ${attribute}
    Should Be Equal     ${output}     ${expectedString}

Input VM Template
    [Arguments]     ${locator}  ${vmTemplate}
    Input Text    ${locator}    ${vmTemplate}
    Verfiy the Text Field    ${locator}      ${vmTemplate}

Verfiy the Text Field
    [Arguments]     ${locator}     ${expectedString}
    Textfield Value Should Be   ${locator}     ${expectedString}

Select from list using Label
    [Arguments]     ${locator}  ${value}
    Select From List By Label   ${locator}  ${value}

Element should not contain in the list
    [Arguments]     ${locator}  ${value}
    Element Should Not Contain      ${locator}  ${value}


