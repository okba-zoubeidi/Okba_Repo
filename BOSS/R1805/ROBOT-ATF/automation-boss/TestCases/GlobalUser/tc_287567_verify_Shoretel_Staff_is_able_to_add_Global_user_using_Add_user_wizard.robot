*** Settings ***
Documentation    Suite description
#...               dev-Tantri Tanisha ,Susmitha
...

#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource          ../GlobalUser/Variables/global_variables.robot
Resource          ../../Variables/EnvVariables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}   country=${country}
Library  String
Library  Collections


*** Test Cases ***
03 Add users
    [Tags]    GlobalUser
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName} with ${AccWithoutLogin} option
    When I switch to "users" page
    Log    ${DMUser}    console=yes
    log to console   ${global_countries}
    set to dictionary   ${DMuser}   global_countries    ${global_countries}
    and I add user    &{DMUser}
    Then I verify that User exist in user table    &{DMUser}
    and I add user    &{LocPMUser}
    Then I verify that User exist in user table    &{LocPMUser}

*** Keywords ***
Set Init Env
    @{user_list}=    Create list
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${TestContract}=    create dictionary


    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    @{user_list}
    Set suite variable    ${TestContract}


   

    : FOR    ${key}    IN    @{TestContract.keys()}
    \    ${updated_val}=    Replace String    ${TestContract["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${TestContract}    ${key}    ${updated_val}

    Set suite variable    &{DMUser}
    : FOR    ${key}    IN    @{DMUser.keys()}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMUser}
    : FOR    ${key}    IN    @{LocPMUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${LocPMUser}    ${key}    ${updated_val}

