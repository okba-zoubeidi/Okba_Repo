*** Settings ***
Documentation     Keywords supported for Add-on Features
...               developer- Megha Bansal
...               Comments:

*** Keywords ***

1I click on manage button of "${myfeature:[^"]+}"
    [Documentation]   This keyword will click on manage button of add on feature page of the specified feature
    &{feature}=    Create Dictionary       feature=${myfeature:[^"]+}
	Run Keyword       click on manage button      &{feature}

I add global user to mobility
    [Documentation]   This keyword will add mobility profile to a global user via Add on Features page
    [Arguments]     &{global_user}
    ${result}=  Run Keyword     add_globaluser_mobility     &{global_user}
    Should be true   ${result}
