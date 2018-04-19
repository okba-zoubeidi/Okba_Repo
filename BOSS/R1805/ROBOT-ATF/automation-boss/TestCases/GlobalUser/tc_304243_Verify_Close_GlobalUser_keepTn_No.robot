*** Settings ***
Documentation    Suite description
...               dev-Megha Bansal
...


Resource    ../../Variables/EnvVariables.robot
Resource    ../../RobotKeywords/BossKeywords.robot

Resource          ../GlobalUser/Variables/global_variables.robot

Library			  ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***

1. Global User : Close Global User - KeepTn - no
    [Tags]    GlobalUser
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   When I switch to "switch_account" page
   And I switch to account ${accountName1} with ${AccWithoutLogin} option
   And I switch to "users" page
   then I verify the page "users"
   And I close global user      &{globaluser_close_no}

