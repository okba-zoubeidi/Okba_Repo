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
Delete BCA
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}
    set to dictionary  ${BCA_INFO}  OutboundCallerID  ${phone_number}
    set to dictionary  ${BCA_INFO}  OtherSettings  ${True}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${BCA_INFO}
    sleep  2s
    ### Verification:
    #1.
    Then I verify BCA  &{BCA_INFO}
    #2.
    And I verify deletion of BCA  &{BCA_INFO}
    sleep  5s

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers
