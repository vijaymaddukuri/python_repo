*** Settings ***
Library     Selenium2Library
Library     Collections
Suite Teardown  Close all browsers

*** Test Cases ***

xpath-test
    Open Browser    http://localhost:3000/page1      firefox
    ${output}   get element attribute   //*[@id="__box3"]       aria-checked

*** Keywords ***
Swipe the ploicies by name
    ${ploicy_list}      get text    xpath=//option[2]
    ${index}     Get Index From List     ${ploicy_list}       Pluto
    ${newIndex}     Evaluate    ${index}+1
    Click on the element  xpath=//option[${newIndex}]
    Click on the element  swapRight
    Click on the element   __box3-inner
    Element Should Not Contain   //*[@id="a-listers"]   Pluto

Swipe the ploicies to right by xpath
    Click on the element  xpath=(//option[@value='232'])[2]
    Click on the element  swapRight
    Click on the element   __box3-inner
    Element Should Not Contain   //*[@id="a-listers"]   Pluto
