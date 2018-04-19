*** Settings ***
Documentation    To Edit VCFE Extension List and to validate error message if all the extensions are removed
...              Immani Mahesh Kumar

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
Vcfe Edit Extension list and remove all extensions with DM user
    [Tags]  Regression  	EL
    Given I login to ${URL} with ${DMemail} and ${DMpassword}
    When I switch to "users" page
    #${phone_num}  ${extn}=    and I add user    &{DMUserProfile}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    5003
    Then I verify that User exist in user table  &{DMUserProfile}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    and Set to Dictionary    ${EditExtensionlist02}    extnlist     remove
    i select vcfe component by searching name "${Extensionlist01['extnlistname']}"
    Then I edit extension list  &{EditExtensionlist02}
    [Teardown]  run keywords  i delete vcfe entry by name ${Extensionlist01['extnlistname']}
    ...                       And I log off
    ...                       I check for alert


Vcfe Edit Extension list and remove all extensions with PM user
    [Tags]  Regression  	EL
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    When I switch to "users" page
    ${phone_num}  ${extn}=    and I add user    &{DMUserProfile}
    and Set to Dictionary    ${Extensionlist01}    extnNumber    ${extn}
    Then I verify that User exist in user table  &{PMUserProfile}
    when I switch to "Visual_Call_Flow_Editor" page
    Then I create extension list    &{Extensionlist01}
    and Set to Dictionary    ${EditExtensionlist02}    extnlist     remove
    i select vcfe component by searching name ${Extensionlist01['extnlistname']}
    Then I edit extension list  &{EditExtensionlist02}
     [Teardown]  run keywords  i delete vcfe entry by name ${Extensionlist01['extnlistname']}
    ...                       And I log off
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
