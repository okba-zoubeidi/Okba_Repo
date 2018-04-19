*** Settings ***
Documentation    To edit custom schedule with changing time zone
...                 Palla Surya Kumar

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

Suite Setup       Set Init Env

#Variable files
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library     String

*** Test Cases ***
Edit Custom Schedule Change Time Zone as DM:
    [Tags]    Regression    CS
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    I create custom schedule    &{CustomSchedule01}
    Set to Dictionary    ${EditCustomSchedule03}    editName    ${CustomSchedule01["customScheduleName"]}
    and I edit custom schedule    &{EditCustomSchedule03}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify custom schedule "${EditCustomSchedule03["customScheduleName"]}" is set for ${accountName1}
    [Teardown]  run keywords  I delete vcfe entry by name ${EditCustomSchedule03["customScheduleName"]}
    ...                      I log off
    ...                      I check for alert

Edit Custom Schedule Change Time Zone as PM:
    [Tags]    Regression  CS
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    Then I switch to "Visual_Call_Flow_Editor" page
    I create custom schedule    &{CustomSchedule02}
    Set to Dictionary    ${EditCustomSchedule04}    editName    ${CustomSchedule02["customScheduleName"]}
    and I edit custom schedule    &{EditCustomSchedule04}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify custom schedule "${EditCustomSchedule04["customScheduleName"]}" is set for ${accountName1}
    [Teardown]  run keywords  I delete vcfe entry by name ${EditCustomSchedule04["customScheduleName"]}
    ...                      I log off
    ...                      I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}

    Set suite variable    &{CustomSchedule01}
    Set suite variable    &{EditCustomSchedule03}
    Set suite variable    &{CustomSchedule02}
    Set suite variable    &{EditCustomSchedule04}

    : FOR    ${key}    IN    @{EditCustomSchedule03.keys()}
    \    ${updated_val}=    Replace String    ${EditCustomSchedule03["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditCustomSchedule03}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule01.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{EditCustomSchedule04.keys()}
    \    ${updated_val}=    Replace String    ${EditCustomSchedule04["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${EditCustomSchedule04}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{CustomSchedule02.keys()}
    \    ${updated_val}=    Replace String    ${CustomSchedule02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${CustomSchedule02}    ${key}    ${updated_val}
