*** Settings ***
Documentation    Add, Copy and Delete Bridged Call Appearances

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
Copy BCA
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    ${bca_name}=  generate_bca_name
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OtherSettings  ${True}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    sleep  2s
    #3 Verifing the added bca
    And I verify BCA  &{localbcainfo}
    #4 Copy the BCA to another
    And I copy BCA  ${localbcainfo}
    #5 Verify the copied BCA
    ${old_bca_name}=  set variable  ${localbcainfo}[ProfileName]
    ${copy_bca_name}=  set variable  ${localbcainfo}[BcaCopyProfileName]
    set to dictionary  ${localbcainfo}  ProfileName  ${copy_bca_name}
    Then I switch to "bridged_call_appearances" page
    And I verify BCA

    [Teardown]
    I delete BCA  &{localbcainfo}
    sleep  5s
    set to dictionary  ${localbcainfo}  ProfileName  ${old_bca_name}
    I delete BCA  &{localbcainfo}
    sleep  5s
    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***
generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}
