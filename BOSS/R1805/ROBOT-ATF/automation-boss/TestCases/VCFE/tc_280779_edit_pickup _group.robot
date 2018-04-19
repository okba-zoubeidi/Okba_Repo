*** Settings ***
Documentation    To add VCFE Pickup Group
...              Saurabh Singh

Suite Setup       Set Init Env

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
#Resource          tc_280747_add_pickup_group.robot
Resource          ../../Variables/LoginDetails.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String

*** Test Cases ***
Vcfe edit Pickup group with DM user
    [Tags]    Regression
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I create pickup group    &{Pickupgroupedit_DM}
    Set to Dictionary    ${Pickupgroupedit}    PGExtn    ${extn_num}
    and I edit pickup group    &{Pickupgroupedit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroupedit['pickupgpname']}" with extension "${Pickupgroupedit['PGExtn']}" is set for ${accountName1}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

Vcfe edit Pickup group with PM user
    [Tags]    Regression
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    ${extn_num}=    I create pickup group    &{Pickupgroupedit_PM}
    Set to Dictionary    ${Pickupgroupedit}    PGExtn    ${extn_num}
    and I edit pickup group    &{Pickupgroupedit}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And in D2 I verify pickup group "${Pickupgroupedit['pickupgpname']}" with extension "${Pickupgroupedit['PGExtn']}" is set for ${accountName1}
    [Teardown]  run keywords  I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{Pickupgroupedit}
    : FOR    ${key}    IN    @{Pickupgroupedit.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroupedit["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroupedit}    ${key}    ${updated_val}

    Set suite variable    &{Pickupgroupedit_DM}
    : FOR    ${key}    IN    @{Pickupgroupedit_DM.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroupedit_DM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroupedit_DM}    ${key}    ${updated_val}

    Set suite variable    &{Pickupgroupedit_PM}
    : FOR    ${key}    IN    @{Pickupgroupedit_PM.keys()}
    \    ${updated_val}=    Replace String    ${Pickupgroupedit_PM["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Pickupgroupedit_PM}    ${key}    ${updated_val}

