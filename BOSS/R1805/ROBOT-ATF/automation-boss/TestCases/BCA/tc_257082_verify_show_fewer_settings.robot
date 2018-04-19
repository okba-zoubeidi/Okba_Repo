*** Settings ***
Documentation    Verify the Show Fewer Settings link on Add BCA page

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
Verify Show Fewer Settings on Add BCA Page
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    ### Actions:
    When I switch to "bridged_call_appearances" page

    ### Verification
    Then I verify show less settings in add bca page

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***