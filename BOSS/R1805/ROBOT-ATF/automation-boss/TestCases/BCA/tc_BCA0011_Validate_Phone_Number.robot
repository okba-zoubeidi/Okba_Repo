*** Settings ***
Documentation    Create BCA with different Phone number with different options for assign from location

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

*** Test Cases ***
Create BCA With Phone Number option as Dont Assign
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}

    set to dictionary  ${localBCAinfo}  AssignFromLocation  Don't assign a number

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  5s

    ### Verification:
    Then I verify BCA  &{localBCAinfo}

    [Teardown]
    I delete BCA  &{localBCAinfo}
    sleep  5s
    Run Keywords  I log off
    ...           I check for alert

Create BCA With Phone Number option as Choose from all locations
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}

    set to dictionary  ${localBCAinfo}  AssignFromLocation  Choose from all locations

    ### Actions:
    #1.
    Then I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I verify BCA  &{localBCAinfo}

    [Teardown]
    I delete BCA  &{localBCAinfo}
    sleep  10s
    Run Keywords  I log off
    ...           I check for alert

Create BCA With Phone Number option as Choose from selected location
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    When I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}

    set to dictionary  ${localBCAinfo}  AssignFromLocation  Choose from selected location

    ### Actions:
    #1.
    Then I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I verify BCA  &{localBCAinfo}

    [Teardown]
    I delete BCA  &{localBCAinfo}
    sleep  10s
    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***
