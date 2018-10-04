*** Settings ***
Documentation     A test suite with a single Gherkin style to validate page1 of web application
...
...               This test will open the browser and select the VM template and policies

Resource          resource.robot
Test Teardown     Close Browser


*** Test Cases ***
Valid Page1
    Given browser is opened to page1
    Enter the VM template
    Select and Verifiy policies

*** Keywords ***
Browser is opened to page1
    Open browser to page1


Enter the VM template
    Input VM Template   __box0-inner    mysql-rhel4-template

Select and Verifiy policies
    Click on the element    __box3-CbBg
    validate the text with attribute name     //*[@id="__box3"]       aria-checked    true

