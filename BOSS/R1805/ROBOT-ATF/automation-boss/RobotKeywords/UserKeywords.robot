*** Settings ***
Documentation     Keywords supported for Users page
...               developer- Megha Bansal
...               Comments:

Library    Collections


*** Keywords ***
I add mobility profile
    [Documentation]   This keyword will add mobility profile to a global user via Personal information page
    [Arguments]     &{global_user}
    ${result}=  Run Keyword     add_mobility_profile     &{global_user}
    Should be true   ${result}

I verify mobility checkbox for global user
    [Documentation]   This keyword will verify the presence of mobility checkbox under Bundle feature for a global user during add user
    [Arguments]     &{global_user}
    ${result}=  Run Keyword     verify_mobility_checkbox     &{global_user}
    Should be true   ${result}

I verify swap for globaluser
    [Documentation]   This keyword will verify if the swap functionality is disabled for global user or not
    [Arguments]   &{global_user}
    ${result}=  Run Keyword     verify_swap_globaluser     &{global_user}
    Should be true   ${result}

I verify global user location
    [Documentation]   This keyword will verify the location of global user
    [Arguments]   &{global_user}
    ${result}=  Run Keyword     verify_globaluser_location    &{global_user}
    Should be true   ${result}

I close global user
    [Documentation]   This keyword will close the global user from users page
    [Arguments]   &{global_user}
    ${result}=  Run Keyword     close_user    &{global_user}
    Should be true   ${result}

I get locations from user location dropdown
    [Documentation]   This keyword will verify userLocation dropdown while adding a global user
    ${locList}=  Run Keyword     get_locations_user_location_dropdown
    [Return]      ${locList}
