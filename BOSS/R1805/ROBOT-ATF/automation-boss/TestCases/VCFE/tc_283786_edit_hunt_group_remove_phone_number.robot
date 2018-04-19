*** Settings ***
Documentation     Login to BOSS portal and Edit Hunt Group - Remove Phone Number
#...               dev-Vasuja
#...               Comments:

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers


#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Resource           ../VCFE/Variables/Vcfe_variables.robot


#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py
Library  String

*** Test Cases ***
1 Login as staff user and Edit Hunt Group - Remove Phone Number
    [Tags]    Regression   HG
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupStaff}    hglocation    ${locationName}
    Set to Dictionary    ${HuntgroupStaff}    hg_phonenumber    random
    ${extn_num}=    Then I create hunt group    &{HuntgroupStaff}
    Set to Dictionary    ${HuntgroupStaff}    HGExtn    ${extn_num}
    And I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    hg_phonenumber    Delete
    And I edit hunt group  &{HuntgroupEdit}
    And I select vcfe component by searching extension "${HuntgroupStaff['HGExtn']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupStaff['HGExtn']}
    ...                       I log off
    ...                       I check for alert

2 Login as staff user and Edit Hunt Group - Remove Phone Number
    [Tags]    Regression   HG
    Given I login to ${URL} with ${phoneDMUser01["user_email"]} and ${phoneDMUser01["password"]}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupDM}    hglocation    ${locationName}
    Set to Dictionary    ${HuntgroupDM}    hg_phonenumber    random
    ${extn_num}=    Then I create hunt group    &{HuntgroupDM}
    Set to Dictionary    ${HuntgroupDM}    HGExtn    ${extn_num}
    And I select vcfe component by searching extension "${HuntgroupDM['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    hg_phonenumber    Delete
    And I edit hunt group  &{HuntgroupEdit}
    And I select vcfe component by searching extension "${HuntgroupDM['HGExtn']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupDM['HGExtn']}
    ...                       I log off
    ...                       I check for alert

3 Login as staff user and Edit Hunt Group - Remove Phone Number
    [Tags]    Regression   HG
    Given I login to ${URL} with ${phonePMUser01["user_email"]} and ${phonePMUser01["password"]}
    And I switch to "Visual_Call_Flow_Editor" page
    Set to Dictionary    ${HuntgroupPM}    hglocation    ${locationName}
    Set to Dictionary    ${HuntgroupPM}    hg_phonenumber    random
    ${extn_num}=    Then I create hunt group    &{HuntgroupPM}
    Set to Dictionary    ${HuntgroupPM}    HGExtn    ${extn_num}
    And I select vcfe component by searching extension "${HuntgroupPM['HGExtn']}"
    Set to Dictionary    ${HuntgroupEdit}    hg_phonenumber    Delete
    And I edit hunt group  &{HuntgroupEdit}
    And I select vcfe component by searching extension "${HuntgroupPM['HGExtn']}"
    Then I verify updated hunt group value    &{HuntgroupEdit}
    And I switch to "Visual_Call_Flow_Editor" page
    [Teardown]  run keywords  I delete vcfe entry for ${HuntgroupPM['HGExtn']}
    ...                       I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{HuntgroupStaff}
    Set suite variable    &{HuntgroupDM}
    Set suite variable    &{HuntgroupPM}



    : FOR    ${key}    IN    @{HuntgroupStaff.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupStaff["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupStaff}    ${key}    ${updated_val}


    : FOR    ${key}    IN    @{HuntgroupDM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupDM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupDM}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{HuntgroupPM.keys()}
    \    ${updated_val}=    Replace String    ${HuntgroupPM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${HuntgroupPM}    ${key}    ${updated_val}
