*** Settings ***
Documentation    1. Select Phone System -> Users -> User -> Phone number -> Prog Buttons
...              2. Click on any of button box or IP phones and click on create New

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
create BCA Through Program Buttons with PM User
    [Tags]    Regression

    ### Pre Conditions:
    Given I login to ${URL} with ${PMemail} and ${PMpassword}

    # Retrieve and use the user phone number which needs a BCA
    ${phone_number}=  I retrieve user phone number  ${PMUser}
    ${phone_number}=  Set Variable  ${SPACE}${phone_number}${SPACE}

    ${bca_name}=  generate_bca_name
    log  ${bca_name}

    &{localbcainfo}=  copy dictionary  ${BCA_INFO}
    set to dictionary  ${localbcainfo}  ProfileName  ${bca_name}
    set to dictionary  ${localbcainfo}  OutboundCallerID  ${phone_number}
    set to dictionary  ${localbcainfo}  AssignFromLocation   Choose from selected location
    set to dictionary  ${localbcainfo}  SelectLongLabel    abcd
    set to dictionary  ${localbcainfo}  SelectShortLabel    abcd
    set to dictionary  ${localbcainfo}  SelectBCA  ${True}


    I switch to "users" page

    #1. Regenerate the element locators on programming box page
    ${line_no}=  generate element locators on program box page  ${PMUser}  Button Box 1  ${None}

    #2. Create a new BCA on programming button page
    set to dictionary  ${localbcainfo}  CreateBcaUsingProgButton     ${True}
    set to dictionary  ${localbcainfo}   SelectType      All
    set to dictionary  ${localbcainfo}  SelectFunction      Bridged Call Appearance
    I create bca from programming button page   ${localbcainfo}



tc_273477 Verify Newly Creted BCA listed on BCA Prog Line for PM
    #1. Again switch to users page and regenerate all locators, because after creating a new bca from programming button
    #tab it lands again in phone tab in phone setting page
    I switch to "account_home" page
    I switch to "users" page

    #2. Regenerate the element locators on programming box page
    ${line_no}=  generate element locators on program box page  ${PMUser}  IP Phones  ${None}


    #9. Select a BCA on programming button page
    And I select bca on user prog buttons page  &{localbcainfo}

tc_273478 Verify Creted BCA is populaed on D2 for PM
    Then In D2 ${D2IP} I login with ${D2User} and ${D2Password}
    and In D2 I verify bridged call appearance "${bca_name}" is set for "${accountName1}"


tc_273476 Verify newly Creted BCA will be listed on BCA page in Phone System for PM
    I switch to "account_home" page
    I switch to "bridged_call_appearances" page
    I delete BCA  &{localbcainfo}
    sleep  5s
    [Teardown]
    Run Keywords  I log off
    ...           I check for alert
    ...           # Close The Browsers

*** Keywords ***
generate_bca_name
    [Documentation]  The keyword generates random bca name
    ${name}=  Generate Random String  8  [LOWER]
    [Return]  ${name}


