*** Settings ***
Documentation    To add On-Hours Schedule without choosing the time zone
...              Immani Mahesh Kumar

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
Resource          ../VCFE/Variables/Vcfe_variables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String
*** Test Cases ***
01 Create On Hours schedule with out timezone with DM User
     [Tags]    Regression    OHS
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule02}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify On Hours schedule "${OHS_name}" is set for ${accountName1}
    [Teardown]  run keywords  I delete VCFE entry by name ${OHS_name}
    ...                      I log off
    ...                      I check for alert


02 Create On Hours schedule with out timezone with PM User
     [Tags]    Regression    OHS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule02}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify On Hours schedule "${OHS_name}" is set for ${accountName1}
    [Teardown]  run keywords  I delete VCFE entry by name ${OHS_name}
    ...                      I log off
    ...                      I check for alert


03 Create On Hours schedule with out timezone with Staff User
     [Tags]    Regression    OHS
    Given I login to ${url} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule02}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    Then In D2 I verify On Hours schedule "${OHS_name}" is set for ${accountName1}
    [Teardown]  run keywords  I delete VCFE entry by name ${OHS_name}
    ...                      I log off
    ...                      I check for alert



*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{OnHoursSchedule01}

    : FOR    ${key}    IN    @{OnHoursSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${OnHoursSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${OnHoursSchedule02}    ${key}    ${updated_val}