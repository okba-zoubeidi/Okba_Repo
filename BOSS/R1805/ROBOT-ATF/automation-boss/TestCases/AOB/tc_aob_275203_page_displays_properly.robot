*** Settings ***
Documentation     BOSS AOB regression
...               dev-Saurabh Singh


#Suite Setup and Teardown
#Suite Setup       Set Init Env
Suite Teardown    Close The Browsers

#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot
Resource          Variables/aob_variables.robot

#Variable files
Resource          ../../Variables/EnvVariables.robot
#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}

*** Test Cases ***
Navigate to Location and User page
    [Tags]  Sanity
    Given I login to AOB page
    And I verify the page "Welcome"
    Then I navigate to Location and user page
    And I verify the page "Locations and Users"