"""Module for BOSS portal functionalities
   Author: Kenash Kanakaraj
"""
import os
import sys
import time

import stafenv

#from base import LocalBrowser
#import web_wrappers.selenium_wrappers as base
from web_wrappers.selenium_wrappers import LocalBrowser
from page.BOSSComponent import BossPage
from mapMgr import mapMgr

#BOSS feature component files
from AOBComponent import AOBComponent as aob
from VCFEComponent import VCFEComponent as vcfe
from BcaComponent import BcaComponent as Bca
from ECCComponent import ECCComponent as ecc
from UserComponent import UserComponent as user
from ServiceComponent import ServiceComponent as service

_DEFAULT_TIMEOUT = 3

class BossComponent( aob, vcfe, Bca, ecc, user, service):
    ''' BOSS Component Interface to interact with the ROBOT keywords
    '''

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, **params):

        self.browsertype = params.get('browser', 'chrome').lower()
        self.location = params.get('country', 'US').lower()
        self._browser = LocalBrowser(self.browsertype)
        browser_obj = self._browser.get_current_browser()
        browser_obj.maximize_window()
        self._browser.location = self.location
        self.boss_page = BossPage(self._browser)
        mapMgr.create_maplist("BossComponent")
        self.mapDict = mapMgr.getMapDict()

    def open_url(self,url):
        """
        `Description:` This function is used to open BOSS portal page

        `:param1` url: URL of boss page

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.open_url(url)
        except Exception,e:
            print(e)

    def reset_password_from_home_page(self,email):
        """
        `Description:` This Function will try to reset password from Home page. By Sending link to Email

        `:param1` email: Email address

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.reset_password_from_home_page(email)
            #return current_time
        except:
            raise AssertionError("Reset password Va email has failed")

    def switch_page_switch_account(self):
        """
        `Description:` This Function will switch to account page.

        `:param1` None

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.switch_page_switch_account()
        except:
            raise AssertionError("Failed to Switch Account")

    def client_login(self, **params):
        """
        `Description:` Login to the BOSS portal using the username and password

        `:param1` username: URL

        `:param2` username: User email address

        `:param3` password: user password

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.open_url(params["URL"])

            self.boss_page.commonfunctionality.client_login(params["username"],
                                                            params["password"])
            print("DEBUG: Login successful")
        except:
            raise AssertionError("Login Failed!!")

    def switch_page(self, **params):
        """
        `Description:` Switch page using the account link on the top of the page

        `:param` params: name of the page which need to be switch

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            print("IN MAIN:")
            if params.keys():
                self.boss_page.commonfunctionality.switch_page(page=params['page'])
            else:
                print("Please check that the input parameters have been provided",
                        self.switch_page.__doc__)
        except:
            raise AssertionError("Page Switch Failed!!")

    def verify_page(self, **params):
        """
        `Description:` Verify if the expected string is available on the page

        `:param1` page- Page identifier

        `:param2` exp_content- Text in the identifier

        `:return:` status - True if comtent is found on the page else False

        `Created by:` Kenash K
        """
        try:
            time.sleep(_DEFAULT_TIMEOUT)
            status = False
            if params.keys():
                status = self.boss_page.commonfunctionality.verify_text(params["page"],
                                                                        params["exp_content"])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_page.__doc__)
            return status
        except:
            raise AssertionError("Page Verification Failed!!")

    def verify_user(self, **params):
        '''
        `Description:` Verify that the user is available in the user table

        `:param1` Business Email

        `:param2` Role

        `:return:` status - True if user is found on the page else False

        `Created by:` Kenash K
        '''
        try:

            status = False
            if params.keys():
                status = self.boss_page.user_handler.verify_user(params["au_businessmail"],
                                                                 params["role"])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_user.__doc__)
            return status
        except:
            raise AssertionError("User verification Failed!!")

    def verify_contract_state(self, **params):
        '''
        `Description:` Verify the contract state

        `Param1:` params: accountName: Name of account

        `Param2:` params: exp_state: State of account

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.account_handler.verify_contract_state(
                    params["account_name"], params["exp_state"])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_contract_state.__doc__)
            return status
        except:
            raise AssertionError("Contarct state verification Failed!!")

    def switch_link_in_partition(self, **params):
        '''
        `Description:` This function will switch partition link

        `Param1:` Partition Name

        `Param2:` Link to Switch

        `Returns:` None

        `Created by:` rdoshi
        '''
        try:
            print("Switch to link in partition")
            if params.keys():
                self.boss_page.commonfunctionality.switch_link_in_partition(params['switch_link'],
                                                                            params['partition'])
            else:
                print("Switch failed")
        except:
            raise AssertionError("Switch to link partition failed!!")

    def switch_account(self, **params):
        """
        `Description:` Switch account using the account link on the top of the page

        `Param:` params: Dictionary with account information

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.commonfunctionality.switch_account(params['newacc'], params['seloption'])
            else:
                print("Please check that the input parameters have been provided",
                        self.switch_account.__doc__)
        except:
            raise AssertionError("Switch Account Failed!!")

    def add_contract(self, **params):
        '''
        `Description:` This Function will create contact

        `Param:` params: Dictionary with contract information

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.account_handler.add_contract(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_contract.__doc__)
                status = False
            return status
        except:
            raise AssertionError("Add contract Failed!!")

    def add_phonenumber(self, **params):
        '''
        `Description:` This function will add phone numbers to BOSS portal

        `Param:` params: Dictionary with phone number information

        `Returns:` None

        `Created by:` Vasuja K

        `Modified by :` Kenash K
        '''
        try:
            if params.keys():
                self.boss_page.phone_number.add_phonenumber(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_phonenumber.__doc__)
        except:
            raise AssertionError("Add Phone number Failed!!")

    def add_user(self, **params):
        '''
        `Description:` This Function will create user in portal

        `Param:` params: Dictionary with user information

        `Returns:` phone_num, extn

        `Created by:` Kenash K
        '''
        try:
            if params.keys():
                phone_num, extn=self.boss_page.user_handler.add_user(params)
                return phone_num, extn
            else:
                print("Please check that the input parameters have been provided",
                        self.add_user.__doc__)
        except:
            raise AssertionError("Add user Failed!!")

    def update_phonestate(self, **params):
        '''
        `Description:` This Function will update phone state to available

        `Param:` params: Dict with phone information

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            if params.keys():
                self.boss_page.phone_number.update_phonenumbers(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_phonenumber.__doc__)
        except:
            raise AssertionError("update phone state Failed!!")

    def verify_phone_state(self, **params):
        '''
        `Description:` This function will verify phone update

        `Param:` params: Dictionary with phone state

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.phone_number.verify_phonenumbers(params)
                return status
            else:
                print("Please check that the input parameters have been provided",
                        self.add_phonenumber.__doc__)
        except:
            raise AssertionError("verify phone state Failed!!")

    def set_location_as_site(self):
        '''
        `Description:` This function will set the location as Site

        `Param:` None

        `Returns:` None

        `Created by:` Vasuja K
        '''
        try:
            self.boss_page.account_handler.set_location_as_site()

        except:
            print("Please check that the input parameters have been provided",
                    self.set_location_as_site.__doc__)
            raise AssertionError("Set location as site Failed!!")

    def click_link_in_grid(self, **params):
        '''
        `Description:` This function will click link in GRID

        `Param1:` Grid ID

        `Param2:` Link

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            self.boss_page.commonfunctionality.click_link_in_grid(params['grid'], params['link'])
        except:
            print("Could not access link", self.click_link_in_grid.__doc__)
            raise AssertionError("Click operation Failed!!")

    def add_instance(self, **params):
        '''
        `Description:` This Function will add instance

        `Param1:` Instance Name

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            self.boss_page.account_handler.add_instance(params['instance_name'])
        except:
            print("Could not access link", self.add_instance.__doc__)
            raise AssertionError("Add instance Failed!!")

    def confirm_contract(self, **params):
        '''
        `Description:` This function will confirm contract.

        `Param:` params: Instance Name , Location

        `Returns:` order_number

        `Created by:` Kenash K
        '''
        try:
            order_number = self.boss_page.account_handler.confirm_contract(params['instance'], params['location'])
            return order_number
        except:
            print("Could not access link", self.confirm_contract.__doc__)
            raise AssertionError("Confirm contract Failed!!")

    def select_option(self, **params):
        '''
        `Description:` Select perticular option

        `Param1:` Option

        `Param2:` Element

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            self.boss_page.commonfunctionality.select_option(params['option'], params['element'])
        except:
            print("Could not access link", self.select_option.__doc__)
            raise AssertionError("Selection Failed!!")

    def add_partition(self, **params):
        '''
        `Description:` add a primary partition to a newly created account

        `Param:` params: Dictionary contains partition info

        `Returns:` None

        `Created by:` rdoshi
        '''
        try:
            if params.keys():
                self.boss_page.add_partition.add_partition(params)
                #verifying the created partition

            else:
                print("Please check if input params have been provided")
        except:
            raise AssertionError("Add partition Failed!!")

    def verify_partition(self, **params):
        '''
        `Description:` This Function will verify the partition has been created or not

        `Param:` params: Dictionary contains partition info

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        '''
        try:
            if params.keys():
                status = self.boss_page.add_partition.verify_partition(params["partitionName"])
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_partition.__doc__)
            return status
        except:
            raise AssertionError("Verify parition Failed!!")

    def enter_contact_name(self, **params):
        """
        `Description:` This function will enter contract name

        `Param1:` contact_name

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.commonfunctionality.search_user(params['contact_name'])
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Enter contact name Failed!!")

    def verify_grid_value(self, **params):
        """
        `Description:` This function will verify the grid value.

        `Param1:` gridvalue: values of grid

        `Returns:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status = False
            if params.keys():
                status = self.boss_page.commonfunctionality.verify_grid_value(
                    params['gridvalue'])
            else:
                print("Please check that the input parameters have been provided")
            return status
        except:
            raise AssertionError("Grid verification Failed!!")


    def move_to_tab(self, **params):
        """
        `Description:` This function will help to switch to tabs

        `Param1:` tab_name

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.commonfunctionality.move_to_tab(params['tab_name'])
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Move to tab Failed!!")

    def verify_tabs_exist(self, *params):
        """
        `Description:` This function will verify the tab is exist or not

        `Param1:` tab_list: list of all tabs

        `Returns:` True or False

        `Created by:` Kenash K
        """
        try:
            status = False
            if len(params):
                status = self.boss_page.commonfunctionality.verify_tabs(params)
            else:
                print("Please check that the input parameters have been provided")
            return status
        except:
            raise AssertionError("Verification tab Failed!!")

    def verify_loc_status(self, **params):
        '''
       `Description:` This function will verify Emergency registration status of location

        `Param1:` Loc_name

        `Param2:` exp_state

        `Returns:` status - True/False

        `Created by:` Vasuja
        '''
        try:
            result=self.boss_page.VCFE_Handler.verify_loc_status(params)
            return result

        except:
            print("Please check that the input parameters have been provided",
                    self.verify_loc_status.__doc__)
            raise AssertionError("Location status verification Failed!!")

    def create_invoice_group(self, **params):
        '''
        `Description:` This function will create the invoice group.

        `Param:` params: Dictionary contains  invoice group Info

        `Returns:` None

        `Created by:` Vasuja
        '''
        try:
            self.boss_page.Invoices_Payments.create_invoice_group(params)
        except:
            print("Please check that the input parameters have been provided",
                    self.create_invoice_group.__doc__)
            raise AssertionError("Invoice group creation Failed!!")

    def verify_invoice_group_location(self, **params):
        '''
        `Description:` To verify the invoice group location is being created

        `Param:` Location to verify

        `Returns:` None

        `Created by:` Vasuja
        '''
        try:
            status = self.boss_page.Invoices_Payments.verify_invoice_group_location(params)
            return status
        except:
            print("Please check that the input parameters have been provided",
                    self.verify_invoice_group_location.__doc__)
            e.args += ("Please check that the input parameters have been provided",)
            raise

    def verify_user_profile(self, **params):
        '''
        `Description:` this function verify user profile

        `Param:` params:  Dictionary contains phone information

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            if params.keys():
                status = self.boss_page.user_handler.verify_user_profile(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.verify_user_profile.__doc__)
            return status
        except:
            raise AssertionError("verification user profile Failed!!")

    def accept_agreement(self):
        """
        `Description:` This function will accept agreement.

        `Param:` None

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.accept_agreement()

        except:
            print("Could not accept agreement")
            raise AssertionError("Accept agreement Failed!!")

    def stop_impersonating(self):
        """
        `Description:` To stop impersonatingthe for current user

        `:return:` None

        `Created by:` Guo Zheng
        """
        try:
            self.boss_page.commonfunctionality.stop_impersonating()
        except:
            raise AssertionError("Stop Impersonating Failed!!")

    def log_off(self):
        """
        `Description:` This function will perform log off operation

        `Param:` None

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.log_off()
        except:
            raise AssertionError("Log Off Failed!!")

    def right_click(self, name):
        """
        `Description:` perform right click operation on elments and redirect to change password field

        `:param` name: First Name last Name

        `:return:` None

        `Created by:` Saurabh Singh
        """
        try:
            
            self.boss_page.commonfunctionality.right_click(name)
        except Exception,e:
            print(e)
            raise AssertionError("Right click failed !!")


    def change_profile_password_from_user_page(self,name):
        """
        `Description:` redirect user to change password setting page from inside user detail page

        `:param` name: First Name last Name

        `:return:` result - True/False

        `Created by:` Saurabh Singh
        """
        try:
            result = self.boss_page.commonfunctionality.change_profile_password_from_user_page(name)
            return result
        except Exception,e:
            print("Reached Exception"+e)
            raise

    def get_build(self):
        """
        `Description:` This function will get the build of BOSS portal

        `:param` None

        `:return:` None

        `Created by:` Saurabh Singh
        """
        self.boss_page.commonfunctionality.get_build()


    def close_user(self,**params):
        """
        `Description:` This Test case will close the User from the page with and without phone number user

        `:param` email: email of user who is going to close

        `:param` name: name of requester

        `:return:` result - True/False

        `Created by:` Saurabh Singh
        `Modified by:` Megha Bansal
        """
        try:
            #print("From Boss: "+email)
            result = self.boss_page.commonfunctionality.close_user(params)
            return result
            #print("Validation of result"+str(result))
        except Exception,e:
            print(e)
            return False

    def change_password(self, **params):
        """
        `Description:`  This function will change the password

        `:param1` new_password: new password which need to be set

        `:param2` old_pwd: old password of user

        `:param` options:

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            old_pass = params.get('oldpassword', '')
            self.boss_page.commonfunctionality.change_password(params["newpassword"],
                                                               old_pass)

        except:
            print("Could not accept agreement")
            raise AssertionError("Change password Failed!!")

    def update_password(self, **params):
        """
        `Description:`  This function will update the password

        `:param1` new_password: new password which need to be set

        `:param2` old_pwd: old password of user

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            old_pass = params.get('oldpassword', '')
            self.boss_page.commonfunctionality.update_password(params["newpassword"],
                                                               params["oldpassword"])

        except:
            raise AssertionError("Update password failed Failed!!")

    def close_the_browser(self, **params):
        """
        `Description:` Close the browser object

        `:param` driver: WebDriver object

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            time.sleep(2)
            self.boss_page.commonfunctionality.close_browser()
        except:
            raise AssertionError("Close browser Failed!!")

    def add_prog_button(self, **params):
        """
        `Description:` For adding program buttons

        `:param` params:  Dictionary contains programmable button information

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            if params.keys():
                self.boss_page.prog_button_handler.add_programmable_buttons(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.add_programmable_buttons.__doc__)
        except:
            raise AssertionError("Add programable button Failed!!")

    def close_open_order(self, Location):
        """
        `Description:` Close open order which create at the time of geo location created

        `:param1:` Location name

        `:return:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status= self.boss_page.commonfunctionality.close_open_order(Location)
            return status
        except Exception,e:
            print e
            raise AssertionError("Closing Order Failed!!")

    def close_location(self, Location, name):
        """
        `Description:` Close the Geo location

        `:param1:` Location name

        `:param2:` requester name

        `:return:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status=self.boss_page.commonfunctionality.close_location(Location, name)
            return status
        except Exception,e:
            print e
            raise AssertionError("Closing Location Failed!!")

    def reset_password_via_email(self, **params):
        """
        `Description:` reset password from email

        `:param` user_email: whom password will be reset

        `:param` emailPassword: email password

        `:param` emailServer: email server

        `:param` setPassword: what password need to be set

        `:return:` status

        `Created by:` Saurabh Singh
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            status=self.boss_page.commonfunctionality.reset_password_via_email(params["emailToReset"], params["emailPassword"],params["emailServer"],params["setPassword"])
            return status
        except Exception, e:
            print(e)
            raise AssertionError("Password Reset via email Failed!!")

    def check_email(self,FROM_EMAIL,fromAdd):
        """
        `Description:` check the email time of latest email

        `:param` fromAdd: sender name

        `:param` user_email: user email

        `:param` emailPassword: email password

        `:param` emailServer: email server

        `:return:` None

        `Created by:` Saurabh Singh
        """
        try:
            self.boss_page.commonfunctionality.check_email(FROM_EMAIL, fromAdd)
        except Exception,e:
            print e
            raise AssertionError("Email Check has been Failed!!")

    def modify_service_status(self, **params):
        """
        `Description:` Modify the service status

        `:param:` params:Dictionary of service  information

        `:return:` None

        `Created by:` rdoshi
        """
        try:
            if params.keys():
               self.boss_page.account_handler.modify_service_status(params)
            else:
                print("Please check that the input parameters have been provided",
                        self.modify_service_status.__doc__)
        except:
            raise AssertionError("modification of servic status Failed!!")

    def check_alert(self):
        """
        `Description:` Check for alert pop up on page

        `:return:`

        `Created by`  Saurabh Singh
        """
        try:
            self.boss_page.commonfunctionality.check_alert()
        except Exception, e:
            print e

    def switch_page_personal_information(self):
        """
        `Description:` switch to personal information page

        `:param:` None

        `:return:` result - True/False

        `Created by:` Kenash K
        """
        try:
            result = self.boss_page.commonfunctionality.switch_page_personal_information()
            return result
        except Exception,e:
            print e
            raise AssertionError("Switch is  Failed!!")

    def switch_page_primary_partition(self):

        try:
            result = self.boss_page.commonfunctionality.switch_page_primary_partition()
            return result
        except Exception,e:
            print(e)
            raise AssertionError("Page partitionswitch failed!!")

    def delete_contract(self,params):

        '''
        `Description:` To delete contract.

        `:param1:` Name of contract to delete

        `:return:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            if params:
                    status=self.boss_page.account_handler.delete_contract(params)
                    time.sleep(2)
                    return status
                    #self.action_ele.explicit_wait("cp_allContractsbtnRefresh")
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Delete Contract Failed!!")


    def verify_contract_delete(self,param):
        """
        `Description:` verify the contract is deleted

        `:param:` Dictionary of contract information

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            if param:
                status = self.boss_page.account_handler.verify_delete_contract(param)
                return status
            else:
                print("Please check that the input parameters have been provided")
        except:
            raise AssertionError("Verifcation of Delete contract Failed!!")


    def check_for_error(self):
        """
        `Description:` To check for errors in phone number page

        `:param:` None

        `:return:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status = self.boss_page.commonfunctionality.check_for_error()
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def add_transfer_request(self, **params):
        """
        `Description:` To add number transfer equest

        `:param` params:

        `:return: status - True/False

        `Created by:` Saurabh Singh
        """
        try:
            status = self.boss_page.commonfunctionality.add_transfer_request(**params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def verify_transfer_request(self,params):
        """
        `Description:` TO verify transfer request

        `:param` params:

        `:return:` status - True/False

         `Created by:` Kenash K
        """
        try:
            status = self.boss_page.commonfunctionality.verify_transfer_request(params)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def add_LNP_service(self,**params):
        """
        `Description:` To add LNP request

        `:param` prams:

        `:return:` order_id

         `Created by:` Saurabh Singh
        """
        try:
            order_id = self.boss_page.commonfunctionality.add_LNP_service(**params)
            return order_id
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def activate_service(self, order_id, phone):
        '''
        `Description:` To activate service

        `Param1:` order_id

        `Param2:` phone

        `Returns:` status - True/False

        `Created by:` rdoshi
        '''
        try:
            status = self.boss_page.commonfunctionality.activate_service(order_id, phone)
            return status
        except:
            raise AssertionError("Error Found on page, Test Case Failed!!")

    def click_cancel(self):
        """
        `Description:` This function will click on Ok button if it is present and then click on Cancel button.

        `Param:`  None

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.boss_page.commonfunctionality.click_cancel()

        except:
            print("Could not click on Cancel button")
            raise AssertionError("Click on cancel Failed!!")

    def go_to_vcfe_page(self, params):
        """
            `Description:` This function will help to go and land in a given vcfe page

            `Param:`  params: page name

            `Created by:` Immani Mahesh kumar
        """
        try:
            self.boss_page.VCFE_Handler.go_to_vcfe_page(params)

        except:
            print("switching to vcfe page has failed", self.go_to_vcfe_page.__doc__)

    def add_usergroup(self, **params):
        '''

        :param params:
        :return:
        '''
        if params.keys():
            self.boss_page.user_handler.add_usergroup(params)
        else:
            print("Please check that the input parameters have been provided")

    def assign_usergroup(self, **params):
        '''

        :param params:
        :return:
        '''
        if params.keys():
            self.boss_page.user_handler.assign_usergroup(params)
        else:
            print("Please check that the input parameters have been provided")

    def delete_usergroup(self, params):
        '''

        :param params:
        :return:
        '''
        try:
            status = self.boss_page.user_handler.delete_usergroup(params)
            return status
        except:
            raise AssertionError("Error occured, could not delete user group!!")

    def add_on_hold_music(self, **params):
        '''
        `Description:` Add 'on hold music' from Phone system

        `Param:` params: Dictionary contains on_hold_music Info

        `Returns:` None

        `Created by:` Vasuja
        '''
        try:
            self.boss_page.OH_music.add_on_hold_music(params)
        except:
            print("Please check that the input parameters have been provided",
                  self.add_on_hold_music.__doc__)
            raise AssertionError("Adding On Hold Music Failed!!")

    def click_on_manage_button(self, **params):
        '''
        `Description:` This Function will click on manage button of specified feature

        `Param:`  feature name

        `Returns:` None

        `Created by:` Megha Bansal
        '''
        try:
            self.boss_page.commonfunctionality.click_on_manage_button(feature=params["feature"])
            print("Okba BossComponent.py",params["feature"])
            print(params["feature"])
        except:
            print("Could not access link", self.click_on_manage_button.__doc__)
            raise AssertionError("Click on Manage button failed!!")

    def add_globaluser_mobility(self, **params):
        '''
        `Description:` This Function will add global user to mobility via add on features page
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.addonfeature.add_globaluser_mobility(params)
            return result
        except:
            print("Could not access link", self.add_globaluser_mobility.__doc__)
            raise AssertionError("Add Global User to mobility failed!!")

    def add_mobility_profile(self, **params):
        '''
        `Description:` This Function will add mobility profile for a global user via personal information page
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.personal_information.add_mobility_profile(params)
            return result
        except:
            print("Could not access link", self.add_mobility_profile.__doc__)
            raise AssertionError("Add Global User to mobility failed!!")

    def verify_mobility_checkbox(self, **params):
        '''
        `Description:` This Function will verify mobility checkbox for a global user if there is smr instance setup for selected country
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.user_handler.verify_mobility_checkbox(params)
            return result
        except:
            print("Could not access link", self.verify_mobility_checkbox.__doc__)
            raise AssertionError("Verify mobility checkbox present failed!!")

    def verify_turnup_service(self, **params):
        '''
                `Description:` This Function will verify Global User Number Service
                `Param:` params
                `Returns: ` result - True/False
                `Created by:` Megha Bansal
                '''
        try:
            result = self.boss_page.phone_number.verify_turnup_service(params)
            return result
        except:
            print("Could not access link", self.verify_turnup_service.__doc__)
            raise AssertionError("Verify Global User Number Service failed!!")

    def verify_swap_globaluser(self, **params):
        '''
        `Description:` This Function will verify swap option for global user is disabled or not
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.user_handler.verify_swap_globaluser(params)
            return result
        except:
            print("Could not access link", self.verify_swap_globaluser.__doc__)
            raise AssertionError("Verify swap for GlobalUser failed!!")

    def verify_provisioning_details(self, **params):
        '''
        `Description:` This Function will verify provisioning details of selected service
        `Param:` params
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.service.verify_provisioning_details(params)
            return result
        except:
            print("Could not access link", self.verify_provisioning_details.__doc__)
            raise AssertionError("Verify provisioning details of global user tn service failed!!")

    def create_DNIS_with_Save(self, **params):
        """
        To create DNIS in phone numbers  page

        :param params: Variable contains phone information

        :return: Status- True or false

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result, selectedTn, selectedDestType = self.boss_page.phone_number.create_DNIS_with_Save(params)
                return result, selectedTn, selectedDestType
            else:
                print("Please check that the input parameters have been provided",
                      self.create_DNIS_with_Save.__doc__)
        except:
            raise AssertionError("Create DNIS Failed!!")

    def create_DNIS_with_Cancel(self, **params):
        """
        To set information to create DNIS with cancel in phone numbers  page

        :param params: Variable contains phone information

        :return: Status- True or false

        `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.create_DNIS_with_Cancel(params)
                return result
            else:
                print("Please check that the input parameters have been provided",
                      self.create_DNIS_with_Cancel.__doc__)
        except:
            raise AssertionError("Create DNIS with cancel failed")

    def select_number_for_Edit(self, **params):
        """
         To select a number for edit in phone numbers  page

         :param params: Variable contains phone information

         :return: None

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                self.boss_page.phone_number.select_number_for_Edit(params)

            else:
                print("Please check that the input parameters have been provided",
                      self.select_number_for_Edit.__doc__)
        except:
            raise AssertionError("Selecting Number Failed!!")

    def verify_PhoneNumber_Operation(self, **params):
        """
         To verify assign window in phone numbers  page

         :param params: Variable contains phone information

         :return: Status- True or false

          `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.verify_PhoneNumber_Operation(params)
                return result

            else:
                print("Please check that the input parameters have been provided",
                      self.verify_PhoneNumber_Operation.__doc__)
        except:
            raise AssertionError("Verification failed!!")

    def verify_PhoneNumber_Operation_for_Edit(self, **params):
        """
        To verify edit window in phone numbers  page

         :param params: Variable contains phone information

         :return: Status- True or false

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.verify_PhoneNumber_Operation_for_Edit(params)
                return result

            else:
                print("Please check that the input parameters have been provided",
                      self.verify_PhoneNumber_Operation_for_Edit.__doc__)
        except:
            raise AssertionError("Verification failed!!")

    def verify_findme(self, option):
        return self.boss_page.commonfunctionality.verify_findme(option)

    def block_here(self):
        print('blocking')

    def config_phone_numbers_callrouting(self, label, phone, num):
        try:
            self.boss_page.commonfunctionality.config_phone_numbers_callrouting(label, phone, num)
        except:
            raise AssertionError("config_phone_numbers_callrouting")

    def config_sim_ring(self, label, num):
        try:
            self.boss_page.commonfunctionality.config_sim_ring(label, num)
        except:
            raise AssertionError("config_phone_sim_ring")

    def config_find_me(self, label, num):
        try:
            self.boss_page.commonfunctionality.config_find_me(label, num)
        except:
            raise AssertionError("config_phone_find_me")

    def refresh_grid(self):
        """
         To refresh grid in phone numbers  page

         :param params: None

         :return: None

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            self.boss_page.phone_number.refresh_grid()
        except:
            raise AssertionError("Refresh failed!")

    def verify_destination_type(self, selectedTn, **params):
        """
        To verify Destination type of DNIS created in phone numbers  page

        :param params: Variable contains phone information , selectedTn

        :return: Status- True or false

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.verify_destination_type(selectedTn, params)
                return result
            else:
                print("Please check that the input parameters have been provided",
                      self.verify_destination_type.__doc__)
        except:
            raise AssertionError("Verify Destination Failed!")

    def verify_destination_and_status(self, selectedTn, selectedDestType, **params):
        """
         To verify Destination name and status of the created DNIS in phone numbers  page

         :param params: Variable contains phone information

         :return: Status- True or false

         `Created by:` Megha ,Tantri Tanisha
        """
        try:
            if params.keys():
                result = self.boss_page.phone_number.verify_destination_and_status(selectedTn, selectedDestType, params)
                return result
            else:
                print("Please check that the input parameters have been provided",
                      self.verify_destination_and_status.__doc__)
        except:
            raise AssertionError("Verify Destination and Status Failed!")

    def verify_tn_status(self, serviceTn, **params):
        """
         Description : To verify the status of Tn

         :param params: Variable contains phone information

         :return: Status- True or false

         `Created by:` Megha Bansal
        """
        try:
            #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if params.keys():
                result = self.boss_page.phone_number.verify_tn_status(serviceTn,  params)
                return result
            else:
                print("Please check that the input parameters have been provided",
                      self.verify_tn_status.__doc__)
        except:
            raise AssertionError("Verify Tn Status Failed!")


    def verify_available_tns(self, params):
        """
        Description : To verify the availability of Tns of the country List

        :param: Variable contains List of country

        :return: Status- True or false

        `Created by:` Megha Bansal
        """
        try:
            result = self.boss_page.phone_number.verify_available_tns(params)
            return result
        except:
            print("Could not access link", self.verify_available_tns.__doc__)
            raise AssertionError("Verify user location dropdown failed!!")

    def add_user_profile(self, **params):
        try:
            if params.keys():
                result = self.boss_page.profileFunctionality.add_user_profile(params)
                return result
        except:
            raise AssertionError("Creation of profile failed")

    def verify_profile_in_profile_grid(self, canvas_id, search_column_id, **params):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = dict()
            column_data['2'] = params["firstName"]
            column_data['3'] = params["lastName"]
            if 'selectedPhoneNumber' in params:
                column_data['6'] = params["selectedPhoneNumber"]

            if 'selectedExtn' in params:
                column_data['5'] = params["selectedExtn"]

            result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, params["email"], column_data)
            return result
        except:
            raise AssertionError("Could not verify that the profile is in the profile grid")

    def verify_profile_in_users_grid(self, canvas_id, search_column_id, **params):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = dict()
            column_data['2'] = params["firstName"] + " " + params["lastName"]
            result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, params["email"], column_data)
            return result
        except:
            raise AssertionError("Could not verify that the profile is in the users grid")

    def select_profile_in_profile_grid(self, canvas_id, search_column_id, **params):
        try:
            result = self.boss_page.commonfunctionality.select_item_in_grid(canvas_id, search_column_id, params["email"])
            return result
        except:
            raise AssertionError("Could not select the profile in the profile grid")

    def select_multiple_profiles_in_profile_grid(self, canvas_id, search_column_id, *search_list):
        try:
            if len(search_list) == 0:
                return False

            profile_list = []
            for profile in search_list:
                profile_list.append(profile["email"])

            result = self.boss_page.commonfunctionality.select_multiple_items_in_grid(canvas_id, search_column_id, profile_list)
            return result
        except Exception, e:
            print(e)
            raise AssertionError("Could not select the profiles in the profile grid")

    def click_button(self, button_id):
       try:
            result = self.boss_page.commonfunctionality.click_button(button_id)
       except Exception as error:
            raise AssertionError("Could not click on the specified button " + error.message)

    def refresh_browser(self):
        """
        `Description:` To refresh browser page
        """
        try:
            self.boss_page.commonfunctionality.refresh_browser()
        except:
            raise AssertionError("No error message is displayed on the screen")


    def change_phone_pin_and_save(self, pin):
        """
        `Description:` To change the phone pin and press save
        """
        try:
            return self.boss_page.commonfunctionality.change_phone_pin_and_save(pin)
        except:
            raise AssertionError("Could not change the phone pin")

    def verify_phone_pin_change(self, pin):
        """
        `Description:` To verify that the pin change succeeded
        """
        try:
            return self.boss_page.commonfunctionality.verify_phone_pin_change(pin)
        except:
            raise AssertionError("Could not verify the change the phone pin")

    def verify_phone_pin_change_failed(self, message):
        """
        `Description:` To verify that the pin change failed
        """
        try:
            return self.boss_page.commonfunctionality.verify_phone_pin_change_failed(message)
        except:
            raise AssertionError("Could not verify the change the phone pin failed")

    def click_element_by_xpath(self, **params):
        """
        `Description:` Login to the BOSS portal using the username and password

        `:param1` username: URL

        `:param2` username: User email address

        `:param3` password: user password

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self.boss_page.commonfunctionality.click_element_by_xpath(params)
            print("DEBUG: Click successful")
        except:
            raise AssertionError("Click Failed!!")

    def input_text_in_input_field(self, **params):
        try:
            self.boss_page.commonfunctionality.input_text_in_input_field(params)
            time.sleep(1)
            print("DEBUG: Input successful")
        except Exception, e:
            print(e)
            raise AssertionError("Input Failed!!")

    def select_option_in_select(self, **params):
        try:
            self.boss_page.commonfunctionality.select_option_in_select(params)
            time.sleep(1)
            print("DEBUG: Select successful")
        except Exception, e:
            print(e)
            raise AssertionError("Select Failed!!")

    def sleep_in_seconds(self, **params):
        try:
            self.boss_page.commonfunctionality.sleep_in_seconds(params)
            print("DEBUG: Sleep successful")
        except Exception, e:
            print(e)
            raise AssertionError("Sleep Failed!!")

    def verify_page_does_not_contain(self, **params):
        status = self.verify_page(**params)
        if status is True:
            return False;
        else:
            return True

    def click_on_phone_system_users(self):
        self.boss_page.commonfunctionality.click_on_phone_system_users()

    def right_click_link_in_grid(self, **params):
        '''
        `Description:` This function will right click link in GRID

        `Param1:` Grid ID

        `Param2:` Link

        `Returns:` None

        '''
        try:
            self.boss_page.commonfunctionality.right_click_link_in_grid(params['grid'], params['link'], params['context_item'])
        except:
            print("Could not access link", self.click_link_in_grid.__doc__)
            raise AssertionError("Right Click operation Failed!!")

    def check_it_says(self, option):
        self.boss_page.commonfunctionality.check_it_says(option)

    def select_tab(self, tab, tabContent):
        '''
        Selects a tab

        :param tab:
        :return:
        '''
        try:
            self.boss_page.commonfunctionality.select_tab(tab, tabContent)
        except:
            print("Could not access link", self.select_tab.__doc__)
            raise AssertionError("Select tab operation Failed!!")

    def adjust_voicemail_interaction(self, extension):
        self.boss_page.commonfunctionality.adjust_voicemail_interation(extension)

    def verify_voicemail_interaction(self, extension):
        self.boss_page.commonfunctionality.verify_voicemail_interaction(extension)

    def select_call_routing_for_user(self, user_email):
        """
         To select Call Routing tab in the Phone/Service details of the selected user

         :param params: Email address of user

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.select_call_routing_for_user(user_email)
            return result
        except:
            raise AssertionError("Call Routing configuration failed!")


    def configure_call_routing(self):
        """
         To configure Call Routing with phone numbers

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_call_routing_options()
            return result
        except:
            raise AssertionError("Call Routing configuration failed!")

    def configure_call_forwarding(self):
        """
         To configure Incoming Call Forwarding

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_call_forwarding()
            return result
        except:
            raise AssertionError("Call Forwarding configuration failed!")

    def call_forwarding_configured(self):
        """
         To verify Call Forwarding is configured

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.call_forwarding_configured()
            return result
        except:
            raise AssertionError("Verify Call Forwarding configured failed!")

			
    def unassign_profile(self,*params):
        try:
                self.boss_page.profileFunctionality.unassign_profile()
        except:
            raise AssertionError("Unassign of profile failed")

    def verify_close_order_is_created(self, canvas_id, search_column_id,closeOrderID,**params):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = dict()
            column_data['3'] = closeOrderID                         #OrderID column
            column_data['5'] = params['profileLocation']            #Location column
            column_data['11'] = "Close"                             #Type column
            column_data['12'] = "Close Service"                     #Sub Type column
            column_data['13'] = "Closed"                            #Status column
            result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, column_data['3'], column_data)
            return result
        except:
            raise AssertionError("Could not verify the close order was created")


    def verify_service_status_closed(self, canvas_id, search_column_id, *params):
        try:
            # here we will extract the data we want to use to do the search and comparison
            column_data = dict()
            column_data['5']=params[0]
            column_data['10'] = "Closed"
            column_data['27'] = params[0]
            column_data['32'] = "Closed"
            column_data['49'] = params[0]
            column_data['54'] = "Closed"
            column_data['71'] = params[0]
            column_data['76'] = "Closed"
            result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, params[0], column_data)
            return result
        except:
            raise AssertionError("Could not verify the close order was created")

    def orderID_of_latest_orders(self):
        try:
            return self.boss_page.commonfunctionality.orderID_of_latest_orders()
        except:
            raise AssertionError("Could not get the latest order id")


    def configure_always_forward_to_voicemail(self):
        """
         Configure always forward to voicemail

         :param params: None

         :return: None

         `Created by:` vuh
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_always_forward_to_voicemail()
            return result
        except:
            raise AssertionError("Always forward to voicemail configuration failed!")


    def always_forward_to_voicemail_configured(self):
        """
         Check to see if always forward to voicemail is configured

         :param params: None

         :return: None

         `Created by:` vuh
        """
        try:
            result = self.boss_page.phoneServiceUsers.always_forward_to_voicemail_configured()
            return result
        except:
            raise AssertionError("Check for always forward configuration failed!")


    def open_operations_ipPbx_primaryPartition(self):
        """
        `Description:` To open the Profile page in the Operations > IP PBX, Primary Paritiion > Profiles
        """
        try:
            self.boss_page.commonfunctionality.open_operations_ipPbx_primaryPartition()

        except:
            raise AssertionError("Click on 'Operations > IP IPBX - Primary Partition > Profiles' - Failed!")

    def verify_profiles_grid_display(self):
        """
         `Description:` To verify the Profiles grid is displayed.

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_profiles_grid_display()
            return result

        except:
            raise AssertionError("To verify the Profiles grid is displayed - Failed!")


    def select_one_profile(self, **parmas):
        """
         `Description:` To verify the Profiles grid is displayed.

         `Param:`  Product type to filter on (eg: Product "Connect CLOUD Standard")

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.select_one_profile(parmas)
            return result

        except:
            raise AssertionError("To verify the Profiles grid is displayed - Failed!")


    def get_first_record_from_profile(self):
        """
         `Description:` Gets the first profile record.

         :return: A list of data from the first record.
        """

        try:
            profileData = self.boss_page.commonfunctionality.get_first_record_from_profile()
            return profileData

        except:
            raise AssertionError("Gets the first profile record. - Failed!")


    def click_reassign_button(self):
        """
         `Description:` Click on ReAssign button

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.click_reassign_button()
            return result

        except:
            raise AssertionError("Click on ReAssign button - Failed!")


    def verify_reassign_wizard_display(self):
        """
         `Description:` Verify the reassign wizard is displayed

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_reassign_wizard_display()
            return result

        except:
            raise AssertionError("Verify the reassign wizard is displayed - Failed!")


    def validate_reassigned_extension(self, **params):
        """
        `Description:` Validate reassigned number.
        Given an invalid number, validates the number is invalid with the error message.

         :return: True if error validation is successful.
        """
        try:
            result = self.boss_page.commonfunctionality.validate_reassigned_extension(params)
            return result

        except:
            raise AssertionError("Validate reassigned number - Failed!!")

    def configure_find_me_numbers(self):
        """
         To configure Find Me Numbers

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.configure_find_me_numbers()
            return result
        except:
            raise AssertionError("Verify Find Me Numbers configured failed!")

    def find_me_numbers_configured(self):
        """
         To verify Find Me Numbers are configured

         :param params: None

         :return: None

         `Created by:`
        """
        try:
            result = self.boss_page.phoneServiceUsers.find_me_numbers_configured()
            return result
        except:
            raise AssertionError("Verify Call Forwarding configured failed!")

    def upload_specified_file(self, **params):
        try:
            if params.keys():
                return self.boss_page.commonfunctionality.upload_specified_file(params)
            return False
        except:
            raise AssertionError("Could not upload specified file")

    def preview_profile_import(self):
        try:
            return self.boss_page.profileFunctionality.preview_profile_import()
        except:
            raise AssertionError("Could not preview the imported profiles")

    def import_previewed_profiles(self):
        try:
            return self.boss_page.profileFunctionality.import_previewed_profiles()
        except:
            raise AssertionError("Could not import the previewed profiles")

    def read_profiles_from_import_file(self, file_path):
        try:
            return self.boss_page.profileFunctionality.read_profiles_from_import_file(file_path)
        except:
            raise AssertionError("Could not read from the specified import file")

    def verify_imported_profiles_in_profile_grid(self, canvas_id, search_column_id, *profile_list):
        try:
            for profile in profile_list:
                # here we will extract the data we want to use to do the search and comparison
                column_data = dict()
                column_data['2'] = profile["firstName"]
                column_data['3'] = profile["lastName"]
                column_data['8'] = profile["type"]
                if profile['phoneNumber'] != '':
                    column_data['7'] = profile["phoneNumber"]
                if profile['extn'] != '':
                    column_data['6'] = profile["extn"]
                result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, profile["email"], column_data)
                if result == False:
                    return result
            return result
        except:
            raise AssertionError("Could not verify that the profile is in the profile grid")

    def verify_imported_profile_in_users_grid(self, canvas_id, search_column_id, *profile_list):
        try:
            for profile in profile_list:
                # here we will extract the data we want to use to do the search and comparison
                column_data = dict()
                column_data['2'] = profile["firstName"] + " " + profile["lastName"]
                if profile['phoneNumber'] != '':
                    column_data['4'] = profile["phoneNumber"]
                if profile['extn'] != '':
                    column_data['5'] = profile["extn"]
                result = self.boss_page.commonfunctionality.verify_item_exists_in_grid(canvas_id, search_column_id, profile["email"], column_data)
                if result == False:
                    return result
            return result
        except:
            raise AssertionError("Could not verify that the profile is in the profile grid")

    def verify_number(self, *param):
        """
        `Description:` To verify a number exists (Extension or Number)
         :param A number either Extension or Number.

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_number(param)
            return result

        except:
            raise AssertionError("To verify a number exists - Failed!")


    def verify_all_column_names_in_Profiles(self):
        """
        `Description:` Gets all the column headings from the Profiles table
         and checks to see if all the column headings are displayed.

        `Returns:` True if all column headings are found, False if the expected columns heading are not found.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_all_column_names_in_Profiles()
            return result

        except:
            raise AssertionError("Getting the column headings from the Profiles table - Failed!!")


    def verify_buttons_enabled_in_Profiles(self, *param):
        """
         `Description:` To verify the buttons that are passed in are enabled in the profiles

         :param List of button ids that should be enabled.

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.verify_buttons_enabled_in_Profiles(param)
            return result

        except:
            raise AssertionError("To verify the buttons that are passed in are enabled in the profiles - Failed!!")


    def select_profile(self, **param):
        """
         `Description:` Selects a profile based on the optional product filter passed in.
         :param A map (dictionary) containing the product name and the minimum number of results needed

         :return: True if successful.
        """
        try:
            result = self.boss_page.commonfunctionality.select_profile(param)
            return result

        except:
            raise AssertionError("Selects a profile based on the optional product filter passed in - Failed!!")


    def Open_Operation_All_Orders(self):
        """
        `Description:` Go to Operation > All Orders

        `Created by:` Okba
        """
        try:
            result = self.boss_page.commonfunctionality.Open_Operation_All_Orders()
            return result
        except Exception,e:
            print(e)
            raise AssertionError("Page Operations > All Orders failed!!")