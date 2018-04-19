Testcase:  TC_288477_Verify that for global user the option to Swap should be disabled.robot

*** Settings ***
Documentation   Verify that Type dropdown is disabled for global user in update TN Wizard.


#Variable files

Resource          ../../RobotKeywords/BOSSKeywords.robot

Resource          ../../Variables/EnvVariables.robot

Resource          ../../Variables/PhoneNumberInfo.robot

Resource          ../../Variables/UserInfo.robot

#Resource          ../../Variables/LoginDetails.robot

Library           ../../lib/BossComponent.py    browser=${BROWSER}

#Library           ../../lib/BossComponent.py    browser=${BROWSER}    country=${country}
Library           ../../lib/DirectorComponent.py
#Library           PPhoneInterface

Library     String
Library     Collections


*** Test Cases ***
Verify that for global user the option to Swap should be disabled.
    [Tags]    GLOBAL
    Given i login to ${URL} with ${bossUsername} and ${bossPassword}
    And I switch to "switch_account" page
    when I switch to account ${SCOCosmoAccount} with ${AccWithoutLogin} option
 #   I add PhoneNumber  &{PhoneNumber_Global_UK}
     When I switch to "users" page
     and I verify UserFields state  ${username}


     [Teardown]  run keywords  I log off
    ...                      I check for alert
     #Then I verify that User exist in user table    &{DMProfUser}

#    ${phone_num}  ${extn}=    and I add user    &{DMProfUser}
#    Set to Dictionary    ${DMProfUser}    ap_phonenumber    ${phone_num}
#    Set to Dictionary    ${DMProfUser}    ap_extn    ${extn}
#    Then I verify that User exist in user table    &{DMProfUser}
#    and I switch to "services" page
#    and I verify profile updated in service table    &{DMProfUser}




 #   I verify profile updated in service table
#    When I switch to "phonenumber" page
#    ${Updatephoneform}=    create dictionary  TnType=disabled
#    Set to Dictionary   ${PhoneNumber_Global_UK}    global_no_check     True
#    Set to Dictionary   ${PhoneNumber_Global_UK}    updateformfield     ${Updatephoneform}
#    and I set PhoneNumber state    &{PhoneNumber_Global_UK}

#    [Teardown]  run keywords
#    ...                      I log off
#    ...                      I check for alert

 #   if params['global_no_check']=="True":
    #And i select checkbox and click update "phonenumber" page

   # Then I check for "Global User" in Type drop down


*** Keywords ***
Provided precondition
    Setup system under test

    *** Keywords ***
Set Init Env
    @{user_list}=    Create list
    ${uni_num}=    Generate Random String    6    [NUMBERS]
    ${uni_str}=    Generate Random String    8    [LETTERS][NUMBERS]
    ${TestContract}=    create dictionary
    ${CustomSchedule_DM}=    create dictionary
    ${CustomSchedule_PM}=    create dictionary
    ${PhoneNumberDetails}=    create dictionary
    ${InvoiceDetails}=    create dictionary
    ${geolocationDetails}=    create dictionary
    ${geolocation_close}=    create dictionary
    ${PartitionDetails}=    create dictionary

    Set suite variable    ${uni_str}
    Set suite variable    ${uni_num}
    Set suite variable    @{user_list}
    Set suite variable    ${TestContract}
    Set suite variable    ${CustomSchedule_DM}
    Set suite variable    ${CustomSchedule_PM}
    Set suite variable    ${PhoneNumberDetails}
    Set suite variable    ${PhoneNumberGlobal}
    Set suite variable    ${InvoiceDetails}
    Set suite variable    ${geolocationDetails}
    Set suite variable    ${geolocation_close}
    Set suite variable    ${PartitionDetails}

    Run keyword if    '${country}' == 'Australia'
        ...    Run Keywords
        ...    set to dictionary  ${TestContract}  &{Contract_Aus}
        ...    AND    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_AUS}
        ...    AND    set to dictionary  ${CustomSchedule_DM}   &{CustomScheduleDM_Aus}
        ...    AND    set to dictionary  ${CustomSchedule_PM}   &{CustomSchedulePM_Aus}
        ...    AND    set to dictionary  ${InvoiceDetails}   &{Invoice_AUS}
        ...    AND    set to dictionary  ${geolocationDetails}   &{geolocation_AUS}
        ...    AND    set to dictionary  ${geolocation_close}   &{geolocation_close_AUS}
        ...    AND    set to dictionary  ${PartitionDetails}   &{Partition_AUS}

        ...    ELSE IF    '${country}' == 'UK'
        ...    Run Keywords
        ...    set to dictionary  ${TestContract}  &{Contract_UK}
        ...    AND    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_UK}
        ...    AND    set to dictionary  ${CustomSchedule_DM}   &{CustomScheduleDM_UK}
        ...    AND    set to dictionary  ${CustomSchedule_PM}   &{CustomSchedulePM_UK}
        ...    AND    set to dictionary  ${InvoiceDetails}   &{Invoice_UK}
        ...    AND    set to dictionary  ${geolocationDetails}   &{geolocation_UK}
        ...    AND    set to dictionary  ${geolocation_close}   &{geolocation_close_UK}
        ...    AND    set to dictionary  ${PartitionDetails}   &{Partition_UK}

        ...    ELSE IF    '${country}' == 'US'
        ...    Run Keywords
        ...    set to dictionary  ${TestContract}   &{Contract02}
        ...    AND    set to dictionary  ${PhoneNumberDetails}  &{PhoneNumber_US}
        ...    AND    set to dictionary  ${PhoneNumberGlobal}  &{PhoneNumber_Global}
        ...    AND    set to dictionary  ${CustomSchedule_DM}   &{CustomSchedule_DM_US}
        ...    AND    set to dictionary  ${CustomSchedule_PM}   &{CustomSchedule_PM_US}
        ...    AND    set to dictionary  ${InvoiceDetails}   &{Invoice_US}
        ...    AND    set to dictionary  ${geolocationDetails}   &{geolocation_US}
        ...    AND    set to dictionary  ${geolocation_close}   &{geolocation_close_US}
        ...    AND    set to dictionary  ${PartitionDetails}   &{Partition_US}
        ...    AND    set to dictionary  ${PartitionDetails}   &{Partition_US}

        #...    AND    log to console     "==============DEBUG================"
        #...    AND    log to console     ${PhoneNumberGlobal}
        ...    ELSE
        ...    log  Please enter a valid Country name like US, UK or Australia


#    : FOR    ${key}    IN    @{TestContract.keys()}
#    \    ${updated_val}=    Replace String    ${TestContract["${key}"]}    {rand_str}    ${uni_str}
#    \    Set To Dictionary    ${TestContract}    ${key}    ${updated_val}
#
#    Set To Dictionary    ${TestContract}    accountName    BOSSTest
#    Set To Dictionary    ${TestContract}    locationName    Melbourne, Australia
#    Set To Dictionary    ${TestContract}    email    dmtest@user1.com
#    Set To Dictionary    ${TestContract}    location    Melbourne, Australia
#    Set To Dictionary    ${PhoneNumberDetails}    clientAccount    BOSSTest
#    Set To Dictionary    ${PhoneNumberDetails}    clientLocation    Melbourne, Australia

    Set To Dictionary    ${TestContract}    accountName    GlobalUsers
    Set To Dictionary    ${TestContract}    locationName    	location3
    Set To Dictionary    ${TestContract}    email    ess@global.com
    Set To Dictionary    ${TestContract}    location    	location3
    Set To Dictionary    ${PhoneNumberDetails}    clientAccount    GlobalUsers
    Set To Dictionary    ${PhoneNumberDetails}    clientLocation    	location3
    Set To Dictionary    ${PhoneNumberGlobal}    clientAccount    GlobalUsers
    Set To Dictionary    ${PhoneNumberGlobal}    clientLocation    	location3
    Set To Dictionary    ${InvoiceDetails}    Location    	location3


    : FOR    ${key}    IN    @{InvoiceDetails.keys()}
    \    ${updated_val}=    Replace String    ${InvoiceDetails["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${InvoiceDetails}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup01}
    : FOR    ${key}    IN    @{Huntgroup01.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup01["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup01}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup02}
    : FOR    ${key}    IN    @{Huntgroup02.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup02["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup02}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup03}
    : FOR    ${key}    IN    @{Huntgroup03.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup03["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup03}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup04}
    : FOR    ${key}    IN    @{Huntgroup04.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup04["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup04}    ${key}    ${updated_val}

    Set suite variable    &{Huntgroup05}
    : FOR    ${key}    IN    @{Huntgroup05.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup05["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${Huntgroup05}    ${key}    ${updated_val}

    #Set suite variable    &{PartitionDetails}
    : FOR    ${key}    IN    @{PartitionDetails.keys()}
    \    ${updated_val}=    Replace String    ${PartitionDetails["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${PartitionDetails}    ${key}    ${updated_val}

    #Set suite variable    &{PhoneNumberDetails}
    : FOR    ${key}    IN    @{PhoneNumberDetails.keys()}
    \    ${updated_val}=    Replace String    ${PhoneNumberDetails["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PhoneNumberDetails}    ${key}    ${updated_val}
#    \    ${updated_val}=    Replace String    ${PhoneNumberDetails["${key}"]}    {rand_str}    ${uni_str}
#    \    Set To Dictionary    ${PhoneNumberDetails}    ${key}    ${updated_val}


     : FOR    ${key}    IN    @{PhoneNumberGlobal.keys()}
    # \    log to console  "==========keys==========="
     #\    log to console  ${PhoneNumberGlobal}
     \    ${updated_val}=    Replace String    ${PhoneNumberGlobal["${key}"]}    {rand_int}    ${uni_num}
     \    Set To Dictionary    ${PhoneNumberGlobal}    ${key}    ${updated_val}


    Set suite variable    &{DMUser}
    : FOR    ${key}    IN    @{DMUser.keys()}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${DMUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMUser}
    : FOR    ${key}    IN    @{LocPMUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${LocPMUser}    ${key}    ${updated_val}

    Set suite variable    &{AccPMUser}
    : FOR    ${key}    IN    @{AccPMUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMUser["${key}"]}    {rand_str}    ${uni_str}
    \    Set To Dictionary    ${AccPMUser}    ${key}    ${updated_val}
    ${usr_str}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    &{DMProfUser}
    : FOR    ${key}    IN    @{DMProfUser.keys()}
    \    ${updated_val}=    Replace String    ${DMProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${DMProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${DMProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${DMProfUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMProfUser}
    : FOR    ${key}    IN    @{LocPMProfUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${LocPMProfUser}    ${key}    ${updated_val}

    Set suite variable    &{AccPMProfUser}
    : FOR    ${key}    IN    @{AccPMProfUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${AccPMProfUser}    ${key}    ${updated_val}

    Set suite variable    &{BillingProfUser}
    : FOR    ${key}    IN    @{BillingProfUser.keys()}
    \    ${updated_val}=    Replace String    ${BillingProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${BillingProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${BillingProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${BillingProfUser}    ${key}    ${updated_val}

    Set suite variable    &{TechnicalProfUser}
    : FOR    ${key}    IN    @{TechnicalProfUser.keys()}
    \    ${updated_val}=    Replace String    ${TechnicalProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${TechnicalProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${TechnicalProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${TechnicalProfUser}    ${key}    ${updated_val}

    Set suite variable    &{EmergencyProfUser}
    : FOR    ${key}    IN    @{EmergencyProfUser.keys()}
    \    ${updated_val}=    Replace String    ${EmergencyProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${EmergencyProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${EmergencyProfUser["${key}"]}    {rand_str}    ${usr_str}
    \    Set To Dictionary    ${EmergencyProfUser}    ${key}    ${updated_val}
    ${usr_str2}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    &{LocPMProfPMUser}
    : FOR    ${key}    IN    @{LocPMProfPMUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMProfPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMProfPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMProfPMUser["${key}"]}    {rand_str}    ${usr_str2}
    \    Set To Dictionary    ${LocPMProfPMUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMProfBillingUser}
    : FOR    ${key}    IN    @{LocPMProfBillingUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMProfBillingUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMProfBillingUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMProfBillingUser["${key}"]}    {rand_str}    ${usr_str2}
    \    Set To Dictionary    ${LocPMProfBillingUser}    ${key}    ${updated_val}

    Set suite variable    &{LocPMProfTechnicalUser}
    : FOR    ${key}    IN    @{LocPMProfTechnicalUser.keys()}
    \    ${updated_val}=    Replace String    ${LocPMProfTechnicalUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${LocPMProfTechnicalUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${LocPMProfTechnicalUser["${key}"]}    {rand_str}    ${usr_str2}
    \    Set To Dictionary    ${LocPMProfTechnicalUser}    ${key}    ${updated_val}
    ${usr_str3}=    Generate Random String    4    [LETTERS][NUMBERS]

    Set suite variable    &{AccPMProfPMUser}
    : FOR    ${key}    IN    @{AccPMProfPMUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMProfPMUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMProfPMUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMProfPMUser["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${AccPMProfPMUser}    ${key}    ${updated_val}

    Set suite variable    &{AccPMProfBillingProfUser}
    : FOR    ${key}    IN    @{AccPMProfBillingProfUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMProfBillingProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMProfBillingProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMProfBillingProfUser["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${AccPMProfBillingProfUser}    ${key}    ${updated_val}

    Set suite variable    &{AccPMProfTechnicalProfUser}
    : FOR    ${key}    IN    @{AccPMProfTechnicalProfUser.keys()}
    \    ${updated_val}=    Replace String    ${AccPMProfTechnicalProfUser["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AccPMProfTechnicalProfUser}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${AccPMProfTechnicalProfUser["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${AccPMProfTechnicalProfUser}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{geolocationDetails.keys()}
    \    ${updated_val}=    Replace String    ${geolocationDetails["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${geolocationDetails}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${geolocationDetails["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${geolocationDetails}    ${key}    ${updated_val}

    : FOR    ${key}    IN    @{geolocation_close.keys()}
    \    ${updated_val}=    Replace String    ${geolocation_close["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${geolocation_close}    ${key}    ${updated_val}
    \    ${updated_val}=    Replace String    ${geolocation_close["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${geolocation_close}    ${key}    ${updated_val}

    Set suite variable    &{Invoice02}
    : FOR    ${key}    IN    @{Invoice02.keys()}
    \    ${updated_val}=    Replace String    ${Invoice02["${key}"]}    {rand_str}    ${usr_str3}
    \    Set To Dictionary    ${Invoice02}    ${key}    ${updated_val}
    ${rand_num}=    Generate Random String    4    12345678

    Set suite variable    &{Huntgroup03}
    : FOR    ${key}    IN    @{Huntgroup03.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup03["${key}"]}    {rand_int}    ${rand_num}
    \    Set To Dictionary    ${Huntgroup03}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{Huntgroup08}
    : FOR    ${key}    IN    @{Huntgroup08.keys()}
    \    ${updated_val}=    Replace String    ${Huntgroup08["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${Huntgroup08}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{AA_02}
    : FOR    ${key}    IN    @{AA_02.keys()}
    \    ${updated_val}=    Replace String    ${AA_02["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_02}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{AA_04}
    : FOR    ${key}    IN    @{AA_04.keys()}
    \    ${updated_val}=    Replace String    ${AA_04["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_04}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{AA_07}
    : FOR    ${key}    IN    @{AA_07.keys()}
    \    ${updated_val}=    Replace String    ${AA_07["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_07}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{AA_09}
    : FOR    ${key}    IN    @{AA_09.keys()}
    \    ${updated_val}=    Replace String    ${AA_09["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${AA_09}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{PG_03}
    : FOR    ${key}    IN    @{PG_03.keys()}
    \    ${updated_val}=    Replace String    ${PG_03["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PG_03}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{PG_04}
    : FOR    ${key}    IN    @{PG_04.keys()}
    \    ${updated_val}=    Replace String    ${PG_04["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PG_04}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{PG_07}
    : FOR    ${key}    IN    @{PG_07.keys()}
    \    ${updated_val}=    Replace String    ${PG_07["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PG_07}    ${key}    ${updated_val}

    ${uni_num}=    Generate Random String    4    12345678
    Set suite variable    &{PG_08}
    : FOR    ${key}    IN    @{PG_08.keys()}
    \    ${updated_val}=    Replace String    ${PG_08["${key}"]}    {rand_int}    ${uni_num}
    \    Set To Dictionary    ${PG_08}    ${key}    ${updated_val}
