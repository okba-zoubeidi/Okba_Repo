*** Settings ***
Documentation     Login to BOSS portal and Validate the presence of Copy BCA  Button
#...               dev-Vasuja
#...               Comments:

#Suite Setup and Teardown
#Suite Setup       Set Init Env
#Suite Teardown    Close The Browsers


#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py


#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String

*** Test Cases ***
1 Login as staff user and Validate the presence of Copy BCA Button
    [Tags]    Regression    BCA
    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option
    ### Actions:
    When I switch to "bridged_call_appearances" page
    ### Verification
    Then I verify the "copy" button in bca

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers