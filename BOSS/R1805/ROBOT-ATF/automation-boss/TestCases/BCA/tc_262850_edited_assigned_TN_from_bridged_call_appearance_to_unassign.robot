*** Settings ***
Documentation    Edited Assigned TN from Bridged Call Appearance to Unassign

#...               dev-Vasuja
#...               Comments:

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot
Variables          Variables/BCA_Variables.py

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}
#Library           ../../lib/BossComponentBCA.py  browser=${BROWSER}
Library           ../../lib/DirectorComponent.py

#Built in library
Library  String


*** Test Cases ***
1. Login as staff user and Edit Assigned TN from Bridged Call Appearance to Unassign
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  Unassign    True
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  ${None}  Available  Bridged Call Appearance  ${bca_name}  ${True}
    And I switch to "bridged_call_appearances" page
    And I delete BCA  &{localbcainfo}
    sleep  5s
    [Teardown]

    Run Keywords  I log off
    ...           I check for alert

2. Login as DM user and Edit Assigned TN from Bridged Call Appearance to Unassign
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${DMemail} and ${DMpassword}

    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  Unassign    True
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  ${None}  Available  Bridged Call Appearance  ${bca_name}  ${True}
    And I switch to "bridged_call_appearances" page
    And I delete BCA  &{localbcainfo}
    sleep  5s
    [Teardown]

    Run Keywords  I log off
    ...           I check for alert

3. Login as PM user and Edit Assigned TN from Bridged Call Appearance to Unassign
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}

    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}
    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}
    And I switch to "phone_systems_phone_numbers" page
    And I find element on phone number page  ${None}  Active  Bridged Call Appearance  ${bca_name}  ${True}
    set to dictionary  ${localbcainfo}  Unassign    True
    And I edit DNIS from Phone Numbers Page  ${localbcainfo}
    sleep  5s
    ### Verification:
    And I find element on phone number page  ${None}  Available  Bridged Call Appearance  ${bca_name}  ${True}
    And I switch to "bridged_call_appearances" page
    And I delete BCA  &{localbcainfo}
    sleep  5s
    [Teardown]

    Run Keywords  I log off
    ...           I check for alert

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}