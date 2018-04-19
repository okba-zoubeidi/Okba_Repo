*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          ../AOB/Variables/aob_variables.robot
#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
Verify UI navigates to Activation page on clicking Dont setup button
    [Tags]  Regression
    Given I login to AOB page
    When I navigate to Location and user page
    And I go to add user page
    Then I verify the page "Users for"
    ${status}=  I check if user is created
    Run Keyword If   '${status}' == 'False'   run keyword   I create User  &{AobUserDetail}
    Run Keyword If   '${status}' == 'False'   run keyword   I click "Save" button
    When I switch bundle and verify text
    When I click on skip user button
    Then I verify the page "Call Handling for"
    ${ch_status}=  I check if call handling is setup
    Run Keyword If   '${ch_status}' == 'False'   run keyword   I select "Set Up" button on call handling page
    Run Keyword If   '${ch_status}' == 'False'   run keyword   I verify the page "Main Number"
    Run Keyword If   '${ch_status}' == 'False'   run keyword   I check "Save" is present
    Run Keyword If   '${ch_status}' == 'False'   run keyword   I check "Cancel" is present
    Run Keyword If   '${ch_status}' == 'True'    run keyword   I check "Update" is present
    Run Keyword If   '${ch_status}' == 'True'    I select "Update" button on call handling page
    Run Keyword If   '${ch_status}' == 'True'    I verify the page "Main Number"
    Run Keyword If   '${ch_status}' == 'True'    I check "Save" is present
    Run Keyword If   '${ch_status}' == 'True'    I check "Cancel" is present

*** Keywords ***
Set Init Env
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${uni_int}=    Generate Random String    4    12345678
    Set suite variable    ${uni_str}
    Set suite variable    ${uni_int}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}

    Set suite variable    &{AobUserDetail}
    : FOR    ${key}    IN    @{AobUserDetail.keys()}
    \    ${updated_val}=    Replace String    ${AobUserDetail["${key}"]}    {rand_int}    ${uni_int}
    \    Set To Dictionary    ${AobUserDetail}    ${key}    ${updated_val}


