*** Settings ***
Documentation    Create, Edit and then varify that the changed in Edit operations
...   are reflected in BCA

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
Verify the changes in Edit are reflected in BCA
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    And I switch to account ${accountName1} with ${AccWithoutLogin} option

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OtherSettings  ${True}

    ### Actions:
    #1.
    When I switch to "bridged_call_appearances" page
    #2.
    And I create Bridged Call Appearance  ${localbcainfo}
    And I verify BCA  &{localbcainfo}

    #3. Edit the BCA
    # Change some of the fileds
    set to dictionary  ${localbcainfo}  Location  ${locationName}
    set to dictionary  ${localbcainfo}  CallForwardBusy  12 calls
    set to dictionary  ${localbcainfo}  CallForwardNoAnswer  8 rings

    And I edit BCA  ${localbcainfo}

    ### Verification
    #4. Navigate to the Edit BCA page and verify the Edit BCA UI
    And I verify edit bca page  &{localbcainfo}

    [Teardown]
    I delete BCA  &{localbcainfo}
    sleep  2s
    Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***
generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}