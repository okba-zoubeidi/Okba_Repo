*** Settings ***
Documentation    Validate the user page SCA Info

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
Validate user page SCA info
    [Tags]    Regression

    ### Pre Conditions:  Log in as PM user
    Given I login to ${URL} with ${PMemail} and ${PMpassword}
    And I switch to "users" page

    &{params}=  create dictionary  ScaInfo  ${True}


    # When I select and verify user on phone system users page  ${PMUser}  ${params}
    When I select and verify user on phone system users page  ${PMUser}


    [Teardown]

    Run Keywords  I log off
    ...                       I check for alert
    ...                       # Close The Browsers

*** Keywords ***