*** Settings ***
Documentation    Verify Programming Profile in operations page is removed after deleting BCA

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
Verify deletion of aBCA from D2
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    # call the clean up function
    clean up

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}

    ${aBCA_name}=  set variable  ${PMUser}


    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  AssociatedBCA  ${True}
#    set to dictionary  ${localbcainfo}  AssociatedBCAProfile  ${aBCA_name}
#    set to dictionary  ${localbcainfo}  SelectPhoneNumber  ${phone_number}
    set to dictionary  ${localbcainfo}  Location  ${locationName}

    ### Actions:
    #1. Switch to BCA page
    When I switch to "bridged_call_appearances" page
    #2. Add New aBCA
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    ${ph_num}=  Set Variable  &{localbcainfo}[SelectPhoneNumber]
    ${extn}=  Set Variable  &{localbcainfo}[Extension]
    ${profile_name}=  Set Variable  &{localbcainfo}[AssociatedBCAProfile]

    #3. Checking the aBCA in D2
    #${d2Bca}=  replace string  ${PMUser}  ${SPACE}  _
    #${d2Bca}=  set variable  ${d2Bca}_${ph_num[-4:]}
    ${d2Bca}=  set variable  ${ph_num[-4:]}

    log  ${d2Bca}
    And In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify bridged call appearance ${d2Bca} is set for ${accountName1} ${true}

    #4. Now delete the aBCA
    And I switch to "bridged_call_appearances" page
    And I delete BCA  &{localbcainfo}
    sleep  2s

    ### Verifications:
    #5. Again verify the BCA entry on primary partition profile
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    And In D2 I verify bridged call appearance ${d2Bca} is set for ${accountName1} ${False}

    [Teardown]
    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


