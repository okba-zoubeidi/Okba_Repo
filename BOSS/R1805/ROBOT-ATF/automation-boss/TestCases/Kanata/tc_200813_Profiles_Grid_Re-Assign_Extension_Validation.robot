*** Settings ***
Documentation  Profile Reassign Extension Validation (tc 200813)

#Keywords Definition file
Resource           ../../RobotKeywords/BOSSKeywords.robot

#Variable files
Resource           ../../Variables/EnvVariables.robot

#BOSS Component
Library			  ../../lib/BossComponent.py    browser=${BROWSER}

#Built in library
Library  String

*** Variables ***
#Pre-condition: This type of product is expected to be available in the account.
${product} =    Connect CLOUD Standard
# Note: Error message does not match testcase.
${error_message_for_three_digit_number} =           Extension is too short.
${extension_three_digit_number} =                   333
# Note: Error message does not match testcase.
${error_message_for_five_digit_number} =            Extension is in use or not valid.
${extension_five_digit_number} =                    55555
# Note: Error message does not match testcase.
${error_message_for_duplicate_number} =             Extension is in use or not valid.
${extension_index_in_profile_record} =              4
${error_message_for_number_starting_with_zero} =    Extension is in use or not valid.
${extension_number_starting_with_zero} =            0123
${error_message_for_number_starting_with_nine} =    Extension is in use or not valid.
${extension_number_starting_with_nine} =            9123

*** Test Cases ***
Profile Reassign Extension Validation (tc 200813)

    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option

    When I open Operations IP PBX Primary Partition
    Then I verify Profiles grid display

    When I select one profile ${product}
    @{profileData}=  and I get first record from profile
    and I click on ReAssign button

    Then I verify reassign wizard is displayed
    and I verify error message ${error_message_for_three_digit_number} when I enter extension ${extension_three_digit_number}
    and I verify error message ${error_message_for_five_digit_number} when I enter extension ${extension_five_digit_number}
    ${extension_duplicate_number} =  Set Variable  @{profileData}[${extension_index_in_profile_record}]
    and I verify error message ${error_message_for_duplicate_number} when I enter extension ${extension_duplicate_number}
    and I verify error message ${error_message_for_number_starting_with_zero} when I enter extension ${extension_number_starting_with_zero}
    and I verify error message ${error_message_for_number_starting_with_nine} when I enter extension ${extension_number_starting_with_nine}

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert

