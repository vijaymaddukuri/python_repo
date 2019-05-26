*** Settings ***
Documentation     A test suite with a single Gherkin style to validate page2 of web application
...
...               This test will swipe the ploicies to left and right according to the requirement.
Resource          resource.robot
Test Teardown     Close Browser
Library     Collections


*** Test Cases ***
Valid Login
    Given browser is opened to page2
    Swipe the policies to right
    Swipe the policies to left
    Search for policy and move to right

*** Keywords ***
Browser is opened to page2
    Open browser to page2

Swipe the policies to right
    Select from list using Label   xpath=//select[@id="a-listers"]  Pluto
    Click on the element  swapRight
    Element should not contain in the list  //*[@id="a-listers"]   Pluto

Swipe the policies to left
    Select from list using Label   xpath=//select[@id="candidates"]  Pluto
    Click on the element  swapLeft
    Element should not contain in the list  //*[@id="candidates"]   Pluto

Search for policy and move to right
    Click on the element  search
    Input Text    search   Eris
    Click on the element  swapRight
    Element should not contain in the list  //*[@id="a-listers"]   Eris