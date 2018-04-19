*** Settings ***
Documentation    Verify the "Bridged Call Appearance" page UI

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py

#BOSS Component
Library           ../../lib/BossComponent.py
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

*** Test Cases ***
Verify BCA Page M5 Portal Bread Crumb
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    ### Actions:
    When I switch to "bridged_call_appearances" page

    ### Verification  bread crumb   "Home -> Phone System -> BOSS_AUTO_68 -> Bridged Call Appearances"
    Then I varify bca m5portal bread crumb  ${accountName1}

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***
