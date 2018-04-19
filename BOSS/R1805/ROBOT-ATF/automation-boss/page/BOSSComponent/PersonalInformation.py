"""Module for actions on the Personal Information page"""

import os
import sys
import time
import datetime

#For console logs while executing ROBOT scripts
from robot.api.logger import console
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from collections import defaultdict


sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
import web_wrappers.selenium_wrappers as base

__author__ = "Kenash Kanakaraj"

class PersonalInformation(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.counter = 30

    #go to tab
    def go_to_tab(tab_locator):
        """
        `Description:` Select which tab to locate.

        `:param `tab_locator:

        `:return:`

        `Created by:` Kenash K
        """
        pass

    #Update password
    def change_password(old_pwd, new_pwd, **options):
        """
        `Description:` Change the user password

        `Created by:` Kenash K
        """
        pass

    #get login information
    def get_login_info():
        """
        `Description:` Get the login name and last login time from the personal info page

        `Created by:` Kenash K
        """
        pass

    #get cotact information
    def get_contact_info():
        """
        `Description:` Get the contact information from the personal info page

        `Created by:` Kenash K
        """
        pass

    #get location information
    def get_location_info():
        """
        `Description:` Get location info from the personal info page

        `Created by:` Kenash K
        """
        pass

    #get active service information
    def get_active_service_info(phone_num="", service_type="", act_date=""):
        """
        `Description:  Get the active services

        `Created by:` Kenash K
        """
        pass

    #Delete user (Cannot be automated since the data takes time to reflect in the UI)

    def add_mobility_profile(self, params):
        """
        `Description:` To add mobility profile for a global user via personal information page

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """
        isDisplayed = False
        isGridPresent = False
        params = defaultdict(lambda: '', params)
        self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        self.action_ele.explicit_wait("grid_checkbox_user")
        if params['gu_name']:
            self.action_ele.clear_input_text("grid_Name")
            self.action_ele.input_text("grid_Name", params['gu_name'])

        self.action_ele.click_element("gu_user_link")
        self.action_ele.explicit_wait("personservice_grid")
        self.action_ele.select_from_dropdown_using_index("profile",1)

        for i in range(self.counter):
            try:
                isEnabled = self.query_ele.element_enabled("feature")
                if isEnabled:
                    break
                else:
                    time.sleep(2)
            except:
                self._browser._browser.refresh()

        if params['feature_name']:
            self.action_ele.select_from_dropdown_using_text("feature", params['feature_name'])

        if params['activationDate']:
            if params['activationDate'] == "today":
                cur_date = datetime.date.today()
                self.action_ele.input_text("profile_activationDate", cur_date.strftime('%m/%d/%Y'))
            else:
                self.action_ele.input_text(
                    "profile_activationDate", params['activationDate'])

        self.action_ele.explicit_wait("Requestedby")
        self.action_ele.select_from_dropdown_using_index("Requestedby", 1)

        self.action_ele.explicit_wait("Requestedsources")
        self.action_ele.select_from_dropdown_using_index("Requestedsources", 1)

        self.action_ele.click_element("addButton")
        for i in range(self.counter):
            if "Processing, please wait.." in self._browser._browser.page_source:
                time.sleep(5)
            else:
                try:
                    # import pdb;
                    # pdb.Pdb(stdout=sys.__stdout__).set_trace()

                    isDisplayed = self.query_ele.element_displayed("okButton")
                    if isDisplayed:
                        verify_success = self.query_ele.text_present("Order has been created")
                        if verify_success == False:
                            return verify_success
                        else:
                            self.action_ele.click_element("okButton")
                            self.action_ele.click_element("personservice_refresh")
                            self.action_ele.explicit_wait("personservice_featurepresent")
                            self.action_ele.clear_input_text("personservice_productname")
                            time.sleep(1)
                            self.action_ele.input_text("personservice_productname", params['feature_name'])
                            verify_success = self.query_ele.element_displayed("personservice_featurepresent")
                            return verify_success
                    else:
                        self.action_ele.explicit_wait("personservice_featurepresent")
                        self.action_ele.clear_input_text("personservice_productname")
                        self.action_ele.input_text("personservice_productname", params['feature_name'])
                        verify_success = self.query_ele.element_displayed("personservice_featurepresent")
                        return verify_success

                except Exception, e:
                    print e

    def verify_globaluser_location(self,params):
        """
        `Description:` This Function will verify the location of global user
        `Param:`: Dictionary contains global user information (Name of the user and its country)
        `Returns:` status - True/False
        `Created by:` Megha Bansal
        """
        self.action_ele.explicit_wait("au_datagrid_usersDataGrid")
        self.action_ele.explicit_wait("grid_checkbox_user")
        if params['username']:
            self.action_ele.clear_input_text("grid_Name")
            self.action_ele.input_text("grid_Name", params['username'])

        self.action_ele.click_element("gu_user_link")
        locationPresent = self.query_ele.text_present(params['country'] + "_GlobalLocation_")

        if locationPresent:
            return True
        else:
            return False


