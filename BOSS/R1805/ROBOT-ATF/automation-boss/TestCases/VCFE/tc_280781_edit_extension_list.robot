*** Settings ***
Documentation    To add VCFE Pickup Group
...              Saurabh Singh

Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../VCFE/Variables/Vcfe_variables.robot
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../lib/DirectorComponent.py
Library  String
#Test Setup      run keywords   Given I login to ${URL} with AutoTest_iW53qRaQ@shoretel.com and Abc123!!
#...             ${phone_num}  ${extn}=    and I add user    &{DMUserProfile}
#...             log to console  ${phone_num}
#...             and Set to Dictionary    ${Extensionlist01}    extnNumber    ${extn}

*** Test Cases ***
Vcfe Create Extension list with DM user
    [Tags]    Regression    EL    AUS    UK
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    Set to Dictionary    ${Extensionlist01}    extnNumber    ${user_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    and Set to Dictionary    ${EditExtensionlist01}    editName    ${Extensionlist01['extnlistname']}
    Set to Dictionary    ${EditExtensionlist01}    extnNumber    ${user2_extn}
    when I switch to "Visual_Call_Flow_Editor" page
    And i select vcfe component by searching name "${Extensionlist01['extnlistname']}"
    Then I edit extension list  &{EditExtensionlist01}
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify extension list "${Extensionlist01['extnlistname']}" is set for ${accountName1}
    [Teardown]  run keywords  And I log off
    ...                       I check for alert

*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    4    12345678
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]

    Set suite variable    ${uni_str}

    Set suite variable    &{Extensionlist01}
    Set suite variable    &{DMUserProfile}
    Set suite variable    &{DMUserProfile1}

    : FOR    ${key}    IN    @{Extensionlist01.keys()}
    \    ${updated_val}=    Replace String    ${Extensionlist01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Extensionlist01}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{DMUserProfile.keys()}
    \    ${updated_val}=    Replace String    ${DMUserProfile["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUserProfile}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{DMUserProfile1.keys()}
    \    ${updated_val}=    Replace String    ${DMUserProfile1["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUserProfile1}    ${key}    ${updated_val}
