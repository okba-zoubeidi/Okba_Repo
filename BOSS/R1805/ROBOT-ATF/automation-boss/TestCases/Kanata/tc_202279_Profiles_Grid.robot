*** Settings ***
Documentation  This is a test file to check if your dependency installations

Suite Teardown    Close The Browsers
#Keywords Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Env file
Resource          ../../Variables/EnvVariables.robot

#libraries
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library           Collections

*** Variables ***
${ProfilesExtension_id}=    ProfilesExtension
${ProfilesNumber_id}=       ProfilesNumber
# Note: This extension is expected as a precondition for Extension-Only profile.
${ProfilesExtension_value}=    1860
# Note: This number is expected as a precondition for Extension-and-DID profile.
${ProfilesNumber_value}=       1 (408) 300-5160
@{ProfileExtension}     ${ProfilesExtension_id}     ${ProfilesExtension_value}
@{ProfileNumber}        ${ProfilesNumber_id}        ${ProfilesNumber_value}

#Note: Product to filter and the mininum number of records needed.
&{Product}=  product=MiCloud Connect Telephony   minNumber=2

# Ids of various buttons on the profiles UI.
@{expectedEnabledButtonsDefault}=  partitionProfilesDataGridAddButton  partitionProfilesDataGridImportButton   partitionProfilesDataGridExportBtn
@{expectedEnabledButtonsSingleSection}=  partitionProfilesDataGridResetPinButton  partitionProfilesDataGridUnassignButton  partitionProfilesDataGridReAssignButton  partitionProfilesDataGridAddButton  partitionProfilesDataGridEditButton  partitionProfilesDataGridImportButton  partitionProfilesDataGridExportBtn
@{expectedEnabledButtonsTwoSections}=  partitionProfilesDataGridUnassignButton  partitionProfilesDataGridAddButton  partitionProfilesDataGridEditButton  partitionProfilesDataGridImportButton  partitionProfilesDataGridExportBtn

*** Test Cases ***

Profile Grid (tc 202279)
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
    When I open Operations IP PBX Primary Partition
    Then I verify Extension-Only is shown @{ProfileExtension}
    and I verify Extension-and-DID is shown @{ProfileNumber}
    and I verify all column names in Profiles
    and I verify buttons enabled in Profiles @{expectedEnabledButtonsDefault}
    When I select a profile &{Product}
    Then I verify buttons enabled for single profile selection @{expectedEnabledButtonsSingleSection}
    When I select another profile &{Product}
    Then I verify buttons enabled for two profile selection @{expectedEnabledButtonsTwoSections}

    [Teardown]  Run Keywords  I log off
    ...                       I check for alert

