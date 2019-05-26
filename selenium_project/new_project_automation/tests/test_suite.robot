*** Settings ***
Resource     ../lib/resources.robot
Suite Setup       Setup Test Environment
Suite Teardown    Teardown Setup

*** Variables ***


#NEW PROJECT DETAILS
${PROJECT_TITLE}      rk_test_automation
${PROJECT_DESCRIPTION}    this is a test project created by automation
${PROJECT_CATEGORY}      Testing
${TAG_SEARCH_KEY}        tes
${MEASUREMENT_UNIT}      US_CUSTOMARY  #MEASUREMENT_UNIT :
                                       #${MEASUREMENT_UNIT} = US_CUSTOMARY ,for English (Inch, Pound, Second, Fahrenheit)
                                       #${MEASUREMENT_UNIT} = SI , for SI (Meter, Kilogram, Second, Kelvin)
${NUMBER_OF_MANDATORY_FIELDS}     2


*** Test Cases ***
TC1 Test End To End Creation of New Project
    Open New Project Window
    Enter New Project Basic Details      ${PROJECT_TITLE}     ${PROJECT_DESCRIPTION}     ${PROJECT_CATEGORY}    ${TAG_SEARCH_KEY}
    Enter New Project Advanced Details       ${MEASUREMENT_UNIT}
    Submit Create Project
    Go To DashBoard
    Validate New Project Created      ${PROJECT_TITLE}

TC3 Test form cannot be submitted without filling mandatory fields
    Go To DashBoard
    Open New Project Window
    Submit Create Project
    Validate Mandatory fields Validation      ${NUMBER_OF_MANDATORY_FIELDS}


TC2 Test Redirection to Upgrade Plan Page
    Go To DashBoard
    Open New Project Window
    Validate Upgrade Plan






