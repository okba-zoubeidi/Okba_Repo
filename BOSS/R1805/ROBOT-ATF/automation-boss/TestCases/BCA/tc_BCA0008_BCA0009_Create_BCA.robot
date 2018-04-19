*** Settings ***
Documentation    Create and Delete Bridged Call Appearances

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py

#BOSS Component

Library           ../../lib/BossComponent.py  browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

#Suite Setup   Adding PhoneNumbers

*** Test Cases ***
Create BCA
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}
    set to dictionary  ${localbcainfo}  OtherSettings  ${True}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
    And I switch to "bridged_call_appearances" page
    And I delete BCA  &{localbcainfo}
    sleep  5s
    ### Verification:
    Then I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${False}
    # Check if the phone number is now in available state
    And I switch to "operations_phone_numbers" page
    &{ph_num}=  copy dictionary  ${PHONE_INFO}
    set to dictionary  ${ph_num}  numberRange  ${None}
    ${result}=  verify phone numbers and their status  &{ph_num}
    should be true  ${result}

    [Teardown]

    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}

#Adding PhoneNumbers
#
#    I login to ${URL} with ${bossUsername} and ${bossPassword}
#    I switch to "switch_account" page
#    I switch to account ${accountName1} with ${AccWithoutLogin} option
#
#    &{PhoneNumberInfo}=  copy dictionary  ${PHONE_INFO_US}
#    log many  &{PhoneNumberInfo}
#
#    # change the clientAccount, clientLocation fields
#    set to dictionary  ${PhoneNumberInfo}  clientAccount  ${accountName1}
#    set to dictionary  ${PhoneNumberInfo}  clientLocation  ${locationName}
#
#    log many  &{PhoneNumberInfo}
#
#    I switch to "operations_phone_numbers" page
#    I add PhoneNumber  &{PhoneNumberInfo}
#    I set PhoneNumber state  &{PhoneNumberInfo}


