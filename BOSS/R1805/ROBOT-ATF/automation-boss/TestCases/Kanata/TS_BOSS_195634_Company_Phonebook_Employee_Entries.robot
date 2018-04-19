*** Settings ***
Documentation  TC 200032 Call Routing - Basic Routing - Call Forward - Always ForwardPriority

#Suite Setup and Teardown
Suite Setup       Set Init Env

#Keywords1 Definition file
Resource          ../../RobotKeywords/BOSSKeywords.robot

#Variable filesot
Resource          ../../Variables/EnvVariables.robot

#BOSS Component
Library           ../../lib/BossComponent.py    browser=${BROWSER}
Library  String
Library  Collections

*** Test Cases ***
01 Log into Portal as Staff Member, and switch to a Cosmo account, and impersonate a user of that account that has the Decision Maker roll, and an available number(s) to assign a profile to
    Log    ${user_properties}    console=yes
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${TC_195634_Acoount} with ${TC_195634_User} option
    Then I verify "User_Options" contains "${TC_195634_User}"
    When I switch to "users" page

02 Create a user when next available phone number,
    # Create user
    Set to Dictionary   ${user_properties}     au_firstname   FNtestuser1
    Set to Dictionary   ${user_properties}     au_lastname    LNtestuser1
    Set to Dictionary   ${user_properties}     au_businessmail   FNtestuser1.LNtestuser1@workemail.com
    Set to Dictionary   ${user_properties}     au_personalmail   FNtestuser1.LNtestuser1@homeemail.com
    Set to Dictionary   ${user_properties}     au_username    FNtestuser1.LNtestuser1@workemail.com
    Set to Dictionary   ${user_properties}     au_cellphone    4125551234
    Set to Dictionary   ${user_properties}     au_homephone    6135553214
    ${phone_num}  ${extn}=    and I add user    &{user_properties}
    and I sleep "20" seconds
    Then I verify that User exist in user table    &{user_properties}

03 Log into Portal as Staff Member, and switch to a Cosmo account, and impersonate a user of that account that has the Decision Maker roll.
    When I stop impersonating
    and I sleep "5" seconds
    and I log off
    and I sleep "5" seconds
    Given I login to ${URL} with ${bossUsername} and ${bossPassword}
    and I switch to "switch_account" page
    and I switch to account ${TC_195634_Acoount} with ${TC_195634_User} option
    Then I verify "User_Options" contains "${TC_195634_User}"

04 Navigate to Home -> Contacts -> Company Phonebook.
    When I sleep "5" seconds
    and I switch to "home_comapnyPhonebook" page
    Then I verify "personal_contacts_menu" contains "Personal Contacts"

05 Type the first or last name in the column filter fields.
    When I input "${ContractAOB["au_firstname"]}" in "company_phonebook_search_first_name_input"
    and I input "${ContractAOB["au_lastname"]}" in "company_phonebook_search_last_name_input"
    and I sleep "2" seconds
    Then I verify "company_phonebook_entry_list" contains "${ContractAOB["au_firstname"]}"
    and I verify "company_phonebook_entry_list" contains "${ContractAOB["au_firstname"]}"
    and I verify "company_phonebook_entry_list" contains "${phone_num}"
    and I verify "company_phonebook_entry_list" contains "${extn}"

*** Keywords ***
Set Init Env
    ${user_password}=    set variable    MitelRocks!666
    ${user_location}=    set variable    AutoTest_location_l4RYdNE7
    ${billing_location}=    set variable    AutoTest_location_l4RYdNE7
    ${user_properties}=    Create Dictionary
    Set suite variable    &{user_properties}
    Set to Dictionary   ${user_properties}     au_userlocation    ${user_location}
    Set to Dictionary   ${user_properties}     au_location    ${billing_location}
    Set to Dictionary   ${user_properties}     au_password    ${user_password}
    Set to Dictionary   ${user_properties}     au_confirmpassword    ${user_password}
    Set to Dictionary   ${user_properties}     ap_phonetype    Connect CLOUD Standard
    Set to Dictionary   ${user_properties}     ap_phonenumber    random
    Set to Dictionary   ${user_properties}     ap_activationdate    today

    Set to Dictionary   ${user_properties}     hw_addhwphone    False
    Set to Dictionary   ${user_properties}     hw_type    Sale New
    Set to Dictionary   ${user_properties}     hw_model    ShoreTel IP420 - Sale
    Set to Dictionary   ${user_properties}     hw_power    False
    Set to Dictionary   ${user_properties}     hw_power_type    ShoreTel IP Phones Power Supply - Sale

    #Set to Dictionary   ${user_properties}     role    Phone Manager
    Set to Dictionary   ${user_properties}     scope    Account
#    Set to Dictionary   ${user_properties}     request_by    boss automation
#    Set to Dictionary   ${user_properties}     request_source    Email
