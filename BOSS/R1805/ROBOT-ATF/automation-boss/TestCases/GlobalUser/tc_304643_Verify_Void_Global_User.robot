*** Settings ***
Documentation    Suite description
...               dev-Megha Bansal
...


Resource    ../../Variables/EnvVariables.robot
Resource    ../../RobotKeywords/BossKeywords.robot

Resource          ../GlobalUser/Variables/global_variables.robot

Library			  ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***

1. Global User : Void Global User - KeepTn - no
    [Tags]    GlobalUser
   Given I login to ${URL} with ${bossUsername} and ${bossPassword}
   When I switch to "switch_account" page
   And I switch to account ${accountName1} with ${AccWithoutLogin} option
   And I switch to "services" page
   then I verify the page "services"
   ${serviceTn}=  I void global user service   &{globaluser_void}
   And I switch to "switch_account" page
   And I switch to account ${systemAccount} with ${AccWithoutLogin} option
   And I switch to "phonenumber" page
   then I verify the page "Phone Numbers"
   then I verify status of ${serviceTn}     &{globaluser_void}


