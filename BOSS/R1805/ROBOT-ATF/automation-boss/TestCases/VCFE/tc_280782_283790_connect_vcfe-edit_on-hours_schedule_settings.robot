*** Settings ***
Documentation    To edit On-Hours Schedule settings
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
01 Edit On Hours schedule and change settings with DM User
    [Tags]    Regression    OHS
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule01}
    And i select vcfe component by searching name "${OHS_name}"
    Then I edit on-hours schedule   &{EditOnHoursSchedule03}
    [Teardown]  run keywords  I delete VCFE entry by name ${EditOnHoursSchedule03['scheduleName']}
    ...                      I log off
    ...                      I check for alert


02 Edit On Hours schedule and change settings with PM User
     [Tags]    Regression    OHS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
	when I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule01}
    And i select vcfe component by searching name "${OHS_name}"
    Then I edit on-hours schedule   &{EditOnHoursSchedule03}
    [Teardown]  run keywords  I delete VCFE entry by name ${OHS_name}
    ...                      I log off
    ...                      I check for alert

03 Edit On Hours schedule and change settings with Staff User
    [Tags]    Regression    OHS
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    When I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    I switch to "Visual_Call_Flow_Editor" page
    ${OHS_name}=  I create on-hours schedule   &{OnHoursSchedule01}
    And i select vcfe component by searching name "${OHS_name}"
    Then I edit on-hours schedule   &{EditOnHoursSchedule03}
    [Teardown]  run keywords  I delete VCFE entry by name ${OHS_name}
    ...                      I log off
    ...                      I check for alert



*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{OnHoursSchedule01}
    Set suite variable    &{EditOnHoursSchedule03}

    : FOR    ${key}    IN    @{OnHoursSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${OnHoursSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${OnHoursSchedule01}    ${key}    ${updated_val}

     : FOR    ${key}    IN    @{EditOnHoursSchedule03.keys()}
    \    ${updated_val}=    Replace String    ${EditOnHoursSchedule03["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditOnHoursSchedule03}    ${key}    ${updated_val}