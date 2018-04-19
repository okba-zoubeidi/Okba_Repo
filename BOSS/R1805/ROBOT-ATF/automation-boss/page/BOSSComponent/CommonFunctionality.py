"""Module for execution of common portal functionalities such as login, log out, account switch etc
   File: CommonFunctionality.py
   Author: Kenash Kanakaraj
"""

import os
import sys
import time
import imaplib
import time,re
import email
import datetime
from time import gmtime, strftime
from collections import defaultdict
import inspect
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#For console logs while executing ROBOT scripts
from robot.api.logger import console

#TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
#import base
import web_wrappers.selenium_wrappers as base

from log import log
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
__author__ = "Kenash Kanakaraj"


_RETRY_COUNT = 3

class CommonFunctionality(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.counter = 20
        self.counter=5     #for retries

    def open_url(self, url):
        """
        `Description:` To open BOSS portal.

        `:param` url: URL of BOSS Page

        `:return:`

        `Created by:` Kenash K
        """
        self._browser.go_to(url)
        log.mjLog.LogReporter("CommonFunctionality", "info", "Open URL successful")

    def client_login(self, username, password, **options):
        """
        `Description:` Login for BOSS portal

        `:param1` username: URL

        `:param2` username: User email address

        `:param3` password: user password

        `:return:` status - True/False

        `Created by:` Kenash K
        """
        try:
            status=False
            self.action_ele.clear_input_text("LoginUserName")
            self.action_ele.clear_input_text("LoginPassword")
            self.action_ele.input_text("LoginUserName", username)
            self.action_ele.input_text("LoginPassword", password)
            self.action_ele.click_element("LoginSubmit")
            time.sleep(2)
            #self.action_ele.explicit_wait("Log_off")
            status=True
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status
    def verify_text(self, page_identifier, exp_text='', **options):
        """
        `Decription:` Verify text in the element_locator

        `:param` page_identifier: Element of page

        `:param` exp_text: expected text

        `:param` options:

        `:return:`

        `Created by:` Kenash K
        """
        status = False
        var = self.query_ele.get_text(page_identifier)
        if exp_text in var:
                status = True
        return status

    def switch_page(self, **params):
        """
        `Description:` To switch to other pages based on given name

        `:param` params: name page which need to be switch

        `:return:`

        `Created by:` Kenash K
        """
        try:
            print("IN COMMON SWITCH")
            print(params)
            getattr(self, "switch_page_" + params['page'])(params)
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_page_switch_account(self, *page):
        """
        `Description:` Switch to switch account page

        `:param` page:

        `:return:`

        `Created by:` Kenash K
        """
        try:

            self.action_ele.click_element('User_Options')
            self.action_ele.click_element('Switch_account')
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_account(self, account_name, options):
        """
        `Description:` Switch user account

        `:param` account_name: name of person whose account to be used

        `:param` options:

        `:return:`

        `Created by:` Kenash K
        `Modifed by: Saurabh Singh
        """
        # switch users with the role
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.clear_input_text('AutoComplete_textbox')
            time.sleep(1)
            self.action_ele.input_text('AutoComplete_textbox',account_name)
            #time.sleep(1) #time to populate the select data
            self.action_ele.explicit_wait("switch_account_list")
            self.action_ele.press_key('AutoComplete_textbox', 'ENTER')
            dropbox = self._browser.element_finder("Peopleselect_dropbox")
            for i in range(self.counter):
                if dropbox.is_enabled():
                    self.action_ele.select_from_dropdown_using_text('Peopleselect_dropbox', options)
                else:
                    time.sleep(1)
            self.action_ele.click_element('SwitchAcc_ok')
            time.sleep(5)
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_page_users(self, *page, **params):
        """
        `Description:` Switch to users page

        `:param` page:

        `:param` params:

        `:return:`

        `Created by:` Kenash K
        """
        time.sleep(5)
        try:
            result = False
            time.sleep(1)
            for i in range(4):
                #TODO: Links has to be identified and clicked.
                #since the submenu disappears after clicking menu link
                try:
                    self.action_ele.click_element("Phone_system_tab")
                    self.action_ele.click_element("Users_link")
                    time.sleep(1)
                    print("SWITCHING TO USER PAGE :%s" %i)
                    user_page_load = self.action_ele.explicit_wait('email_search')
                    if user_page_load:
                        result = True
                        break
                except:
                    pass
            else:
                raise

        except Exception as err:
            print(err.message)
            raise Exception
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_page_usergroup(self, *page, **params):
        """
        `Description:` Switch to user group page

        `:param` page:

        `:param` params:

        `:return:`

        `Created by:` Vasuja K
        """
        time.sleep(3)
        try:
            result = False
            time.sleep(1)
            for i in range(4):
                #TODO: Links has to be identified and clicked.
                #since the submenu disappears after clicking menu link
                try:
                    self.action_ele.click_element("Phone_system_tab")
                    self.action_ele.click_element("usergroup_link")
                    time.sleep(1)
                    print("SWITCHING TO USER PAGE :%s" %i)
                    user_page_load = self.action_ele.explicit_wait('userGroupGridnew_group_addButton')
                    if user_page_load:
                        result = True
                        break
                except:
                    pass
            else:
                raise

        except Exception as err:
            print(err.message)
            raise Exception
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_page_accounts(self, *options):
        """
        `Description:` Switch to accounts page

        `:param` options:

        `:return:`

        `Created by:` Kenash K
        """
        self.action_ele.explicit_wait('Operations_tab')
        self.action_ele.mouse_hover('Operations_tab')
        self.action_ele.explicit_wait('Accounts_link')
        self.action_ele.click_element('Accounts_link')

    def switch_page_contracts(self, *options):
        """
        `Description:` Switch to contacts page

        `:param `options:

        `:return:`

        `Created by:` Kenash K
        """
        self.action_ele.mouse_hover('Operations_tab')
        #self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.action_ele.click_element('Contracts_link')
        time.sleep(2)


    def switch_page_VCFE(self, **params):
        """
        `Decription:` Switch to VCFE page

        `:param` params:

        `:return:`

        `Created by:` Kenash K
        """
        self.action_ele.click_element("Phone_system_tab")
        self.action_ele.click_element("VCFE_link")

    def search_user(self, user_name):
        """
        `Description:` Search user in grid

        `:param` user_name:

        `:return:`

        `Created by:` Kenash K
        """
        print("IN Search User")
        self.action_ele.click_element('Contact_name_filter')
        self.action_ele.input_text('Contact_name_filter', user_name)

    def switch_page_partitions(self, *options):
        """
        `Description:` Switch to partition page

        `:param` options:

        `:return:`

        `Created by:` Kenash K
        """
        self.action_ele.mouse_hover('Operations_tab')
        self.action_ele.click_element('Partitions_link')

    def switch_page_phonenumber(self, *options):
        """
        `Description:` Switch to primary phone number page

        `:param` options:

        `:return:`

        `Created by:` Vasuja K
        """
        time.sleep(7)
        #self.action_ele.explicit_wait('Operations_tab')
        self.action_ele.mouse_hover('Operations_tab')
        self.action_ele.click_element('ph_phone_numbers_submenu')

    def switch_page_primary_partition(self, *options):
        """
        `Description:` Switch to primary partition page

        `:param` options:

        `:return:`

        `Created by:` Kenash K
        """
        self.action_ele.mouse_hover('Operations_tab')
        self.action_ele.click_element('Primary_Partition_link')

    def switch_page_services(self, *page, **params):
        """
        `Description:` switch to services page

        `:param` page: name of page

        `:param` params:

        `:return:`

        `Created by:` Kenash K
        """
        try:
            time.sleep(5)
            result = False
            time.sleep(1)
            for i in range(4):
                # TODO: Links has to be identified and clicked.
                # since the submenu disappears after clicking manu link
                try:
                    self.action_ele.click_element('Organization_tab')
                    time.sleep(2)
                    self.action_ele.click_element('Services_link')
                    time.sleep(1)
                    print("SWITCHING TO USER PAGE :%s" % i)
                    servicepage_load = self.action_ele.explicit_wait('headerRow_BaseNameStripped')
                    if servicepage_load:
                        result = True
                        break
                except:
                    pass
            else:
                raise
            self.action_ele.explicit_wait("select_all_check_box")
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_page_Visual_Call_Flow_Editor(self, options):
        """
        `Description:` Switch to visual call flow editor page

        `Param:`  None

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            result = False
            for i in range(4):
                # TODO: Links has to be identified and clicked.
                # since the submenu disappears after clicking manu link
                try:
                    self.action_ele.explicit_wait('phone_system_nav')
                    self.action_ele.click_element('phone_system_nav')
                    self.action_ele.explicit_wait("Visual_Call_Flow_Editor")
                    self.action_ele.click_element("Visual_Call_Flow_Editor")
                    print("SWITCHING TO VCFE PAGE :%s" % i)
                    vcfe_loaded = self.action_ele.explicit_wait("vcfe_add_dropdown")
                    if vcfe_loaded:
                        #self.action_ele.explicit_wait("vcfe_extension_textbox", ec="visibility_of_element_located")
                        self.action_ele.explicit_wait("VCFE_datagrid")
                        result = True
                        break
                except:
                    pass
            else:
                raise AssertionError
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_page_Invoices_and_Payments(self, options):
        """
        `Description:` Switch to invoice and payments page

        `Param:`  None

        `Returns:` None

        `Created by:` Vasuja K
        """
        time.sleep(2)
        self.action_ele.click_element('Organization_tab')
        self.action_ele.click_element("Invoices_Payments")

    def switch_page_geographic_locations(self, options):
        """
        `Description:` Switch to geographic location page

        `Param:`  None

        `Returns:` None

        `Created by:` Vasuja K
        """
        time.sleep(5)
        self.action_ele.click_element('phone_system_nav')
        self.action_ele.click_element("geo_loc")

    def switch_page_bridged_call_appearances(self, params):
        """
        switching to the bridged call appearances page
        :return:
        """
        time.sleep(2)
        self.action_ele.explicit_wait('phone_system_nav')
        self.action_ele.click_element('phone_system_nav')
        self.action_ele.click_element("Bridged_Call_Appearances")

    def switch_page_operations_phone_numbers(self, params):
        """
        switching to the operations - phone numbers page
        :return:
        """
        time.sleep(2)
        self.action_ele.click_element('Operations_tab')
        self.action_ele.click_element("ph_phone_numbers_submenu")

    def switch_page_phone_systems_phone_numbers(self, params):
        """
        switching to the phone systems - phone numbers page
        :return:
        """
        time.sleep(2)
        self.action_ele.click_element('Phone_system_tab')
        self.action_ele.click_element("Ph_system_phone_numbers")

    def switch_page_phone_systems_Add_On_Features(self, params):
        """
        switching to the phone systems - phone numbers page
        :return:
        """
        time.sleep(2)
        self.action_ele.click_element('Phone_system_tab')
        self.action_ele.click_element("add-on_features_submenu")

    def switch_page_phone_systems_on_hold_music(self, params):
        """
        switching to the phone systems - on hold music page
        :return:
        """
        time.sleep(2)
        self.action_ele.click_element('Phone_system_tab')
        self.action_ele.click_element("Ph_system_on_hold_music")

    def switch_page_account_home(self, params):
        """
        switching to the operations - phone numbers page
        :return:
        """
        time.sleep(1)
        self.action_ele.click_element('Account_Home_Page')
        time.sleep(1)

    def update_password(self, new_pwd, old_pwd):
        """
        `Description:` To update the old password

        `:param` new_pwd: the password need to be set

        `:param` old_pwd: old password

        ``:return:``

        `Created by:` Kenash K
        """
        try:
           self.action_ele.click_element('change_password')
           self.action_ele.input_text('old_password', old_pwd)
           self.action_ele.input_text('cp_NewPersonPassword', new_pwd)
           self.action_ele.input_text('cp_ConfirmPersonPassword', new_pwd)
           self.action_ele.click_element('cp_changePersonPasswordForm_OK')
           self.action_ele.explicit_wait("ok_box")
           time.sleep(2)
           self.action_ele.click_element("ok_box")
           print("password set")
        except Exception,e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_link_in_partition(self, link='', partition=''):
        """
        `Description:` switch to partition link

        `:param` link: link to click on partition

        `:param` partition: partition name

        ``:return:``

        `Created by:` Kenash K
        """
        #todo remove debugger
        self.action_ele.mouse_hover('Phone_system_tab')
        if partition is not '':
            #todo get the element for selected partition in queryelement
            self.action_ele.mouse_hover('Phone_system_tab')
            partitions = self._browser.elements_finder('Partitions')
            for part in partitions:
                if part.text == partition:
                    part.click()
                    part.find_element_by_link_text(link).click()
                    break

    def verify_grid_value(self, gridvalue):
        '''
        `Description:` Verify the values present in grid

        `:param1` gridvalue: values of grid

        `:return:` True/False

        `Created by:` Kenash K
        '''
        #TODO get the valur from the gridcontainer and check the value
        try:
            verify_text = self.query_ele.text_present(gridvalue)
            if verify_text:
                return True

            else:
                return False
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def click_link_in_grid(self, gridcontainer, link):
        '''
        `Description:` click link in grid

        `:param` link: the link which need to click

        `:return:`

        `Created by:` Kenash K
        '''
        try:
            self.grid = self._browser.element_finder(gridcontainer)
            self.grid.find_element_by_partial_link_text(link).click()
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def select_option(self, option, locator):
        '''
        `Description:` To select option

        `:param` option: the option which need to be selected

        `:param` locator: locator which need to select

        `:return:`

        `Created by:` Kenash K
        '''
        try:
            self.action_ele.select_from_dropdown_using_text(locator, option)
            self.action_ele.explicit_wait('contract_alert_ok')
            self.action_ele.click_element('contract_alert_ok')
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_link_in_operations(self, linkText):
        """
        `Description:` switch to links in operation page

        `:param` linkText: on which user has to switch

        `:return:`

        `Created by:` Kenash K
        """
        self.action_ele.mouse_hover('operations_nav')
        elements=self._browser.elements_finder(mapDict['operations_div']["BY_VALUE"]+"//*")
        for element in elements:
            if element.text == linkText:
                element.click()

    def accept_agreement(self):
        """
        `Description:` To accept agreement.

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element("dm_login_agree")
        except Exception,e:
            print(e)
            print("Accept agreement failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_tabs(self, tab_list):
        """
        `Description:` verify the tab on the page

        `:param` tab_list: list of all tabs

        `:return:` True or False

        `Created by:` Kenash K
        """
        try:
            tab_list_obj = self._browser.elements_finder('Home_menu')
            elements = tab_list_obj[0].text.split('\n')

            for element in tab_list:
                print element
                if element not in elements:
                    return False
            return True

        except Exception,e:
            print(e)
            print("Verification Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def change_password(self, new_password='', old_pwd='', options='login'):
        """
        `Description:` To change user password

        `:param` new_password: new password which need to be set

        `:param` old_pwd: old password of user

        `:param` options:

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.explicit_wait('cp_NewPersonPassword')
            self.action_ele.input_text('cp_NewPersonPassword', new_password)
            self.action_ele.input_text('cp_ConfirmPersonPassword', new_password)
            self.action_ele.click_element('cp_changePersonPasswordForm_OK')
            time.sleep(10)
            self.action_ele.click_element("password_confirmation")
            #
            # self.action_ele.explicit_wait("fnMessageBox_OK")
            # self.action_ele.click_element("fnMessageBox_OK")
            time.sleep(3)
        except Exception,e:
            print(e)
            print("Could not change password")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def stop_impersonating(self):
        """
        `Description:` To stop impersonatingthe for current user

        `:return:` None

        `Created by:` Guo Zheng
        """
        try:
            result = False
            time.sleep(1)
            for i in range(4):
                # TODO: Links has to be identified and clicked.
                # since the submenu disappears after clicking menu link
                try:
                    self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
                    self.action_ele.explicit_wait('User_Options')
                    self.action_ele.click_element('User_Options')
                    self.action_ele.click_element('Homepage_logoff')
                    time.sleep(1)
                    print("Log off user tries:%s" % i)
                    log_off_success = self.action_ele.explicit_wait('LoginUserName')
                    if log_off_success:
                        result = True
                        break
                except:
                    pass
            else:
                pass
        except Exception as err:
            print("log off failed", err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise

    def log_off(self):
        """
        `Description:` To log off the current user

        `:return:` None

        `Created by:` Kenash K
        """
        try:
            result = False
            time.sleep(1)
            for i in range(4):
                # TODO: Links has to be identified and clicked.
                # since the submenu disappears after clicking menu link
                try:
                    self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
                    self.action_ele.explicit_wait('User_Options')
                    self.action_ele.click_element('User_Options')
                    self.action_ele.click_element('Homepage_logoff')
                    time.sleep(1)
                    print("Log off user tries:%s" % i)
                    log_off_success = self.action_ele.explicit_wait('LoginUserName')
                    if log_off_success:
                        result = True
                        break
                except:
                    pass
            else:
                pass
        except Exception as err:
            print("log off failed", err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise

    def close_browser(self):
        """
        `Description:` Close the browser object

        `:param` driver: WebDriver object

        `:return:``

        `Created by:` Kenash K
        """
        time.sleep(2)
        self._browser.quit()

    def move_to_tab(self, tab_name):
        """
        `Description:` move to perticular tab

        `:param` tab_name:  name of tab

        `:return:`` None

        `Created by:` Kenash K
        """
        self.action_ele.click_element(tab_name)

    def right_click(self, name):
        """
        `Description:` perform right click operation on elments and redirect to change password field

        `:param` name: First Name last Name

        `:return:` None

        `Created by:` Saurabh Singh
        """
        print("*******************")
        #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
        action = ActionChains(self._browser._browser)
        time.sleep(2)
        print("Finding user.... %s" % name)
        el = self._browser.elements_finder("user_list")#to get the list of elements from all the tray
        #print(el)
        for elm in el:
            first_value = elm.find_elements_by_tag_name("div")
            print("Finding user.... %s" % first_value[0].text)
            if first_value[0].text==name.replace('_',''):
                action.context_click(first_value[0]).perform()
                break

        self.action_ele.click_element('ResetPasswordContextMenuItem')
        self.action_ele.explicit_wait("reset_pwd")
        self.action_ele.click_element("reset_pwd")

    def change_profile_password_from_user_page(self,name):
        """
        `Description:` redirect user to change password setting page from inside user detail page

        `:param` name: First Name last Name

        `:return:` result

        `Created by:` Saurabh Singh
        """
        try:
            result=False
            time.sleep(2)
            el=self._browser.elements_finder("user_link")
            for elm in range(len(el)):
                if el[elm].text==name.replace('_', ''):
                    el[elm].click()
                    self.action_ele.explicit_wait("change_password")
                    result = True
                    break
            print(result)

        except Exception,e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return result
    def close_user(self, params):
        """
        `Description:` This Test case will close the User from the page with and without phone number user

        `:param` email: email of user who is going to close

        `:param` name: name of requester

        `:return:` status

        `Created by:` Saurabh Singh

        `Modified by:` Megha Bansal
        """
        result = False
        time.sleep(2)
        params = defaultdict(lambda: '', params)
        email = params['email']
        name = params['name']
        self.action_ele.click_element("email_search")
        self.action_ele.input_text("email_search",email)
        eml = self._browser.elements_finder("email_list")
        #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        #phn = self._browser.elements_finder("phone_name")
        for each in range(len(eml)):
            if eml[each].text==email:
                action = ActionChains(self._browser._browser)
                action.context_click(eml[each]).perform()
                context_menu_items = self._browser.elements_finder("close_user_context_menu")
                for menu_items in range(len(context_menu_items)):
                    if context_menu_items[menu_items].text.lower() == "Close User".lower():
                        context_menu_items[menu_items].click()
                        #self.action_ele.click_element(menu_items)
                time.sleep(1)
                self.action_ele.click_element("confirm_box")
                self.action_ele.explicit_wait("header_close_user")
                self.action_ele.click_element("close_user_date")
                self.action_ele.input_text('close_user_date', datetime.date.today().strftime('%m/%d/%Y'))
                self.action_ele.click_element("simple_click")
                time.sleep(1)
                self.action_ele.click_element("simple_click")
                #self.action_ele.click_element("request_dropdown")
                time.sleep(3)
                if params['keepGlobalTn'] == 'no':
                    self.action_ele.select_radio_button('keepGlobalTn_no')
                elif params['keepGlobalTn'] == 'yes':
                    self.action_ele.select_radio_button('keepGlobalTn_yes')
                self.action_ele.select_from_dropdown_using_text("request_dropdown", name)
                time.sleep(3)
                self.action_ele.input_text("case_id",123)
                ##import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
                self.action_ele.click_element("next")
                self.action_ele.click_element("next")
                self.action_ele.click_element("finish_button")

                for i in range(self.counter):
                    try:
                        isDisplayed = self.query_ele.element_displayed("ok_box")
                        if isDisplayed:
                            break
                        else:
                            time.sleep(5)
                    except:
                        self._browser._browser.refresh()
                time.sleep(1)
                self.action_ele.click_element("ok_box")
                time.sleep(5)
                #import pdb
                #pdb.Pdb(stdout=sys.__stdout__).set_trace()
                try:
                    lis=[]
                    #self.action_ele.explicit_wait("home_page")
                    eml = self._browser.elements_finder("email_list")
                    for each in range(len(eml)):
                        lis.append(eml[each].text)
                    if email not in lis:
                        print("User is Closed")
                        print "User is closed successfully"
                        result = True
                    else:
                        print("User is not closed")
                        result=False
                except Exception,e:
                    print "User is not closed successfully"
                    self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                    result = False
                finally:
                    self.action_ele.click_element("email_search")
                    self.action_ele.clear_input_text("email_search")
                    self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                    return result

    def reset_password_from_home_page(self,email=''):
        """
        `Description:` to traverse to password reset page

        `:param` email: email of user whom password is going to reset.

        `:return:`

        `Created by:` Saurabh Singh
        """
        self.action_ele.click_element("home_page_link")
        if self.query_ele.get_text("headerName") == "Reset Password or PIN":
            time.sleep(2)
            #print(email)
            self.action_ele.input_text("userName", email)
            self.action_ele.click_element("submit")
            if self.query_ele.get_text("final_header") == "Request Submitted":
                print("Request has sent")
                #self.action_ele.click_element(".//*[@id='content']/div/p/a")
            else:
                print("Request has not been sent")
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        time.sleep(5)

    def read_email(self, current_time, user_email, emailPassword, emailServer):
        """
        `Description:` read the email and fetch the link


        `:param` current_time: time of email before the the new email arrived

        `:param` user_email: email of user

        `:param` emailPassword: email password

        `:param` emailServer: email of server

        `:return:`

        `Created by:` Saurabh Singh
        """

        #FROM_PWD = "ROD#12345"
        #SMTP_SERVER = "relay.shoretel.com"
        SMTP_PORT = 993

        mail = imaplib.IMAP4_SSL(emailServer)
        mail.login(user_email, emailPassword)
        mail.select('inbox')

        types, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()

        # to read the latest mail
        latest_email_id = int(id_list[-1])
        # print latest_email_id

        for each in range(latest_email_id, latest_email_id - 2, -1):
            #import pdb
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            typ, data = mail.fetch(each, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    # print msg
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_date = msg['Date']
                    time = email_date.split(" ")
                    del (time[-1])
                    time = " ".join(time)
                    time = time.replace(",", "")
                    e_time = datetime.datetime.strptime(time, "%a %d %b %Y %H:%M:%S")
                    print "New Email Time: "+str(e_time)
                    console("New Email Time: "+str(e_time))
                    print "Previos Email Time: "+str(current_time)
                    console("Previos Email Time: "+str(current_time))
                    if current_time != None:
                        if email_subject == "Reset your Mitel password or PIN" and e_time>current_time:
                            if msg.is_multipart():
                                body = msg.get_payload()[0].get_payload()
                                # print "*********************"
                                # print body
                                # body = body.replace("=\r\n", "")
                                body = body.replace("\r\n", "")
                                body = body.replace("3D", "")
                                body = body.replace("==You", "==")
                                #print "**********************"
                                url = re.search(r'http:[\d\D]+?\s', body).group(0)
                                status = True
                                #print(url)
                                return url
                            else:
                                body = msg.get_payload()
                                body = body.replace("=\r\n", "")
                                body = body.replace("3D", "")
                                # body = body.replace("==You", "==")
                                urlList = re.findall(
                                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
                                #print(urlList)
                                if len(urlList) == 0:
                                    url = None
                                else:
                                    url = urlList[0]
                                return url

                        else:
                            url=None
                    else:
                        if email_subject == "Reset your Mitel password or PIN":
                            if msg.is_multipart():
                                body = msg.get_payload()[0].get_payload()
                                # print "*********************"
                                # print body
                                # body = body.replace("=\r\n", "")
                                body = body.replace("\r\n", "")
                                body = body.replace("3D", "")
                                body = body.replace("==You", "==")
                                # print "**********************"
                                url = re.search(r'http:[\d\D]+?\s', body).group(0)
                                status = True
                                # print(url)
                                return url
                            else:
                                body = msg.get_payload()
                                body = body.replace("=\r\n", "")
                                body = body.replace("3D", "")
                                # body = body.replace("==You", "==")
                                urlList = re.findall(
                                    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                    body)
                                # print(urlList)
                                if len(urlList) == 0:
                                    url = None
                                else:
                                    url = urlList[0]
                                return url

                        else:
                            url = None
        return url

    ###############################################

    def check_email(self,fromAdd, user_email, emailPassword, emailServer):
        """
        `Description:` check the email time of latest email

        `:param` fromAdd: sender name

        `:param` user_email: user email

        `:param` emailPassword: email password

        `:param` emailServer: email server

        `:return:`

        `Created by:` Saurabh Singh
        """

        #FROM_PWD = "ROD#12345"
        #SMTP_SERVER = "relay.shoretel.com"
        SMTP_PORT = 993

        mail = imaplib.IMAP4_SSL(emailServer)
        mail.login(user_email,emailPassword)
        mail.select('inbox')

        types, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()

        # to read the latest mail
        latest_email_id = int(id_list[-1])

        for each in range(latest_email_id, latest_email_id - 2, -1):
            typ, data = mail.fetch(each, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    # print msg
                    email_subject = msg['subject']
                    email_from = msg['from']
                    if email_from==fromAdd and email_subject=="Reset your Mitel password or PIN":
                        email_date = msg['Date']
                        time = email_date.split(" ")
                        del(time[-1])
                        time = " ".join(time)
                        time=time.replace(",","")
                        e_time = datetime.datetime.strptime(time, "%a %d %b %Y %H:%M:%S")
                        #print("fetched time from email: "+str(e_time))
                        break
                    else:
                        e_time = None
        print("Checking last mail time: %s " % e_time)
        print(e_time)
        console("Checking last mail time: %s " % e_time)
        console(e_time)
        return e_time

    def reset_password_via_email(self, user_email, emailPassword, emailServer, setPassword):
        """
        `Description:` reset password from email

        `:param` user_email: whom password will be reset

        `:param` emailPassword: email password

        `:param` emailServer: email server

        `:param` setPassword: what password need to be set

        `:return:` status

        `Created by:` Saurabh Singh
        """
        fromAdd = "ShoreTel Sky Support BOSS Auto Env <skysupport@shoretel.com>"
        #print(email+emailPassword+emailServer)
        current_time = self.check_email(fromAdd, user_email, emailPassword, emailServer)
        self.reset_password_from_home_page(user_email)
        count=0
        status=False
        while count<5:
            time.sleep(10)
            url=self.read_email(current_time, user_email, emailPassword, emailServer)

            count+=1
            print("Checking for new Email "+str(count)+" time")
            console("Checking for new Email "+str(count)+" time")
            #print(count)
            if url!=None:
                break

        if url!=None:
            try:
                self.open_url(url)
                self.action_ele.input_text("new_password",setPassword)
                self.action_ele.input_text("confirm_pwd",setPassword)
                self.action_ele.click_element("submit_button")
                if self.query_ele.get_text("confirmation_text")=="Your password has been changed.":
                    print "Password set successfully"
                    status=True
                else:
                    print "Password did not set successfully"
                    status=False
            except Exception,e:
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                print e
                status=False

        else:
            print("No latest Email to set password has arrived")
            status=False
        return status

    def switch_page_order(self, options):
        """
        `Description:` switch to order page

        `:param` options:

        `:return:`

        `Created by:` Saurabh Singh
        """
        try:
            time.sleep(13)
            self._browser._browser.refresh()
            time.sleep(5)
            result = False
            for i in range(4):
                try:
                    time.sleep(3)
                    self.action_ele.explicit_wait("Organization_tab")
                    self.action_ele.click_element('Organization_tab')
                    time.sleep(2)
                    el=self._browser.elements_finder("order_link")
                    for each in range(len(el)):
                        if el[each].text=="Orders":
                            el[each].click()
                            print "Order page is opened successfully"
                            break
                    vcfe_loc_loaded = self.action_ele.explicit_wait("location_tab")
                    if vcfe_loc_loaded:
                        result = True
                        break
                except:
                    pass
            else:
                raise
        except Exception,e:
            print e
            print("rached expection")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def close_open_order(self, Location):
        """
        `Description:` To close open order created by geo location

        `:return:`

        `Created by:` Saurabh Singh
        """
        try:
            status=False
            time.sleep(2)
            self.action_ele.select_from_dropdown_using_text("status_tab","Open")
            self.action_ele.input_text("location_tab", Location)
            self.action_ele.click_element("order_id")
            self.action_ele.explicit_wait("save_button")
            self.action_ele.select_from_dropdown_using_text("order_status", "Closed")
            time.sleep(1)
            self.action_ele.click_element("save_button")
            self.action_ele.explicit_wait("ok_button")
            time.sleep(1)
            el=self._browser.elements_finder("ok_button")
            el[1].click()
            for i in range(5):
                try:
                    time.sleep(1)
                    ok_btn=self.action_ele.explicit_wait('export_button')
                    console("iteration number: %s" %i)
                    if ok_btn:
                        break
                except:
                    pass
            #self.action_ele.explicit_wait("export_button")
            self.action_ele.click_element("location_tab")
            self.action_ele.clear_input_text("location_tab")
            print "Geo Location has been closed"
            status=True
        except Exception,e:
            print(e)
            print e
            status=False
            print("Exception reached")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def close_location(self, Location, name):
        """
        `Description:` To close geo location

        `:return:`

        `Created by:` Saurabh Singh
        """
        try:
            status=False
            time.sleep(1)
            self.action_ele.select_from_dropdown_using_text("geo_location_status", "Pending")
            el=self._browser.elements_finder("geo_location_name_field")
            for each in range(len(el)):
                if el[each].text==Location:
                    action = ActionChains(self._browser._browser)
                    action.context_click(el[each]).perform()
                    break
            self.action_ele.click_element("close_option")
            self.action_ele.select_from_dropdown_using_text("request_dropdown", name)
            self.action_ele.input_text("case_id",123)
            self.action_ele.click_element("close_location_next")
            self.action_ele.click_element("close_location_next")
            self.action_ele.click_element("close_location_finish")
            self.action_ele.explicit_wait("ok_button")
            time.sleep(3)
            self.action_ele.click_element("ok_button")
            self.action_ele.explicit_wait("location_export_button")
            time.sleep(3)
            self.action_ele.explicit_wait("geo_location_status")
            time.sleep(3)
            self.action_ele.select_from_dropdown_using_text("geo_location_status", "Pending")
            time.sleep(3)
            el=self._browser.elements_finder("geo_location_name_field")
            lis=[]
            for each in range(len(el)):
                lis.append(el[each])
            if Location not in lis:
                print "Location is closed"
            else:
                print "Location is not closed"

            status=True
        except Exception,e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def check_alert(self):
        """
        `Description:` Check for alert pop up on page

        `:return:`

        `Created by`  Saurabh Singh
        """
        try:
            browser_obj = self._browser.get_current_browser()
            WebDriverWait(browser_obj, 3).until(EC.alert_is_present(), "Checking for Alert Pop up")
            alert = browser_obj.switch_to.alert
            print alert.text
            alert.accept()
        except Exception,e:
            print e
            print"No alert"
            #self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_page_personal_information(self):
        """
        `Description:` switch to personal information page

        `:return:`

        `Created by:` Saurabh Singh
        """
        try:
            result = False
            time.sleep(2)
            self.action_ele.click_element('User_Options')
            self.action_ele.click_element('personal_information_pageLink')
            self.action_ele.explicit_wait('change_password')
            result = True
        except Exception,e:
            print e
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return result
    def get_build(self):
        """
        `Description:` To get the build version

        `:return:`

        `Created by:` Saurabh Singh
        """
        el = self._browser.elements_finder("build")
        return el[0].text

    def switch_page_aob(self, *page):
        """
        `Description:` Switch to AOB page

        `:param` page:

        `:return:`

        `Created by:` Kenash K
        """
        try:
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.click_element('Phone_system_tab')
            self.action_ele.click_element("aob_setup_link1")
            #to witch to different windows
            win = self._browser._browser.window_handles
            self._browser._browser.switch_to_window(win[len(win) - 1])
            #self.action_ele.switch_to_window(1)
            self.action_ele.explicit_wait("welcome")
            if "Mitel Easy Setup" == self._browser._browser.title:
                print("AOB page is loaded")
            #aob_link = self.query_ele.get_element_attribute('aob_setup_link', 'href')
            #self._browser.go_to(aob_link)
            #self.action_ele.explicit_wait("aob_help_url") #added to wait till page load
        except Exception as err:
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            raise AssertionError("Could not switch to AOB page")

    def switch_page_phone_number(self,*params):
        """
        `Description:` To switch to phone number page

        `:param` params:

        `:return:`

        `Created by:` Kenash K
        """
        try:
            result = False
            time.sleep(2)
            i=0
            for i in range(3):
                self.action_ele.click_element('Phone_system_tab')
                if self.action_ele.click_element('Phone_system_tab')=="None":
                    self.action_ele.click_element('Phone_system_tab')
                time.sleep(2)
                elements = self._browser.elements_finder('Ph_phone_number')
                elements[0].click()
                phone_tab = self.action_ele.explicit_wait("Ph_number_tab")
                if phone_tab:
                    result = True
                    break
                else:
                    pass
            result = True
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return result

    def check_for_error(self):
        """
        `Description:` To check for errors in phone number page

        `:return: `

        `Created by:` Kenash K
        """
        try:
            result = False
            self.action_ele.explicit_wait("Ph_number_tab")
            for i in range(3):
                header = self.query_ele.get_text("Ph_error_heading]")
                time.sleep(2)
                if not header:
                    error = self.query_ele.get_text("Ph_error_message")
                    print(error)
                    self.action_ele.click_element('ok_box')
                    result = False
            else:
                result = True
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return result


    def __add_numbers_request(self,params):
        """
        `Description:`  Private function to add  phone number request

        `:param` params:

        `:return:

        `Created by:` Saurabh Singh
        """
        try:
            time.sleep(2)
            self.action_ele.click_element("Ph_tab_requests")
            self.action_ele.explicit_wait("Ph_add_button")
            self.action_ele.click_element("Ph_add_button")
            self.action_ele.explicit_wait("Ph_domestic_number")
            self.action_ele.click_element("Ph_domestic_number")
            self.action_ele.explicit_wait("Ph_current_providor")
            self.action_ele.input_text("Ph_phone_number_text",params)
            time.sleep(1)
            self.action_ele.click_element("Ph_phone_number_button")
            time.sleep(2)
            self.action_ele.click_element("Ph_next_buton")
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_transfer_request(self,**params):
        """
        `Description:` To add number transfer request. This method can run on windows only due to dependency on
        "autoit" package.

        `:param` params:

        `:return:

        `Created by:` Saurabh Singh
        """
        try:
            try:
                import autoit
            except ImportError as e:
                print e.msg
            console(params)
            status=False
            self.__add_numbers_request(params['phone'])
            self.action_ele.input_text("Ph_account_name",params['accountName'])
            self.action_ele.input_text("Ph_account_number",params["AccountID"])
            self.action_ele.click_element("Ph_account_next")
            time.sleep(1)
            self.action_ele.click_element("Ph_fileupload")
            self.action_ele.explicit_wait("Ph_browse_btn")
            self.action_ele.click_element("Ph_browse_btn")
            autoit.win_exists("[TITLE:Open]")
            time.sleep(2)
            autoit.control_send("[CLASS:#32770]", "Edit1",params['filePath'])
            time.sleep(1)
            autoit.control_click("[CLASS:#32770]", "Button1")
            time.sleep(1)
            self.action_ele.click_element("Ph_ok_confirmation")
            self.action_ele.click_element("Ph_invoice_next")
            time.sleep(1)
            self.action_ele.click_element("Ph_radio_button")
            self.action_ele.click_element("Ph_callerID_next")
            time.sleep(1)
            self.action_ele.click_element("Ph_Directory_radio_button")
            self.action_ele.click_element("Ph_Directory_next")
            time.sleep(1)
            self.action_ele.click_element("Ph_Finish_next")
            self.action_ele.explicit_wait("Ph_upload_button")
            time.sleep(1)
            self.action_ele.click_element("Ph_upload_button")
            self.action_ele.explicit_wait("Ph_upload_choose_button")
            time.sleep(1)
            self.action_ele.click_element("Ph_upload_choose_button")
            autoit.win_exists("[TITLE:Open]")
            time.sleep(2)
            autoit.control_send("[CLASS:#32770]", "Edit1",params['filePath'])
            time.sleep(1)
            autoit.control_click("[CLASS:#32770]", "Button1")
            time.sleep(1)
            self.action_ele.click_element("Ph_submit_button")
            self.action_ele.explicit_wait("Ph_submit_modify")
            time.sleep(2)
            status=True
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_transfer_request(self,params):
        """
        `Description:` TO verify transfer request


        `:param` params:

        `:return:`

         `Created by:` Kenash K
        """
        try:
            status=False
            time.sleep(2)
            self.action_ele.click_element("Ph_tab_requests")
            time.sleep(1)
            self.action_ele.input_text("Ph_header_number",params)
            time.sleep(2)
            text=self.query_ele.get_text("Ph_grid")
            if text=="Submitted":
                print("Request Submitted")
                status=True
            return status
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_LNP_service(self,**prams):
        """
        `Description:` To add LNP request

        `:param` prams:

        `:return:`

         `Created by:` Saurabh Singh
        """
        try:
            status=False
            time.sleep(2)
            self.action_ele.click_element("add_service")
            self.action_ele.explicit_wait("add_service_LNP")
            self.action_ele.click_element("add_service_LNP")
            self.action_ele.select_from_dropdown_using_text("LNP_requested_by",prams['requestedBy'])
            time.sleep(1)
            self.action_ele.select_from_dropdown_using_text("LNP_source",prams['source'])
            self.action_ele.select_from_dropdown_using_text("LNP_Servie_class",prams["serviceClass"])
            time.sleep(1)
            #self.action_ele.select_from_dropdown_using_text("LNP_product","Fee for local number porting (LNP)")
            self.action_ele.select_from_dropdown_using_index("LNP_product",prams['index'])
            self.action_ele.click_element("LNP_next")
            time.sleep(1)
            self.action_ele.click_element("LNP_finish")
            self.action_ele.explicit_wait("LNP_ok")
            confirmation_text = self.query_ele.get_text("LNP_Order_id")
            order_id = re.search(r'-?\d+', confirmation_text).group()
            console(order_id)
            time.sleep(1)
            self.action_ele.click_element("LNP_ok")
            self.action_ele.explicit_wait("add_service")
            status = True
            return order_id

        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def activate_service(self,order_id,phone):
        """
        `Description:` To activate service

        `:param` order_id: Order id of product

        `:param` phone:  phone number

        `:return:`

         `Created by:` Saurabh Singh
        """
        try:
            status = False
            self.action_ele.input_text("Service_search_box",order_id)
            self.action_ele.click_element("order_id_link")
            self.action_ele.explicit_wait("LNP_service_status")
            self.action_ele.click_element("LNP_setting_tab")
            self.action_ele.explicit_wait("checkbox_for_Wait")
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element("LNP_add_TN")
            self.action_ele.input_text("LNP_Text_box","+"+str(phone))
            time.sleep(3)
            self.action_ele.click_element("LNP_save_btn")
            time.sleep(2)
            self.action_ele.click_element("LNP_save_btn")
            time.sleep(1)
            self.action_ele.explicit_wait("LNP_ok")
            time.sleep(1)
            self.action_ele.click_element("LNP_ok")
            #self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
            self.action_ele.explicit_wait("add_service")
            self.action_ele.click_element("order_id_link")
            time.sleep(2)
            self.action_ele.select_from_dropdown_using_text("LNP_service_status","Awaiting Invoice")
            self.action_ele.click_element("LNP_Service_Detail_save")
            self.action_ele.explicit_wait("LNP_ok")
            time.sleep(1)
            self.action_ele.click_element("LNP_ok")
            time.sleep(1)
            self.action_ele.explicit_wait("LNP_Cancel")
            time.sleep(1)
            self.action_ele.click_element("LNP_Cancel")
            time.sleep(1)

            self.action_ele.select_from_dropdown_using_text("LNP_service_status","In Research")
            self.action_ele.click_element("LNP_Service_Detail_save")
            self.action_ele.explicit_wait("LNP_ok")
            time.sleep(1)
            self.action_ele.click_element("LNP_ok")
            time.sleep(1)
            self.action_ele.explicit_wait("LNP_Cancel")
            time.sleep(1)
            self.action_ele.click_element("LNP_Cancel")
            time.sleep(1)

            self.action_ele.select_from_dropdown_using_text("LNP_service_status","Submitted")
            self.action_ele.click_element("LNP_Service_Detail_save")
            self.action_ele.explicit_wait("LNP_ok")
            time.sleep(1)
            self.action_ele.click_element("LNP_ok")
            self.action_ele.explicit_wait("LNP_Cancel")
            time.sleep(1)
            self.action_ele.click_element("LNP_Cancel")
            time.sleep(1)

            self.action_ele.select_from_dropdown_using_text("LNP_service_status","Scheduled")
            self.action_ele.click_element("LNP_Service_Detail_save")
            self.action_ele.explicit_wait("LNP_ok")
            time.sleep(1)
            self.action_ele.click_element("LNP_ok")
            time.sleep(1)
            self.action_ele.explicit_wait("LNP_Cancel")
            time.sleep(1)
            self.action_ele.click_element("LNP_Cancel")
            time.sleep(1)

            self.action_ele.select_from_dropdown_using_text("LNP_service_status","Active")
            self.action_ele.click_element("LNP_Service_Detail_save")
            self.action_ele.explicit_wait("LNP_ok")
            time.sleep(1)
            self.action_ele.click_element("LNP_ok")
            time.sleep(1)
            self.action_ele.explicit_wait("LNP_ok")
            time.sleep(1)
            self.action_ele.click_element("LNP_ok")
            self.action_ele.explicit_wait("add_service")
            time.sleep(1)
            status=self.query_ele.get_text("LNP_status")
            if status=="Active":
                status=True
                return status
            else:
                return status
        except Exception,e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_message_displayed(self, error_message):
        '''
        `Description:` This function will help to check whether the error message is displayed on screen or not

        `Param1:`  error_message

        `Returns:` status - True/False

        `Created by:` Vasuja K
        '''
        try:
            time.sleep(2)
            if error_message in self._browser._browser.page_source:
                print(error_message)
                return True
            else:
                return False
        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def click_cancel(self):
        """
        `Description:` This function will click on Ok button if it is present and then click on Cancel button.

        `Param:`  None

        `Returns:` None

        `Created by:` Vasuja K
        """
        self.action_ele.explicit_wait("vcfe_cancel_button", ec="element_to_be_clickable")
        self.action_ele.click_element("vcfe_cancel_button")
        time.sleep(2)
        #self.action_ele.explicit_wait("VCFE_delete_yes", ec="element_to_be_clickable")
        self.action_ele.click_element('VCFE_delete_yes')
        time.sleep(2)

    def verify_findme(self, option):
        try:
            self.action_ele.explicit_wait('CallRoutingTab_Finish')
            verify = self.query_ele.text_present(option)
            return verify == option

        except Exception as err:
            print(err.message)
            console(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def config_phone_numbers_callrouting(self, label, phone, num):
        try:
            self.action_ele.explicit_wait('CallRoutingTab_Availability')
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings')
            self.action_ele.explicit_wait('CallRoutingTab_ConfigureMainSettings_AddButton')
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings_AddButton')

            self.action_ele.input_text(label, num)
            self.action_ele.input_text(phone, num)
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings_AddFinish')
            time.sleep(2)
            self.action_ele.explicit_wait('CallRoutingTab_Availability')


        except Exception as err:
            print(err.message)
            console(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def config_sim_ring(self, label, num):
        try:
            self.action_ele.explicit_wait('CallRoutingTab_Availability')
            self.action_ele.explicit_wait('CallRoutingTab_ConfigureMainSettings')
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings')
            self.action_ele.explicit_wait('CallRoutingTab_ConfigureMainSettings_Next')
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings_Next')
            self.action_ele.click_element(label)
            self.action_ele.select_from_dropdown_using_text(label, num)
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings_AddFinish')
            time.sleep(2)
            self.action_ele.explicit_wait('CallRoutingTab_Availability')

        except Exception as err:
            print(err.message)
            console(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def config_find_me(self, label, num):
        try:
            time.sleep(5)
            self.action_ele.explicit_wait('CallRoutingTab_Availability')
            self.action_ele.explicit_wait('CallRoutingTab_ConfigureMainSettings')
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings')
            self.action_ele.explicit_wait('CallRoutingTab_ConfigureMainSettings_Next')
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings_Next')
            self.action_ele.explicit_wait('CallRoutingTab_ConfigureMainSettings_Next')
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings_Next')
            self.action_ele.click_element(label)
            self.action_ele.select_from_dropdown_using_text(label, num)
            self.action_ele.click_element('CallRoutingTab_ConfigureMainSettings_AddFinish')
            time.sleep(5)
            self.action_ele.explicit_wait('CallRoutingTab_Availability')

        except Exception as err:
            print(err.message)
            console(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def switch_page_addonfeatures(self, *options):
        self.action_ele.mouse_hover('phone_system_menu')
        self.action_ele.click_element('add-on_features_submenu')

    def switch_page_eccreports(self, *options):
        self.action_ele.mouse_hover('team_menu')
        self.action_ele.click_element('ecc_submenu')
        time.sleep(15)

    def click_on_manage_button(self,**params):
        """
        `Description:` To click on manage button of specified feature

        `:param` params: feature name

        `Created by:` Megha Bansal
        """
        try:
            print("Okba CommonFunctionality1.py!!!!!")
            print("Okba...")
            print(params)
            getattr(self, "click_on_manage_button_" + params['feature'])(params)

            print("Okba CommonFunctionality2.py!!!!!")
        except Exception as err:
            print("Okba ohhh no!")
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def click_on_manage_button_Connect_Scribe_Manage(self,params):
        """
        `Description:` To click on manage button of Connect Scribe
        `Created by:` Okba Zoubeidi
        """
        time.sleep(15)
        print("Okba I'm here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.action_ele.click_element('Connect_Scribe_Manage')
        time.sleep(15)

    def click_on_manage_button_mobility(self,params):
        """
        `Description:` To click on manage button of mobility
        `Created by:` Megha Bansal
        """
        self.action_ele.click_element('Mobility_Manage')

    def switch_page_primary_partition_profiles(self, params):
        """
        `Description:` Switch to the profiles tab of the primary partition page

        `:param` options:

        `:return:`

        """
        self.action_ele.explicit_wait("OperationsPrimaryPartitionsProfiles")
        self.action_ele.click_element("OperationsPrimaryPartitionsProfiles")

    def switch_page_primary_partition_numbers(self, params):
        """
        `Description:` Switch to the numbers tab of the primary partition page

        `:param` options:

        `:return:`

        """
        self.action_ele.explicit_wait("OperationsPrimaryPartitionsNumbers")
        self.action_ele.click_element("OperationsPrimaryPartitionsNumbers")

    def verify_item_exists_in_grid(self, canvasId, searchColumnId, searchText, columnData):
        """
        `Description:` Verify if the specified item exists in the specified grid

        `:canvasId` - the id of the grid (mandatory)
        `:searchColumnId` - the id of the search box to search from (mandatory)
        `:searchText` - the text to search for (mandatory)
        `:columns` - OPTIONAL - a map of column numbers and data for each column. If not supplied, only the presence of the search text will be used to determin it the item exists

        `:return:` True if the item exists, False otherwise

        """
        self.action_ele.explicit_wait(canvasId)
        self.action_ele.explicit_wait(searchColumnId)
        self.action_ele.clear_input_text(searchColumnId)
        self.action_ele.input_text(searchColumnId, searchText)
        self.action_ele.explicit_wait(canvasId)
        grid_table_row = self._browser.element_finder(canvasId)
        if grid_table_row:
            if columnData and len(columnData) != 0:
                # Get the fields
                columns = grid_table_row.find_elements_by_tag_name('div')
                print("Number of columns: %s" % str(len(columns)))
                test = {int(key):value for key, value in columnData.items()}
                # verify the columns
                if 0 != len(columns):
                    for col, val in test.items():
                        print("passed in col: " + str(col) + " val: " + val + " vs grid " + columns[col].text)
                        print("NOW COMPARE")
                        if columns[col].text != val:
                            print("VALUES DO NOT MATCH")
                            return False
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False


    def select_item_in_grid(self, canvasId, searchColumnId, searchText):
        """
        `Description:` Verify if the specified item exists in the specified grid

        `:canvasId` - the id of the grid (mandatory)
        `:searchColumnId` - the id of the search box to search from (mandatory)
        `:searchText` - the text to search for (mandatory)

        """
        self.action_ele.explicit_wait(searchColumnId)
        self.action_ele.input_text(searchColumnId, searchText)
        self.action_ele.explicit_wait(canvasId)
        grid_table_row = self._browser.element_finder(canvasId)
        if grid_table_row:
            columns = grid_table_row.find_elements_by_tag_name('div')
            if 0 != len(columns):
                columns[1].click()

    def select_multiple_items_in_grid(self, canvasId, searchColumnId, itemsList):
        """
        `Description:` Verify if the specified item exists in the specified grid

        `:canvasId` - the id of the grid (mandatory)
        `:searchColumnId` - the id of the search box to search from (mandatory)
        `:itemsList` - list of the text to search for (mandatory)

        """
        for idx, searchText in enumerate(itemsList):
            self.action_ele.explicit_wait(searchColumnId)
            self.action_ele.input_text(searchColumnId, searchText)
            self.action_ele.explicit_wait(canvasId)
            grid_table_row = self._browser.element_finder(canvasId)
            if grid_table_row:
                columns = grid_table_row.find_elements_by_tag_name('div')
                if 0 != len(columns):
                    columns[1].click()
        self.action_ele.explicit_wait(searchColumnId)
        self.action_ele.clear_input_text(searchColumnId)

    def click_button(self, button_id):
        self.action_ele.explicit_wait(button_id)
        self.action_ele.click_element(button_id)
        return True

    def refresh_browser(self):
        self._browser._browser.refresh()

    def change_phone_pin_and_save(self, pin):
        if (pin == 'default'):
            self.action_ele.explicit_wait('PinUseDefault')
            self.action_ele.select_checkbox('PinUseDefault')
        else:
            self.action_ele.explicit_wait('NewProfilePassword')
            self.action_ele.input_text('NewProfilePassword', pin)
            self.action_ele.explicit_wait('ConfirmProfilePassword')
            self.action_ele.input_text('ConfirmProfilePassword', pin)
        self.action_ele.explicit_wait('changeProfilePasswordFormOK')
        self.action_ele.click_element('changeProfilePasswordFormOK')
        return True

    # verification for now is that the Reset PIN form is no longer displayed
    def verify_phone_pin_change(self, pin):
        try:
            self.action_ele.explicit_wait('ChangePinSuccessOK', 5)
            self.action_ele.click_element('ChangePinSuccessOK')
            status = True
        except Exception as error:
            print(error.message)
            status = False
        return status

    def verify_phone_pin_change_failed(self, message):
        try:
            self.action_ele.explicit_wait('ErrorMessagePhonePin')
            if message in self.query_ele.get_text("ErrorMessagePhonePin"):
                status = True
            else:
                status = False
        except Exception as error:
            print(error.message)
            status = False
        return status


    def switch_page_home_personalContacts(self, params):
        """
        switching to the home - personal contact page
        :return:
        """
        time.sleep(3)
        self.action_ele.mouse_hover('Home_tab')
        time.sleep(5)
        self.action_ele.click_element("personal_contacts_link")
        time.sleep(2)

    def switch_page_home_companyPhonebook(self, params):
        """
        switching to the home - personal contact page
        :return:
        """
        time.sleep(3)
        self.action_ele.mouse_hover('Home_tab')
        time.sleep(5)
        self.action_ele.click_element("company_phonebook_link")
        time.sleep(2)

    def input_text_in_input_field(self, params):
        try:
            self.action_ele.explicit_wait(params['input_id'], 2)
            self.action_ele.input_text(params['input_id'], params['text'])
            time.sleep(1)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def click_element_by_xpath(self, params):
        try:
            self.action_ele.explicit_wait(params['element_xpath'], 2)
            self.action_ele.click_element(params['element_xpath'])
            time.sleep(1)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def select_option_in_select(self, params):
        try:
            self.action_ele.explicit_wait(params['select_id'], 2)
            self.action_ele.select_from_dropdown_using_text(params['select_id'], params['option'])
            time.sleep(1)
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def sleep_in_seconds(self, params):
        try:
            time.sleep(params['sleep_secconds'])
        except Exception, e:
            print(e)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def click_on_phone_system_users(self):
        self.action_ele.click_element("Phone_system_tab")
        self.action_ele.explicit_wait("Users_link")
        self.action_ele.click_element("Users_link")

    def check_it_says(self, option):

        console("select_on_hold_music " + option)
        self._browser._browser.refresh()
        self.action_ele.explicit_wait('on_hold_music_selection')
        text = self.query_ele.get_text("on_hold_music_selection")
        return text == option

    def right_click_link_in_grid(self, gridcontainer, link, context_item):
        '''
        `Description:` click link in grid

        `:param` link: the link which need to click

        '''
        try:
            self.grid = self._browser.element_finder(gridcontainer)
            # self.grid.find_element_by_partial_link_text(link).click()

            linkEle = self.grid.find_element_by_partial_link_text(link)
            action = ActionChains(self._browser._browser)
            action.context_click(linkEle).perform()


            self.action_ele.explicit_wait(context_item)
            self.action_ele.click_element(context_item)

        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def select_tab(self, tab, tab_content):
        self.action_ele.click_element(tab)
        self.action_ele.explicit_wait(tab_content)

    def adjust_voicemail_interation(self, extension):
        try:
            self.action_ele.explicit_wait('CallRoutingTab_NoVM')
            self.action_ele.click_element('CallRoutingTab_NoVM')
            self.action_ele.explicit_wait('CallRoutingTab_ExtensionForward')
            self.action_ele.input_text('CallRoutingTab_ExtensionForward', extension)
            self.action_ele.explicit_wait('CallRoutingTab_Finish')
            self.action_ele.click_element('CallRoutingTab_Finish')
            self.action_ele.explicit_wait('CallRoutingTab_ChangeVoiceMailInteraction')


        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_voicemail_interaction(self, extension):
        try:
            self.action_ele.explicit_wait('CallRoutingTab_ChangeVoiceMailInteraction')
            verify_1 = self.query_ele.text_present('No voicemail greeting recorded')
            verify_2 = self.query_ele.text_present('Callers are not allowed to leave a voicemail')
            verify_3 = self.query_ele.text_present(
                'Callers who press 0 during the voicemail greeting will be forwarded to ' + extension)

            return verify_1 and verify_2 and verify_3

        except Exception as err:
            print(err.message)
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        return False


    def orderID_of_latest_orders(self):
        """
        `Description:` Get order ID of the latest orders

        `:param`

        `:return:`one Order ID

        """
        print("Start orderID_of_latest_orders ")
        # click the OrderID header tab to sort by newest to oldest order.
        self.action_ele.explicit_wait("OrderIDHearderTab")
        self.action_ele.click_element("OrderIDHearderTab")
        self.action_ele.click_element("OrderIDHearderTab")
        grid_table_row = self._browser.element_finder("OrderDataGridCanvas")
        if grid_table_row:
                columns = grid_table_row.find_elements_by_tag_name('div')
        #orderIDs start at colum 3 in the grid
        print("End orderID_of_latest_orders ")
        return columns[3].text

		
    def open_operations_ipPbx_primaryPartition(self):
        """
        `Description:` To open the Profile page in the Operations > IP PBX, Primary Paritiion > Profiles
        """

        self.action_ele.explicit_wait("Operations_tab")
        self.action_ele.click_element("Operations_tab")

        self.action_ele.explicit_wait("Primary_Partition_link")
        self.action_ele.click_element("Primary_Partition_link")

        self.action_ele.explicit_wait("OperationsPrimaryPartitionsProfiles")
        self.action_ele.click_element("OperationsPrimaryPartitionsProfiles")


    def verify_profiles_grid_display(self):
        """
         `Description:` To verify the Profiles grid is displayed.

         :return: True if successful.
        """
        result = False
        self.action_ele.explicit_wait("ProfileDataGridCanvas")
        grid_table = self._browser.element_finder("ProfileDataGridCanvas")
        if grid_table:
            result = True

        return result


    def select_one_profile(self, params):
        """
         `Description:` To verify the Profiles grid is displayed.

         `Param:`  Product type to filter on (eg: Product "Connect CLOUD Standard")

         :return: True if successful.
        """
        result = False
        neededRows = 1
        if self.filter_profiles_product(params['product'], neededRows):

            self.action_ele.explicit_wait("ProfileDataGridCanvas")
            grid_table = self._browser.element_finder("ProfileDataGridCanvas")
            if grid_table:
                rows = grid_table.find_elements_by_class_name('slick-row')
                for row in rows:
                    columns = row.find_elements_by_class_name('slick-cell')
                    for column in columns:

                        if not columns[1].is_selected():
                            columns[1].click()
                            result = True
                            break
                        else:
                            continue
                    break

        return result


    def get_first_record_from_profile(self):
        """
         `Description:` Gets the first profile record. Data is retrieved by iterating the table and extracting
         the data from the ".text" attribute. If elements have data in a child element, then it is not retrieved.
         Enhancement is needed to perform deep retrieval of data.

         :return: A list of data from the first record.
        """
        profileData = []
        self.action_ele.explicit_wait("ProfileDataGridCanvas")
        grid_table = self._browser.element_finder("ProfileDataGridCanvas")
        if grid_table:
            rows = grid_table.find_elements_by_class_name('slick-row')
            if not rows:
                raise Exception("Unable to get rows from Profiles table")
            for row in rows:
                columns = row.find_elements_by_class_name('slick-cell')
                for column in columns:
                    if hasattr(column, 'text'):
                        profileData.append(column.text)
                break

        return profileData


    def verify_reassign_wizard_display(self):
        """
         `Description:` Verify the reassign wizard is displayed

         :return: True if successful.
        """

        result = False
        self.action_ele.explicit_wait("profilesReassignNumberForm")
        profilesReassignForm = self._browser.element_finder("profilesReassignNumberForm")

        if profilesReassignForm:
            result = True

        return result


    def click_reassign_button(self):
        """
         `Description:` Click on ReAssign button

         :return: True if successful.
        """

        # Click on Reassign button
        self.action_ele.explicit_wait("profilesReassignButton")
        reassignButton = self._browser.element_finder("profilesReassignButton")
        reassignButton.click()

        return True


    def validate_reassigned_extension(self, params):
        """
        `Description:` Given an invalid number, validates the number is invalid with the error message.

         :return: True if error validation is successful.
        """
        result = False

        expectedErrorMessage = params['errorMessage']
        extensionNumber = params['extensionNumber']

        self.action_ele.explicit_wait("profilesReassignNewExtensionInputBox")
        self.action_ele.clear_input_text("profilesReassignNewExtensionInputBox")
        self.action_ele.input_text("profilesReassignNewExtensionInputBox", extensionNumber)

        self.action_ele.explicit_wait("profilesReassignNumberFormSaveButton")
        self.action_ele.click_element("profilesReassignNumberFormSaveButton")

        self.action_ele.explicit_wait("profilesReassignNumberNewExtensionErrorMessage")
        disaplayedErrorMessage = self.query_ele.get_text("profilesReassignNumberNewExtensionErrorMessage")

        if expectedErrorMessage in disaplayedErrorMessage:
            result = True

        return result


    def filter_profiles_product(self, product, neededRows):
        """
        `Description:` Filters the Profiles page for a certain product and for a specific number.

        `Param:`  product - Product type to filter on (eg: Product "Connect CLOUD Standard")
        `Param:`  neededRows - Minimum number of records needed for the filtered result.

        `Returns:` True if if the condition is met, otherwise false.
        """

        result = False

        self.action_ele.explicit_wait("ProfilesProductDropdown")
        self.action_ele.select_from_dropdown_using_text("ProfilesProductDropdown", product)
        grid_table = self._browser.element_finder("ProfileDataGridCanvas")
        if grid_table:
            rows = grid_table.find_elements_by_class_name('slick-row')

            if (len(rows) >= neededRows):
                result = True
            else:
                result = False

        return result

    def upload_specified_file(self, params):
        try:
            try:
                import autoit
            except ImportError as e:
                print e.message
            for i in range(5):
                #for clicking the browse button since another control overlaps the button
                ex = self.query_ele._element_finder(params["browseButton"])
                action = webdriver.common.action_chains.ActionChains(self._browser._browser)
                action.move_to_element_with_offset(ex, 5, 5).click().perform()
                time.sleep(5)
                status1 = autoit.win_exists("[TITLE:Open]")
                if status1 == 0:
                    print("click on Browse button failed")
                    print("Retrying number: %s "% str(i))
                else:
                    #Exiting as Open Dialog box has been found
                    print("Exiting as Open Dialog box has been found")
                    break
            else:
                return False
            time.sleep(2) #this is for the path to resolve in the browse window
            autoit.control_send("[TITLE:Open]", "Edit1", params["filePath"])
            time.sleep(1)
            autoit.control_click("[TITLE:Open]", "Button1")
            return True
        except:
            raise AssertionError("Upload of the specified file failed")

    def verify_number(self, param):
        """
        `Description:` Check to see if a number exists

         :return: True if successful.
        """

        result = False;

        if not param:
            console("No value for Number id and Number value")
            return False

        id = param[0]
        value = param[1]
        if not id or not value:
            console("No value for Number id or Number value")
            return False;

        self.action_ele.explicit_wait(id)
        self.action_ele.input_text(id, value)
        grid_table = self._browser.element_finder("ProfileDataGridCanvas")
        if grid_table:
            rows = grid_table.find_elements_by_class_name('slick-row')
            if (len(rows) >= 1):
                result = True

        self.action_ele.clear_input_text(id)

        return result


    def verify_all_column_names_in_Profiles(self):
        """
        `Description:` Gets all the column headings from the Profiles table
         and checks to see if all the column headings are displayed.

        `Returns:` True if all column headings are found, False if the expected columns heading are not found. .
        """
        result = False
        expectedColumnHeaders = ["First Name", "Last Name", "Email", "Extension", "Number", "Product", "Location"]

        try:
            console("Check if Profile table all headers are displayed.")

            self.action_ele.explicit_wait("profileTableColumHeadings")
            columnHeadersElement = self._browser.elements_finder("profileTableColumHeadings")

            if columnHeadersElement:
                columnHeaders = (columnHeadersElement[0].text).split("\n") # get all column heading text from the element.

                # Check if each expected column name is displayed.
                for expectedColumnHeader in expectedColumnHeaders:
                    if expectedColumnHeader in columnHeaders:
                        result = True
                    else:
                        result = False
                        console("Column header " + expectedColumnHeader + " not displayed in Profiles Table")
                        break;

                # If the expected column numbers don't match the displayed column numbers, then error.
                if len(columnHeaders) != len(expectedColumnHeaders):
                    result = False;
                    console("More columns are displayed than expected.")

            else:
                result = False
                console("Empty List, cannot find Profile Columns")

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            console(message)
            result = False
            console("Cannot get Profile Columns")

        return result


    def verify_buttons_enabled_in_Profiles(self, enabledButtonList):
        """
         `Description:` To verify the buttons that are passed in are enabled in the profiles

        `Returns:` True if successful.
        """
        result = False
        expectedEnabledButtons = enabledButtonList

        try:
            console("Check some buttons are enabled in Profile")

            # get a list of buttons that are enabled (by iterating through a list of button elements and querying the attribute).
            enabledButtons = []
            self.action_ele.explicit_wait("profilesAllButtons")
            parentElementForAllButtons = self._browser.elements_finder("profilesAllButtons")
            allButtonElements = parentElementForAllButtons[0].find_elements_by_tag_name("button") #only one element expected.
            for buttonElement in allButtonElements: # From each button element, extract the id attribute and create a list for enalbled buttons.
                disabled = buttonElement.get_attribute('aria-disabled')
                if disabled == "false": # false because we want enabled buttons.
                    if (buttonElement.get_attribute('id') != "partitionProfilesDataGridToggleBtn"): # ignore this? - this seems to be enabled but not visible???
                        enabledButtons.append(buttonElement.get_attribute('id'))

             # compare with the list of button to validate
            for expectedEnabledButton in expectedEnabledButtons:
                if expectedEnabledButton in enabledButtons:
                    result = True
                else:
                    result = False
                    console("Button " + expectedEnabledButton + " not enabled in Profiles Table")
                    break;

             # If the number of expected enabled buttons don't match the number of actual buttons, then error.
            if len(expectedEnabledButtons) != len(enabledButtons):
                result = False
                console("More buttons are displayed than expected.")

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            console(message)
            result = False
            console("Unable to verify default active buttons in Profiles")

        return result


    def select_profile(self, param):
        """
         `Description:` Selects a profile based on the optional product filter passed in.
         :param A map (dictionary) containing the product name and the minimum number of results needed

         :return: True if successful.
        """
        result = False

        try:
            if param:
                if not self.filter_profiles_product(param):
                    console("Product filter failed.")
                    return False

            # Iterate through the table and select the first valid profile.
            self.action_ele.explicit_wait("ProfileDataGridCanvas")
            grid_table = self._browser.element_finder("ProfileDataGridCanvas")
            if grid_table:
                rows = grid_table.find_elements_by_class_name('slick-row')
                for row in rows:
                    columns = row.find_elements_by_class_name('slick-cell')
                    for column in columns:

                        checkbox = (columns[0].find_elements_by_tag_name("input"))[0] # there should only be one element.
                        if (checkbox and (not checkbox.is_selected())):
                            checkbox.click()
                            result = True
                            break
                        else:
                            continue

                    break

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            console(message)
            result = False
            console("Unable to a Profile")

        return result


    def filter_profiles_product(self, product):
        """
        `Description:` Filters a products for a minimum number passed in.

        `Returns:` True if if the confition is met, otherwise false.

        `Created by:` A. Benedict
        """

        result = False
        # Search
        if not product:
            return False;

        productToFilter = product.get("product")
        minNumberOfRecords = int(product.get("minNumber"))

        self.action_ele.explicit_wait("ProfilesProductDropdown")
        self.action_ele.select_from_dropdown_using_text("ProfilesProductDropdown", productToFilter)
        grid_table = self._browser.element_finder("ProfileDataGridCanvas")
        if grid_table:
            rows = grid_table.find_elements_by_class_name('slick-row')

            if (len(rows) >= minNumberOfRecords):
                result = True

        return result

    def Open_Operation_All_Orders(self):
        """
        `Description:` Go to Operation > All Orders

        `Created by:` Okba
        """
        self.action_ele.explicit_wait('Operations_tab')
        self.action_ele.mouse_hover('Operations_tab')
        self.action_ele.explicit_wait("All_Orders_link")
        self.action_ele.click_element("All_Orders_link")