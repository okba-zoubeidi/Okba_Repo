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


01 Provision the required TN
   [Tags]    GlobalUser
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   When I switch to "switch_account" page
   And I switch to account ${accountName} with ${AccWithoutLogin} option
   When I switch to "phonenumber" page
   I add PhoneNumber    &{PhoneNumberDetails}
   And I set PhoneNumber state    &{PhoneNumberDetails}
   Then I verify PhoneNumber state    &{PhoneNumberDetails}
   I add PhoneNumber  &{PhoneNumberGlobal}
   And I set PhoneNumber state    &{PhoneNumberGlobal}
   Then I verify PhoneNumber state    &{PhoneNumberGlobal}



*** Keywords ***
Set Init Env
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]


    ${PhoneNumberDetails}=    create dictionary


    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    ${PhoneNumberDetails}
    Set suite variable    ${PhoneNumberGlobal}

    Run keyword if    '${country}' == 'Australia'
        ...    Run Keywords
        ...    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_AUS}

        ...    ELSE IF    '${country}' == 'UK'
        ...    Run Keywords
        ...    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_UK}

        ...    ELSE IF    '${country}' == 'US'
        ...    Run Keywords
        ...    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_US}
        ...    AND    set to dictionary  ${PhoneNumberGlobal}  &{PhoneNumber_Global}

        ...    ELSE
        ...    log  Please enter a valid Country name like US, UK or Australia





    #Set suite variable    &{PhoneNumberDetails}
    : FOR    ${key}    IN    @{PhoneNumberDetails.keys()}
    \    ${updated_val}=    Replace String    ${PhoneNumberDetails["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PhoneNumberDetails}    ${key}    ${updated_val}



     : FOR    ${key}    IN    @{PhoneNumberGlobal.keys()}

     \    ${updated_val}=    Replace String    ${PhoneNumberGlobal["${key}"]}    {rand_int}    ${uni_num}
     \    Set To Dictionary    ${PhoneNumberGlobal}    ${key}    ${updated_val}


