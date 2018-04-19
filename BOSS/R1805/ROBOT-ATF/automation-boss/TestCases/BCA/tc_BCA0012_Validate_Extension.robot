*** Settings ***
Documentation    Verify the allocation of default extensions while creating BCA

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
Validate Default Extension
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    &{localBCAinfo}=  copy dictionary  ${BCA_INFO}

    set to dictionary  ${localBCAinfo}  AssignFromLocation  Don't assign a number
    set to dictionary  ${localBCAinfo}  Extension  Validate Default Extension

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  5s
    #3. Create another BCA with default extension and varify it
    &{old_bca}=  copy dictionary  ${localBCAinfo}
    set to dictionary  ${localBCAinfo}  ProfileName  TestBCA2

    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  5s

    ### Verification: varify the extension
    Then I verify BCA  &{localBCAinfo}

    [Teardown]
    I delete BCA  &{old_bca}
    sleep  5s
    I delete BCA  &{localBCAinfo}
    sleep  5s

    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***
