*** Settings ***
Documentation  Login To Boss Portal And Edit An Auto Attendant With Custom Schedule
...            Mahesh
Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/LoginDetails.robot
Resource          ../../Variables/EnvVariables.robot
Resource          ../../Variables/AutoAttendantInfo.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py

*** Test Cases ***
01 Edit Auto Attendant and assign a custom Schedule as DM user
    [Tags]    Regression        AA
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule03}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component  CustomSchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA04}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${CustomSchedule03['customScheduleName']}
    ...               I log off
    ...               I check for alert


02 Edit Auto Attendant and assign a custom Schedule as PM user
    [Tags]    Regression        AA
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule03}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    Assign_vcfe_component  CustomSchedule
    Set to Dictionary    ${EditAA04}    Assign_vcfe_Name    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA04}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${CustomSchedule03['customScheduleName']}
    ...               I log off
    ...               I check for alert


03 Edit Auto Attendant and assign a custom Schedule as Staff user
    [Tags]    Regression        AA
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "Visual_Call_Flow_Editor" page
    And I create custom schedule    &{CustomSchedule03}
    ${extn_num}=   I add Auto-Attendant    &{AA_01}
    Set to Dictionary    ${AA_01}    AA_Extension    ${extn_num}
    Then I select vcfe component by searching extension "${extn_num}"
    Set to Dictionary    ${EditAA04}    customScheduleName    ${CustomSchedule03['customScheduleName']}
    And I edit Auto-Attendant     &{EditAA04}
    [Teardown]  run keywords  I delete vcfe entry for ${extn_num}
    ...               I delete VCFE entry by name ${CustomSchedule03['customScheduleName']}


*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{CustomSchedule03}

    : FOR    ${key}    IN    @{CustomSchedule03.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule03["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule03}    ${key}    ${updated_val}

