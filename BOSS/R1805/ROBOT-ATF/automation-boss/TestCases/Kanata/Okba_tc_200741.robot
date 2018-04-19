
*** Settings ***
Documentation  TC 200741 : Next button check, logged in as DM

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}

#Built in library
Library  String
Library  Collections

*** Test Cases ***
TC 200741 : Next button check, logged in as DM

    Given I login and switch to account ${newacc}
    And I switch to "phone_systems_Add_On_Features" page
    Then I click on manage button of Connect_Scribe_Manage
    Then I log off
