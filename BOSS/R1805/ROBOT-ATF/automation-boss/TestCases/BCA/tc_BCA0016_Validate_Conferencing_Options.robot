*** Settings ***
Documentation    Verify Differenct conferencing options on Add BCA page

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
Validate Conferencing Options on Add BCA Page
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    ### Actions:
    When I switch to "bridged_call_appearances" page

    ### Verification
    Then I varify conferencing options on add bca page

    [Teardown]
    Run Keywords  I log off
    ...           I check for alert

Create BCA with Conferencing Option Disable Conferencing
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    clean up

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localBCAinfo}  AssignFromLocation  Don't assign a number
    set to dictionary  ${localBCAinfo}  OtherSettings  ${True}

    ### Actions:
    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  5s
    ### Verification
    Then I verify BCA  &{localBCAinfo}

    [Teardown]
    I delete BCA  &{localBCAinfo}
    sleep  5s
    Run Keywords  I log off
    ...           I check for alert

Create BCA with Conferencing Option Enable Others May Not Join
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    clean up

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localBCAinfo}  AssignFromLocation  Don't assign a number
    set to dictionary  ${localBCAinfo}  OtherSettings  ${True}
    set to dictionary  ${localBCAinfo}  ConferencingOptions  Enable, others may not join
    #set to dictionary  ${localBCAinfo}  EnableToneWhenPartiesJoinOrLeave  ${True}

    ### Actions:
    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  5s
    ### Verification
    Then I verify BCA  &{localBCAinfo}

    [Teardown]
    I delete BCA  &{localBCAinfo}
    sleep  5s
    Run Keywords  I log off
    ...           I check for alert

Create BCA with Conferencing Option Enable Others May Join
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    clean up

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localBCAinfo}  AssignFromLocation  Don't assign a number
    set to dictionary  ${localBCAinfo}  OtherSettings  ${True}
    set to dictionary  ${localBCAinfo}  ConferencingOptions  Enable, others may join
    #set to dictionary  ${localBCAinfo}  EnableToneWhenPartiesJoinOrLeave  ${True}

    ### Actions:
    When I switch to "bridged_call_appearances" page
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  5s
    ### Verification
    Then I verify BCA  &{localBCAinfo}

    [Teardown]
    I delete BCA  &{localBCAinfo}
    sleep  5s
    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***