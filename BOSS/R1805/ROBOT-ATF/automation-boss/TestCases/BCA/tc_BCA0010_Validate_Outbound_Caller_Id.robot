*** Settings ***
Documentation    Add BCA with default Outbound caller Id or with no options from the select dropdown "'Select Phone Number…'"

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
Create BCA With Default Outbound Call Id
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2. Create the BCA with default outbound caller Id
    And I create Bridged Call Appearance  ${BCA_INFO}
    sleep  2s
    ### Verification:
    Then I verify BCA  &{BCA_INFO}

    [Teardown]
    I delete BCA  &{BCA_INFO}
    sleep  5s
    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***
