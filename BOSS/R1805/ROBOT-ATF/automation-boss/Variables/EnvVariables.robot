*** Variables ***
#BOSS PORTAL INFO
${URL}                    http://10.197.145.190/
#${URL}                    http://10.198.107.94/
#${URL}                    http://10.32.131.11/


${bossUsername}           staff@shoretel.com
${bossPassword}           Abc123!!
#${bossPassword}           Abc123!!
#${bossPassword}           Abc123!!

${bossUser}               Staff User
${bossCluster1}           BOSS QA
${bossCluster}            BAU
${platform}               COSMO
${BROWSER}                chrome
${AutomationNew}          Automation New

${SCOCosmoAccount}        VCFE_BCA_automation
#${SCOCosmoAccount}        Reg_Automation
#${SCOCosmoAccount}        1801 Regression

${country}                US
#${country}                Australia
#${country}                UK

${locationName}           Boss_auto_location
#${locationName}           Test Location
#${locationName}           Location1

${AccWithoutLogin}        --> Switch account without logging in as someone else

#US
${request_by}             Auto User2
${user_extn}              5083
${user2_extn}             5084
${extnlistname}           Boss_ExtnList_01

#AUS
#${request_by}             dm user
#${user_extn}              4826
#${extnlistname}           Extension_List_1

#UK
#${request_by}             dm user
#${user_extn}              2508
#${extnlistname}           Boss_ Extension_List_01

#Account Detail:
${accountName1}           VCFE_BCA_automation
#${accountName1}           Reg_Automation
#${accountName1}           1801 Regression

#US
${DMemail}                a2user2dm@mitel.com
${DMpassword}             Abc123!!
${PMemail}                a3user3pm@mitel.com
${PMpassword}             Abc123!!

${PMUser}                 Auto User3
#AUS
#${DMemail}                dm@auto.com
#${DMpassword}             Test123!!
#${PMemail}                pm@2auto.com
#${PMpassword}             Test123!!

#UK
#${DMemail}                dm@automation.com
#${DMpassword}             Test123!!
#${PMemail}                priya@sco.com
#${PMpassword}             Test123!!

#D2 Portal details US
${D2IP}                   10.197.145.186
${D2User}                 admin@auto.com
${D2Password}             Shoreadmin1#

#D2 Portal details AUS
#${D2IP}                   10.198.107.93
#${D2User}                 suser01@shoretel.com
#${D2Password}             ShoreTel1$

#D2 Portal details UK
#${D2IP}                   10.32.131.50
#${D2User}                 vsabusam@mac.shoretel.com
#${D2Password}             Shoretel1$##not working

#User login details US
&{phoneDMUser01}    user_email=a2user2dm@mitel.com    password=Abc123!!
&{phonePMUser01}    user_email=a3user3pm@mitel.com   password=Abc123!!

#User login details AUS
#&{phoneDMUser01}    user_email=dm@auto.com    password=Test123!!
#&{phonePMUser01}    user_email=pm@2auto.com    password=Test123!!

#User login details UK
#&{phoneDMUser01}    user_email=dm@automation.com    password=Test123!!
#&{phonePMUser01}    user_email=priya@sco.com    password=Test123!!

&{LNP_service}      requestedBy=boss automation     source=Email    serviceClass=projectmgt     index=12            #Index is the index number of LNP service


#AOB Related Variables

# AOB Login Variables
${AOBAccount}     AOB_Contract_Reg
${AOBemail}       cont_aob@shoretel.com
${AOBUsername}    AOB contract

${salesforceUserName}     sasingh
${salesforcePassword}     Nov@1234

&{AOB_login_dic}       url=${URL}    bossusername=${bossUsername}     bosspassword=${bossPassword}   AOBaccountName=${AOBAccount}    AccWithoutLogin=${AccWithoutLogin}   page=aob

# Profile Grid Variables
${ProfileGridAccount}   Automation One
${ProfileGridLocation}   Automation One

#${ProfileGridRequestedBy}   One User1
#${ProfileGridRequestedSource}   2

${TC_195498_Acoount}        AutoTest_Acc_kmDag0Ko
${TC_195498_User}           autotestdm7uHJ Auto

${TC_195634_Acoount}        AutoTest_Acc_l4RYdNE7
${TC_195634_User}           autotestdmtBt5 Auto

#Okba
${newacc}   Automation One