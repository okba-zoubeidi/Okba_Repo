import os
import sys
import time
import datetime
from distutils.util import strtobool
from collections import defaultdict

#For console logs while executing ROBOT scripts
from robot.api.logger import console

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

#import base
import web_wrappers.selenium_wrappers as base
import log

import inspect
__author__ = "Kenash Kanakaraj"




#login to BOSS portal
class UserHandler(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.hw_info = False

    def add_user(self, params):
        '''
        `Description:` Create user in BOSS portal

        `Param:` params: Dictionary contains user information

        `Returns:` phone_number, extn

        `Created by:` Kenash K
        '''
        try:
            self.hw_info = False
            self.action_ele.explicit_wait('adduser_button')
            self.action_ele.click_element('adduser_button')
            isglobaluser=self.add_contact_info(params)
            phone_number, extn = self.add_phone_info(params)
            if not isglobaluser:
                if self.hw_info:
                    self.add_hardware_info(params)
            self.add_role(params)
            self.add_user_confirm(params)
            self.action_ele.explicit_wait('email_search', 300)
            return phone_number, extn
        except:
            print("Failed to add contact")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_contact_info(self, params):
        '''
        `Description:` Add user for BOSS portal

        `Param:` params: Dictionary contains user information

        `Returns:` global user status - True/False

        `Created by:` Kenash K

        `Modified by:` Tantri Tanisha, Hanumanthu Susmitha
        '''
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("adduser_firstname")
            self.action_ele.input_text('adduser_firstname', params['au_firstname'])
            self.action_ele.input_text('adduser_lastname', params['au_lastname'])
            self.action_ele.input_text('adduser_businessEmail', params['au_businessmail'])
            self.action_ele.input_text('adduser_personalEmail', params['au_personalmail'])
            self.action_ele.select_from_dropdown_using_text('adduser_userLocation', params['au_userlocation'])
            if params['au_userlocation'] in params['global_countries']:
                isglobaluser = True  #its a global user
            else:
                isglobaluser = False #its a normal user
            self.action_ele.select_from_dropdown_using_text('adduser_billingLocation', params['au_location'])
            self.action_ele.input_text('adduser_title', params['au_title'])
            self.action_ele.input_text('adduser_cellPhone', params['au_cellphone'])
            self.action_ele.input_text('adduser_homePhone', params['au_homephone'])
            self.action_ele.select_from_dropdown_using_text('adduser_preferredNotificationEmail',
                                                            params['au_preferrednotificationemail'])
            self.action_ele.select_from_dropdown_using_text('adduser_preferredContactMethod',
                                                            params['au_preferredcontactmethod'])
            self.action_ele.input_text('adduser_userName', params['au_username'])
            self.action_ele.input_text('adduser_password', params['au_password'])
            self.action_ele.input_text('adduser_confirmPassword', params['au_confirmpassword'])
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element('adduser_contactnextbutton')
        except:
            print("Failed to add contact info")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return isglobaluser


    def add_phone_info(self, params):
        '''
        `Description:` Add phone info while adding user for BOSS portal

        `Param:` params: Dictionary contains phone information

        `Returns:` phonenum, extn

        `Created by:` Kenash K
        '''
        try:
            phonenum=''
            extn=''
            params = defaultdict(lambda: '', params)
            if params['ap_phoneloc']:
                self.action_ele.select_from_dropdown_using_text('phone_Location', params['ap_phoneloc'])
            self.action_ele.select_from_dropdown_using_text('phone_Type', params['ap_phonetype'])

            if bool(params['ap_phonenumber']):
                if params['ap_phonetype'] != 'Connect CLOUD Voicemail Only':
                    self.hw_info = True
                else:
                    self.hw_info = False
                if params['ap_phonenumber'] == "random":
                    self.action_ele.select_from_dropdown_using_index('phone_Number',1)
                    phonenum = self.query_ele.get_text_of_selected_dropdown_option('phone_Number')
                else:
                    self.action_ele.select_from_dropdown_using_text('phone_Number', params['ap_phonenumber'])

                if not params['ap_extn']:
                    extn = self.query_ele.get_value('Person_Profile_Extension')
                else:
                    extn = params['ap_extn']

            if bool(params['ap_activationdate']):
                if params['ap_activationdate'] == "today":
                    cur_date = datetime.date.today()
                    self.action_ele.input_text('activationDate', cur_date.strftime('%m/%d/%Y'))
                else:
                    self.action_ele.input_text(
                        'activationDate', params['ap_activationdate'])

            #todo checkbox
            #account_type = params.get('account_type', 'cosmo').lower()
            #if account_type == 'cosmo':
            #    self.select_products_for_users_cosmo(params)
            #else:
            #    self.select_products_for_users(params)
            self.action_ele.click_element("user_label")
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.action_ele.click_element('adduser_contactnextbutton')
            errors = self._browser.elements_finder('user_errors')
            for error in errors:
                if "Extension is in use or not valid." in error.text:
                    extn = error.text.split(':')[-1].strip()
                    self.action_ele.input_text('Person_Profile_Extension', extn)
                    self.action_ele.click_element('adduser_contactnextbutton')

            return phonenum, extn
        except:
            print("Failed to update phone info")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_hardware_info(self, params):
        '''
        `Description:` Add hardware info while adding user for BOSS portal

        `Param:` params: Dictionary contains hardware information

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            params = defaultdict(lambda: '', params)
            if bool(strtobool(params['hw_addhwphone'])):
                self.action_ele.select_checkbox('hw_add')
                self.action_ele.select_from_dropdown_using_text('hw_type', params['hw_type'])
                self.action_ele.select_from_dropdown_using_text('hw_model', params['hw_model'])
                self.action_ele.input_text('hw_ship_date', params['hw_shipdate'])
            if bool(strtobool(params['hw_power'])):
                self.action_ele.select_checkbox('hw_power_supply')
                self.action_ele.select_from_dropdown_using_text('hw_power_supply_type', params['hw_power_type'])
            self.action_ele.click_element('adduser_contactnextbutton')
        except:
            print("Failed to add hardware info")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_role(self, params):
        '''
        `Description:` Add Role of user while adding user for BOSS portal

        `Param1:` params: role: Role of user, scope: Scope of user

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait('availableRoles')
            self.action_ele.select_from_dropdown_using_text('availableRoles', params['role'])
            self.action_ele.explicit_wait('addRoles')
            self.action_ele.click_element('addRoles')
            if params['scope'].lower() == 'location':
                self.action_ele.click_element('loc_scope')
            #self.action_ele.explicit_wait('adduser_contactnextbutton')
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.action_ele.click_element('adduser_contactnextbutton')
        except:
            print("Failed to add user roles")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_user_confirm(self, params):
        '''
        `Description:` To confirm the add user operation

        `Param1:` params: request_by: The person who requested, request_source

        `Returns:` None

        `Created by:` Kenash K
        '''
        try:
            params = defaultdict(lambda: '', params)
            if params['request_by']:
                self.action_ele.select_from_dropdown_using_text('requestedBy', params['request_by'])

            if params['request_source']:
                self.action_ele.select_from_dropdown_using_text('requestSource', params['request_source'])

            if params['request_source'] == 'Case':
                self.action_ele.input_text('caseNumber', params['case_number'])
            self.action_ele.click_element('adduser_finish')
            self.action_ele.explicit_wait('add_user_button1')
            self._browser._browser.execute_script("window.scrollTo(document.body.scrollHeight,0);")
        except:
            print("Failed to complete user confirm")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_user(self, usermailid, role):
        '''
        `Description:` To verify the created user

        `Param:` params: usermailid: email id of user, role: role of user

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            user_role = {'Phone Manager': 'au_isPM', 'Decision Maker': 'au_isDM',
                         'Billing': 'au_isBC', 'Technical': 'au_isTC',
                         'Emergency': 'au_isEC'}
            status = False
            self._browser._browser.refresh()
            time.sleep(3)
            self.action_ele.explicit_wait('email_search')
            self.action_ele.input_text('email_search', usermailid)
            self.action_ele.explicit_wait(user_role[role])
            self.action_ele.select_checkbox(user_role[role])
            for i in range(5):
                try:
                    time.sleep(1)
                    self._browser._browser.refresh()
                    grid_load=self.action_ele.explicit_wait('user_wait_grid')
                    console("iteration number: %s" %i)
                    self._browser._browser.refresh()
                    if grid_load:
                        break
                except:
                    self._browser._browser.refresh()
                    pass
            time.sleep(3)
            #self._browser._browser.refresh()
            self.action_ele.explicit_wait(user_role[role])
            var = self.query_ele.text_present(usermailid)
            self.action_ele.unselect_checkbox(user_role[role])
            self.action_ele.clear_input_text('email_search')

            if usermailid in var:
                status = True
            return status
        except:
            print("Verify user failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

    def verify_user_profile(self, params, **options):
        """
        Verify the user profile
        :param params:  Dictionary contains phone information
        :param options:
        :return:
        """
        status = False
        ph_num = params['ap_phonenumber']
        for c in ['(', ')', ' ', '-', '+']: ph_num = ph_num.replace(c, "")
        time.sleep(3)
        self.action_ele.explicit_wait('headerRow_ProductName')
        self.action_ele.clear_input_text("service_headerRow_OrderId")
        self.action_ele.input_text('headerRow_BaseNameStripped', ph_num)
        self.action_ele.input_text('headerRow_ProductName', params['ap_phonetype'])
        self._browser._browser.refresh()
        time.sleep(3)  #Remove after demo
        self._browser._browser.refresh()
        var = self.query_ele.text_present(params['ap_phonetype'])
        if var:
            status = True
        return status

    def select_products_for_users_cosmo(self,params):
        """
        Select product for Cosmo User
        :param params:  Dictionary contains cosmo user information
        :return:
        """
        divFeatures = self._browser.elements_finder('divBundleLabels')
        labellist = [i.text for i in divFeatures]
        divInputs = self._browser.elements_finder('divBundleInputs')
        featureInputs = params['features_cosmo_bundle'].split(',')
        for featureInput in featureInputs:
            if featureInput in labellist:
                idx = labellist.index(featureInput)
                divInputs[idx].click()
        divFeatures = self._browser.elements_finder('divalacarteLabels')
        labellist = [i.text for i in divFeatures]
        divInputs = self._browser.elements_finder('divalacarteInputs')
        featureInputs = params['features_cosmo_alacarte'].split(',')
        for featureInput in featureInputs:
            if featureInput in labellist:
                idx = labellist.index(featureInput)
                divInputs[idx].click()

    def add_usergroup(self, params):
        """
        `Description:` Add 'User group' from Phone system

        `Param:` params: Dictionary contains User_group Info

        `Returns:` None

        `Created by:` Vasuja
         """
        try:
            self.action_ele.explicit_wait('userGroupGridnew_group_addButton')
            self.action_ele.click_element('userGroupGridnew_group_addButton')
            self.action_ele.input_text('userGroup_Name', params['userGroupName'])
            self.action_ele.select_from_dropdown_using_text('UG_ProfileTypeId', params['profileType'])
            self.action_ele.select_from_dropdown_using_text('UG_HoldMusicId', params['holdMusic'])
            self.action_ele.click_element('UG_groupWizard_next')
            self.action_ele.select_checkbox('UG_AllowCallPickUp')
            self.action_ele.select_checkbox('UG_AllowOverheadPaging')
            self.action_ele.select_checkbox('UG_AllowHuntgroupStateChange')
            self.action_ele.select_checkbox('UG_AllowExtensionAssignment')
            self.action_ele.select_checkbox('UG_ShowCallerId')
            self.action_ele.select_checkbox('UG_ShowCallHistory')
            self.action_ele.select_checkbox('UG_AllowAvailabilityStateChange')
            self.action_ele.select_from_dropdown_using_text('UG_DirectedIntercom', params['directedIntercom'])
            self.action_ele.select_from_dropdown_using_text('UG_WhisperPage', params['whisperPage'])
            self.action_ele.select_from_dropdown_using_text('UG_Barge', params['Barge'])
            self.action_ele.select_from_dropdown_using_text('UG_SilentMonitor', params['silentMonitor'])
            self.action_ele.click_element('UG_groupWizard_next')
            self.action_ele.select_checkbox('UG_AllowVoicemailCallBack')
            self.action_ele.select_checkbox('UG_AllowBroadcastList')
            self.action_ele.select_checkbox('UG_AllowSystemList')
            self.action_ele.select_checkbox('UG_AllowDownloadWav')
            self.action_ele.click_element('UG_groupWizard_next')
            self.action_ele.select_from_dropdown_using_text('UG_ClassofService', params['classOfService'])
            self.action_ele.select_from_dropdown_using_text('UG_AccountCodeMode', params['accountCodeMode'])
            self.action_ele.click_element('UG_groupWizard_finish')

        except:
            console("Failed to add user group")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def assign_usergroup(self, params):
        """
        `Description:` Assign any user in User group

        `Param1:` user mail id

        `Param2:` user Group Name

        `Returns:` None

        `Created by:` Vasuja
         """
        try:
            self.action_ele.explicit_wait('email_search')
            self.action_ele.input_text('email_search', params['usermailid'])
            self.action_ele.click_element('User_phoneName')
            self.action_ele.click_element('User_UserGroup')
            self.action_ele.select_from_dropdown_using_text('User_UserGroup', params['userGroupName'])
            self.action_ele.click_element('User_UserGroup_submit')
        except Exception, e:
            print(e)
            console("Failed to assign user group")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def delete_usergroup(self, user_group_name):
        """
        `Description:` Delete user group from Phone System--> User groups

        `Param1:` user_group_name

        `Returns:` status - True/False

        `Created by:` Vasuja
         """
        try:
            status = False
            self.action_ele.explicit_wait('ug_headerRow_Name')
            self.action_ele.input_text('ug_headerRow_Name', user_group_name)
            if self.query_ele.get_text("ug_name_in_grid") == user_group_name:
                self.action_ele.click_element("ug_checkbox")
                self.action_ele.explicit_wait("ug_delete")
                time.sleep(1)
                self.action_ele.click_element("ug_delete")
                self.action_ele.explicit_wait("ug_delete_yes")
                time.sleep(1)
                self.action_ele.click_element("ug_delete_yes")
                time.sleep(3)
                ug_list = self._browser.elements_finder("ug_list")
                if len(ug_list) == 0:
                    status = True
            self.action_ele.clear_input_text('ug_headerRow_Name')
        except Exception, e:
            print(e)
            print ("Failed to delete User group")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
        return status

    def verify_mobility_checkbox(self, params):
        """
            `Description:` This Function will verify mobility checkbox for a global user if there is smr instance setup for selected country

            `Param:` params: Dictionary contains global user information

            `Returns:` status - True/False

            `Created by:` Megha Bansal
            """

        self.action_ele.explicit_wait('adduser_button')
        self.action_ele.click_element('adduser_button')
        self.add_contact_info(params)

        isDisplayed = self.query_ele.element_displayed("mobilityCheckbox")
        isEnable = self.query_ele.element_enabled("mobilityCheckbox")

        if isDisplayed and isEnable:
            return True
        else:
            return False

    def verify_swap_globaluser(self, params):
        """
        `Description:` This Function will verify swap is disabled for globaluser or not

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """
        self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        self.action_ele.explicit_wait("grid_checkbox_user")
        if params['username']:
            self.action_ele.clear_input_text("grid_Name")
            self.action_ele.input_text("grid_Name", params['username'])

        self.action_ele.right_click("gu_user_link")
        disabledList = self._browser.elements_finder("disabledoption")
        for item in disabledList:
            name_list = item.text
            if name_list == 'Swap':
                return True

        return False

    def get_locations_user_location_dropdown(self):
        """
        `Description:` This Function will verify the User Location dropdown while adding a global user

        `Param:` None

        `Returns: ` result - True/False

        `Created by:` Megha Bansal
        """
        self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        self.action_ele.click_element('adduser_button')
        self.action_ele.explicit_wait("adduser_firstname")

        userLocationList = self._browser.elements_finder('User_Location_dd')
        locList = []
        for i in userLocationList:
            locList.append(i.text)

        self.action_ele.click_element("adduser_cancel")
        time.sleep(1)
        self.action_ele.explicit_wait("confirm_box")
        self.action_ele.click_element("confirm_box")
        return locList