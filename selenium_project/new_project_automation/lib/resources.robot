*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.

Library          Selenium2Library

*** Variables ***
#GENERIC DETAILS
${SIMSCALE_URL}   https://www.simscale.com/dashboard/
${BROWSER}        Firefox
${DELAY}          1

#LOGIN DETAILS
${USER}     kumrahul
${PASSWORD}    rahul@123

*** Keywords ***
Setup Test Environment
#This Method calls other methods and performs all the actions required to setup the test environment
    Open Browser To Login Page
    Login Page Should Be Open
    Login and Wait for Dashboard Page to Load      ${USER}     ${PASSWORD}
    Sleep    10
    run keyword and continue on failure      Accept Cookies

Open Browser To Login Page
#Open the browser with the desired URL and Maximize the browser window
    Open Browser    ${SIMSCALE_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Login Page Should Be Open
#Vaidate that the Simscale login page is open
    Title Should Be    SimScale Login

Login and Wait for Dashboard Page to Load
#Enter the credentials, login and wait until the Dashboard page loads
    [Arguments]       ${USER}       ${PASSWORD}
    Input Text       id=emailInput      ${USER}
    Input Text       id=passInput       ${PASSWORD}
    Click Button     id=authClick
    Wait Until Page Contains   Dashboard

Accept Cookies
#This is to "Accept" the pop-up for cookies
     Click Element    //*[@id="btn-cookie-message-accept"]

Open New Project Window
#Open the New Project Window
    Click Button      id=newProject
    Wait Until Element Is Visible       id=createNewProjectDialog

Enter New Project Basic Details
#Enter the all the details except the Advanced details
     [Arguments]     ${PROJECT_TITLE}     ${PROJECT_DESCRIPTION}      ${PROJECT_CATEGORY}     ${TAG_SEARCH_KEY}
     Input Text     id=projectTitle       ${PROJECT_TITLE}
     Input Text     id=projectDescription     ${PROJECT_DESCRIPTION}
     Click Element      id=projectCategory
     Wait Until Page Contains    Aerospace
     Click Element         //*[@id="projectCategory"]/div[@class='selectOptions']/div[@class='selectOption']/label[.='${PROJECT_CATEGORY}']
     Input Text        //*[@id="createNewProjectDialog"]//form//span[@class='tagify__input']       ${TAG_SEARCH_KEY}
     Click Element      //div[@class='tagify__dropdown tags-dropdown']/div[@class='tagify__dropdown__item']


Enter New Project Advanced Details
#Enter all the Advanced details
     [Arguments]       ${MEASUREMENT_UNIT}
     Click Element       //*[@id="createNewProjectDialog"]//form/h5
     Click Element       id=measurements
     Click Element      //*[@id="measurements"]/div[@class='selectOptions']/div[@class='selectOption']/label[@for='${MEASUREMENT_UNIT}']

Submit Create Project
#Hit the Submit Project button
     Click Button        //*[@id="createNewProjectDialog"]//form/button[@class='btn btn-medium btn-primary btn-create-new-project inputSubmit']

Go To DashBoard
#Go to Dashboard page
     Go to    ${SIMSCALE_URL}

Validate New Project Created
#In the Dashboard page check if the newly created project exists
      [Arguments]        ${PROJECT_TITLE}
      Page Should Contain       ${PROJECT_TITLE}

Cleanup Created Project
#Delete the Created Project
     Go to     ${SIMSCALE_URL}
     Sleep    10
     Click Element       //div[@class='project-item-body']//p[@class='project-title']
     Sleep   10
     Wait Until Page Contains        About this project
     Click Button       //button[@title='Delete']
     Wait Until Page Contains        Delete Project
     Click Button       //button[@class='btn btn-danger btn-delete-project']
     Wait Until Page Contains        Dashboard

Validate Upgrade Plan
#Click on Upgrade Plan Button and validate it redirects to the appropriate page
     Click Element      //*[@id="createNewProjectDialog"]//form/div[@class="inputGroup inputGroup--toggle inputGroup--toggleProjectVisibility"]/a
     Sleep   10
     Wait Until Page Contains     Professional

Validate Mandatory fields validation
#Validate that error pops-up when mandatory fields are left blank
    [Arguments]        ${NUMBER_OF_MANDATORY_FIELDS}
    Wait Until Element Is Visible      //*[@id="createNewProjectDialog"]//form//span[@class='inputGroup__error']     timeout=20
    Page Should Contain Element       //*[@id="createNewProjectDialog"]//form//span[@class='inputGroup__error']     limit=${NUMBER_OF_MANDATORY_FIELDS}

Teardown Setup
#Call Cleanup Project and close opened browser windows
    Cleanup Created Project
    Close Browser


