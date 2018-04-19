*** Settings ***
Documentation  TC 200032 Call Routing - Basic Routing - Call Forward - Always ForwardPriority

#Suite Setup and Teardown
Suite Setup       Set Init Env

Resource    ../../RobotKeywords/BOSSKeywords.robot
Resource    ../../Variables/EnvVariables.robot

Library     ../../lib/BossComponent.py
Library     String
Library     Collections

*** Test Cases ***
TC 200032 Call Routing - Basic Routing - Call Forward - Always ForwardPriority
    Given I login and switch to account AutoTest_Acc_3Dg532wA
#    and I switch to "primary_partition" page
#    When I switch to "primary_partition_profiles" page
    # Create user 1
    ${pr_firstName}=    set variable    FNtestuser1
    ${pr_lastName}=     set variable    LNtestuser1
    ${pr_email1}=    set variable    email${pr_firstName}@${pr_lastName}.com
    Set to Dictionary   ${user_properties}     firstName   autotest${pr_firstName}
    Set to Dictionary   ${user_properties}     lastName    ${pr_lastName}
    Set to Dictionary   ${user_properties}     email   ${pr_email1}
#    Log    ${user_properties}    console=yes
#    And I add a profile with an auto assigned extension   &{user_properties}
#    And I verify the profile is in the profile grid  &{user_properties}
#    And I verify the profile is added to the users table   &{user_properties}
    # Create user 2
    ${pr_firstName}=    set variable    FNtestuser2
    ${pr_lastName}=     set variable    LNtestuser2
    ${pr_email2}=    set variable    email${pr_firstName}@${pr_lastName}.com
    Set to Dictionary   ${user_properties}     firstName   autotest${pr_firstName}
    Set to Dictionary   ${user_properties}     lastName    ${pr_lastName}
    Set to Dictionary   ${user_properties}     email   ${pr_email2}
#    Log    ${user_properties}    console=yes
#    And I add a profile with an auto assigned extension   &{user_properties}
#    And I verify the profile is in the profile grid  &{user_properties}
#    And I verify the profile is added to the users table   &{user_properties}
    When I open Call Routing for user ${pr_email1}
    and I configure always forward to voicemail
    and I verify always forward to voicemail is configured
#    Then I log off

*** Keywords ***
Set Init Env
    ${user_properties}=    Create Dictionary
    Set suite variable    &{user_properties}
    Set to Dictionary   ${user_properties}     profileLocation     AutoTest_location_3Dg532wA
    Set to Dictionary   ${user_properties}     autoExtn    True
