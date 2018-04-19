"""Module for creating and verifying Emergency hunt group
   File: VCFEHandler.py
   Author: Rahul
"""

import os
import sys
import time
from distutils.util import strtobool
from collections import defaultdict

from selenium import webdriver
#For console logs while executing ROBOT scripts
from robot.api.logger import console


#import base
import web_wrappers.selenium_wrappers as base
import log

from CommonFunctionality import CommonFunctionality
__author__ = "Rahul"





#login to BOSS portal
class ProgButtonHandler(object):
    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.common_functionality = CommonFunctionality(self._browser)

    def add_programmable_buttons(self,params):
        """
        `Description:` For adding program buttons handler

        `:param` params:  Dictionary contains programmable button information

        `:return:`

        `Created by:` Kenash K
        """
        self.common_functionality.switch_page_users()
        #self.common_functionality.search_user(params['user_email'])
        self.action_ele.input_text('email_search', params['user_email'])
        #element = self._browser.elements_finder(mapDict['user_phone_settings']["BY_VALUE"] + "//*")
        self.action_ele.click_element('user_phone_settings')
        self.action_ele.click_element('user_prog_button')

        #TODO Add programmable button by number
        if(params['function']=="Silent Coach"):
            self.action_ele.explicit_wait('user_silent_coach')
            self.action_ele.click_element('user_silent_coach')
        else:
            self.action_ele.explicit_wait('user_silent_coach')
            self.action_ele.click_element('user_silent_coach')
        self.action_ele.explicit_wait('user_select_prog_button_function')
        self.action_ele.select_from_dropdown_using_text('user_select_prog_button_function',
                                                        params['function'])
        self.action_ele.input_text('user_prog_button_long_label',
                                   params['longlabel'])
        self.action_ele.input_text('user_prog_button_short_label',
                                   params['shortlabel'])
        self.action_ele.input_text('user_select_prog_button_extension',
                                   params['extension'])
        self.action_ele.explicit_wait('user_prog_button_save')
        self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.action_ele.click_element('user_prog_button_save')
        time.sleep(2)
        self.action_ele.explicit_wait("fnMessageBox_OK")
        time.sleep(1)
        self.action_ele.click_element("fnMessageBox_OK")






