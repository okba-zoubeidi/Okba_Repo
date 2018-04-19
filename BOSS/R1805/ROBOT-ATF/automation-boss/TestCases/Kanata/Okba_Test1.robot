*** Settings ***
Documentation  Okba Test123

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
Test1234
   Given I login and switch to account ${newacc}
   When I switch to Open Operation All Orders

