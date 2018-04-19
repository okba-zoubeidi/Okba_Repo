*** Settings ***
Documentation    Verify the Edit page of aBCA

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
Verify UI of Edit page for aBCA
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    # call the clean up function
    clean up

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  AssociatedBCA  ${True}

    ### Actions:
    #1. Switch to BCA page
    When I switch to "bridged_call_appearances" page
    #2. Add New aBCA

    And I create Bridged Call Appearance  ${localbcainfo}

    set to dictionary  ${localbcainfo}  AssociatedBCAProfile  &{localbcainfo}[AssociatedBCAProfile]
    set to dictionary  ${localbcainfo}  SelectPhoneNumber  &{localbcainfo}[SelectPhoneNumber]
    set to dictionary  ${localbcainfo}  AssociatedBCAExtn  &{localbcainfo}[Extension]
    set to dictionary  ${localbcainfo}  Location  ${locationName}

    And I verify BCA  &{localbcainfo}

    ### Verifications:
    #3. Verify the Edit aBCA page
#    Then I switch to "bridged_call_appearances" page
    And I verify edit bca page  &{localbcainfo}

    [Teardown]
#    I switch to "bridged_call_appearances" page
    Then I delete BCA  &{localbcainfo}
    sleep  2s
    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***

generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


