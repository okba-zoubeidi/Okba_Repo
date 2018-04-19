*** Settings ***
Documentation    Verify the status of Unassinged TN from BCA to Unassign

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
1. Login as staff user and Verify the status of Unassinged TN from BCA to Unassign
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

    # Check if the phone number is now in available state
    And I switch to "operations_phone_numbers" page
    &{ph_num}=  copy dictionary  ${PHONE_INFO}
    set to dictionary  ${ph_num}  numberRange  ${None}
    ${result}=  verify phone numbers and their status  &{ph_num}
    should be true  ${result}
    sleep  5s
    # Checking the linked phone number in D2
    ${dnis}=  Replace String  ${localbcainfo['SelectPhoneNumber']}  ${SPACE}(  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  )${SPACE}  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  -  ${EMPTY}
    ${dnis}=  set variable  +${dnis}
    log  ${dnis}
    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${True}

    # Now delete the aBCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  &{localbcainfo}
    sleep  2s

    ### Verifications:
    # Again Checking the linked phone number in D2
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${False}

    [Teardown]

    Run Keywords  I log off
    ...           I check for alert

2. Login as DM user and Verify the status of Unassinged TN from BCA to Unassign
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

    # Check if the phone number is now in available state
    And I switch to "operations_phone_numbers" page
    &{ph_num}=  copy dictionary  ${PHONE_INFO}
    set to dictionary  ${ph_num}  numberRange  ${None}
    ${result}=  verify phone numbers and their status  &{ph_num}
    should be true  ${result}
    sleep  5s
    # Checking the linked phone number in D2
    ${dnis}=  Replace String  ${localbcainfo['SelectPhoneNumber']}  ${SPACE}(  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  )${SPACE}  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  -  ${EMPTY}
    ${dnis}=  set variable  +${dnis}
    log  ${dnis}
    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${True}

    # Now delete the aBCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  &{localbcainfo}
    sleep  2s

    ### Verifications:
    # Again Checking the linked phone number in D2
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${False}
    [Teardown]

    Run Keywords  I log off
    ...           I check for alert

3. Login as PM user and Verify the status of Unassinged TN from BCA to Unassign
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

    # Check if the phone number is now in available state
    And I switch to "operations_phone_numbers" page
    &{ph_num}=  copy dictionary  ${PHONE_INFO}
    set to dictionary  ${ph_num}  numberRange  ${None}
    ${result}=  verify phone numbers and their status  &{ph_num}
    should be true  ${result}
    sleep  5s
    # Checking the linked phone number in D2
    ${dnis}=  Replace String  ${localbcainfo['SelectPhoneNumber']}  ${SPACE}(  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  )${SPACE}  ${EMPTY}
    ${dnis}=  Replace String  ${dnis}  -  ${EMPTY}
    ${dnis}=  set variable  +${dnis}
    log  ${dnis}
    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${True}

    # Now delete the aBCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  &{localbcainfo}
    sleep  2s

    ### Verifications:
    # Again Checking the linked phone number in D2
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And I verify DNIS in D2  ${dnis}  ${accountName1}  ${False}
    [Teardown]

    Run Keywords  I log off
    ...           I check for alert


*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}