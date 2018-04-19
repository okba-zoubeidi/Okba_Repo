"""Module for actions on the Personal Contacts page"""

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

class PhoneUsers(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def select_call_routing_for_user(self, user_email):
        """
        `Description:` Look for the user whose email address is given then click
                        on the Service/Phone Name column. Then select the
                        Call Routing tab

        `:param params:` Email address of user

        created by:
        """
        try:
            self.action_ele.click_element("Phone_system_tab")
            self.action_ele.click_element("Users_link")

            canvasid = "au_datagrid_usersDataGrid"
            searchcolumnid = "headerRow_BusinessEmail"

            self.action_ele.explicit_wait("headerRow_BusinessEmail")
            self.action_ele.input_text(searchcolumnid, user_email)
            self.action_ele.explicit_wait(canvasid)
            grid_table_row = self._browser.element_finder(canvasid)
            if grid_table_row:
                print grid_table_row

                # It is essential to wait for the element to load, even though we were waiting for the grid to load.
                self.action_ele.explicit_wait("MatchingServicePhoneName")
                elms = self._browser.elements_finder("MatchingServicePhoneName")
                elms[0].click()

                self.action_ele.explicit_wait("CallRouting_tab")
                self.action_ele.click_element("CallRouting_tab")
                return True

        except:
            raise AssertionError("Navigation Failed!!")

    def click_on_configure_main_settings(self, **params):
        """
        `Description:` Click on Configure Main Settings

        `:param params:`

        created by:
        """
        try:
            self.action_ele.explicit_wait("configureMainSettingsButtonId")

            matching_xpath = "configureMainSettingsButton"
            matching_buttons = self._browser.elements_finder(matching_xpath)
            if matching_buttons:
                print matching_buttons

                search_item = "Configure Main Settings"
                for button in matching_buttons:
                    name_list = button.text
                    if search_item == name_list:
                        time.sleep(1)
                        button.click()
                        return True
            return False

        except:
            raise AssertionError("Navigation Failed!!")

    def click_on_configure_phones_add(self, **params):
        """
        `Description:` Click on Configure Phones -> Add

        `:param params:`

        created by:
        """
        try:
            self.action_ele.explicit_wait("callRoutingAddNumbersHeader")

            matching_xpath = "configureMainSettingsButton"
            matching_buttons = self._browser.elements_finder(matching_xpath)
            if matching_buttons:
                print matching_buttons

                search_item = "Add"
                for button in matching_buttons:
                    name_list = button.text
                    if search_item == name_list:
                        time.sleep(1)
                        button.click()
                        return True
            return False

        except:
            raise AssertionError("Navigation Failed!!")

    def add_phone_for_call_routing(self, phone_number):
        """
        `Description:` Add phone to call routing

        `:param params:`

        created by:
        """
        try:
            self.action_ele.explicit_wait("tblCallRoutingNumbers")
            self.action_ele.input_text("configurePhoneCallRoutingAddLabel", phone_number)
            self.action_ele.input_text("configurePhoneCallRoutingAddPhoneNumber", phone_number)

            # Click on "Press 1 to connect"
            self.action_ele.click_element('configurePhoneCallRoutingPressOne')

            # Click on Finish
            self.action_ele.click_element('callRoutingSettingsWizard_finish')
            return True

        except:
            raise AssertionError("Navigation Failed!!")

    def add_second_phone_for_call_routing(self, phone_number):
        """
        `Description:` Add second phone to call routing

        `:param params:`

        created by:
        """
        try:
            self.action_ele.explicit_wait("tblCallRoutingNumbers")
            self.action_ele.input_text("configurePhoneCallRoutingAddLabel2", phone_number)
            self.action_ele.input_text("configurePhoneCallRoutingAddPhoneNumber2", phone_number)

            # Click on "Press 1 to connect"
            self.action_ele.click_element('configurePhoneCallRoutingPressOne2')

            # Click on Finish
            self.action_ele.click_element('callRoutingSettingsWizard_finish')
            return True

        except:
            raise AssertionError("Navigation Failed!!")

    def add_phone_to_call_routing(self, phone_number, phone_index):
        try:
            result = self.click_on_configure_main_settings()
            if not result:
                return result

            result = self.click_on_configure_phones_add()
            if not result:
                return result

            if phone_index == "first":
                result = self.add_phone_for_call_routing(phone_number)
            else:
                result = self.add_second_phone_for_call_routing(phone_number)
            if not result:
                return result

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def configure_call_routing_options(self, **params):
        """
        `Description:` Add phones to Call Routing.
        They have to be added one at the time, otherwise it would fail even when adding them manually. It seems like a bug in BOSS.
        It would be nice to create new users first and then add their phone numbers, rather than hard-coding extension numbers.

        `:param params:`

        created by:
        """
        try:
            result = self.add_phone_to_call_routing("4001", "first")
            if not result:
                return result

            time.sleep(3)
            result = self.add_phone_to_call_routing("4002", "second")
            if not result:
                return result

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def find_and_click_matching_element(self, xpath, search_item):
        try:
            matching_buttons = self._browser.elements_finder(xpath)
            if matching_buttons:
                print matching_buttons

                for button in matching_buttons:
                    name_list = button.text
                    if search_item == name_list:
                        time.sleep(1)
                        button.click()
                        return True
            return False
        except:
            raise AssertionError("Failed to find matching element!!")

    def configure_always_forward_to_voicemail(self):
        """
        `Description:`

        `:param params:

        created by: vuh
        """
        try:
            # Click on Find Me change button
            self.action_ele.explicit_wait("configureMainSettingsButtonId")
            self.action_ele.click_element('changeVoicemail')

            # Click on "Always forward my calls to" radio button
            element = self._browser.element_finder("alwaysForwardRadio")
            if element:
                element.click()
            else:
                return False

            # Select forwarding option
            self.action_ele.select_from_dropdown_using_text('alwaysForwardOptions', "voicemail")

            # click on Finish
            self.action_ele.click_element('availabilityRoutingWizard_finish')

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def always_forward_to_voicemail_configured(self):
        """
        `Description:` Check to see if always forward to voicemail has been configured

        `:param params:

        created by: vuh
        """
        try:
            # Click on Find Me change button
            self.action_ele.explicit_wait("availabilityRouting-content")
            time.sleep(3)
            self.action_ele.click_element('changeVoicemail')

            # Check if "Forward the call to" radio button is checked
            self.action_ele.explicit_wait("alwaysForwardRadio")
            element = self._browser.element_finder("alwaysForwardRadio")
            if element and not element.is_selected():
                console("Always forward was not selected")
                return False

            # Check voicemail option
            element = self._browser.element_finder("alwaysForwardOptions")
            if element and element.get_attribute('value') != "0": # voicemail value
                return False

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def configure_call_forwarding(self, **params):
        """
        `Description:`

        `:param params:

        created by: V Milutinovic
        """
        try:
            # Click on Find Me change button
            self.action_ele.explicit_wait("configureMainSettingsButtonId")
            self.action_ele.click_element('changeFindMe')

            # Click on Call Forwarding button
            self.action_ele.explicit_wait("availabilityRoutingWizard")
            result = self.find_and_click_matching_element("callRoutingButtons", "Call Forwarding")
            if not result:
                return result

            # Click on "Forward the call to" radio button
            element = self._browser.element_finder("forwardTheCallTo")
            if element:
                element.click()
            else:
                return False

            # Select voicemail option
            self.action_ele.select_from_dropdown_using_text('forwardTheCallToOptions', "voicemail")
            # select number of rings
            self.action_ele.select_from_dropdown_using_text('ringsBeforeForwarding', "5")
            # and if more than 8 calls forward to
            self.action_ele.select_from_dropdown_using_text('ifMoreThan8CallsForwardTo', "voicemail")

            # click on Finish
            self.action_ele.click_element('availabilityRoutingWizard_finish')

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def call_forwarding_configured(self, **params):
        """
        `Description:`

        `:param params:

        created by: V Milutinovic
        """
        try:
            # Click on Find Me change button
            self.action_ele.explicit_wait("availabilityRouting-content")
            time.sleep(3)
            self.action_ele.click_element('changeFindMe')

            # Click on Call Forwarding button
            self.action_ele.explicit_wait("availabilityRoutingWizard")
            result = self.find_and_click_matching_element("callRoutingButtons", "Call Forwarding")
            if not result:
                console("failed to click on Call Forwarding option")
                return result

            # Check if "Forward the call to" radio button is checked
            self.action_ele.explicit_wait("forwardTheCallTo")
            element = self._browser.element_finder("forwardTheCallTo")
            if element and not element.is_selected():
                console("failed to click on Call Forwarding option")
                return False

            # Check voicemail option
            element = self._browser.element_finder("forwardTheCallToOptions")
            if element and element.get_attribute('value') != "0": # voicemail value
                return False

            # Check number of rings
            element = self._browser.element_finder("ringsBeforeForwarding")
            if element and element.get_attribute('value') != "4":
                return False

            # # and if more than 8 calls forward to
            # self.action_ele.select_from_dropdown_using_text('ifMoreThan8CallsForwardTo', "voicemail")
            element = self._browser.element_finder("ifMoreThan8CallsForwardTo")
            if element and element.get_attribute('value') != "0": # voicemail value
                return False

            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def configure_find_me_numbers(self, **params):
        """
        `Description:` Configure Find Me numbers that will be used sequentially

        `:param params:`

        created by:
        """
        try:
            time.sleep(3)
            result = self.click_on_configure_main_settings()
            if not result:
                return result

            # Click on Next button
            nextButtonId = "callRoutingSettingsWizard_next"
            self.action_ele.explicit_wait(nextButtonId)
            self.action_ele.click_element(nextButtonId)

            # Click on next again in new window
            self.action_ele.explicit_wait("cosmoCallRoutingSimRingContainer")
            self.action_ele.click_element(nextButtonId)

            # click on "Ring my Find Me numbers sequentially before playing my voicemail"
            self.action_ele.explicit_wait("cosmoCallRoutingFindMeContainer")
            result = self.find_and_click_matching_element("ringMyFindMeNumbers", "Ring my Find Me numbers sequentially before playing my voicemail")
            if not result:
                return result

            # click on "Prompt the caller to record their name if caller ID is not available"
            self.action_ele.select_checkbox("promptCallerToRecordName")

            # Enter My Find Me numbers
            self.action_ele.select_from_dropdown_using_text('myFindMeNumber1', "4001 - Press 1 to connect - Try for 3 rings")
            self.action_ele.select_from_dropdown_using_text('myFindMeNumber2', "4002 - Press 1 to connect - Try for 3 rings")

            # Click on Finish
            self.action_ele.click_element('callRoutingSettingsWizard_finish')

            time.sleep(3)
            return True
        except:
            raise AssertionError("Navigation Failed!!")

    def select_selected_call_routing_for_user(self, user_email):
        """
        `Description:` In this case the user is already selected

        `:param params:` Email address of user

        created by:
        """
        try:
            self.action_ele.click_element("Phone_system_tab")
            self.action_ele.click_element("Users_link")

            canvasid = "au_datagrid_usersDataGrid"
            searchcolumnid = "headerRow_BusinessEmail"

            self.action_ele.explicit_wait("headerRow_BusinessEmail")
            self.action_ele.input_text(searchcolumnid, user_email)
            self.action_ele.explicit_wait(canvasid)
            grid_table_row = self._browser.element_finder(canvasid)
            if grid_table_row:
                print grid_table_row

                self.action_ele.explicit_wait("SelectedMatchingServicePhoneName")
                elms = self._browser.elements_finder("SelectedMatchingServicePhoneName")
                elms[0].click()

                self.action_ele.explicit_wait("CallRouting_tab")
                self.action_ele.click_element("CallRouting_tab")
                return True

        except:
            raise AssertionError("Navigation Failed!!")

    def find_me_numbers_configured(self, **params):
        """
        `Description:` To verify Find Me Numbers are configured

        `:param params:

        created by: V Milutinovic
        """
        try:
            # The changes are not refreshed in the form after changing routing settings.
            # Need to open call routing for the user again by walking through few menus to refresh content.
            self.select_selected_call_routing_for_user("auser1@shoretel.com")
            self.click_on_configure_main_settings()

            self.action_ele.explicit_wait("availabilityRouting-content")
            time.sleep(3)

            # Check if "Forward the call to" radio button is checked
            self.action_ele.explicit_wait("findMeNumbersSettings")
            element = self._browser.element_finder("findMeNumbersSettings")
            if element:
                console("element" + element.text)

            text = element.text
            do_not_pick_up = "pick up, ring these numbers sequentially"
            if do_not_pick_up not in element.text:
                return False
            if "4001" not in element.text:
                return False
            if "4002" not in element.text:
                return False

            return True
        except:
            raise AssertionError("Navigation Failed!!")



