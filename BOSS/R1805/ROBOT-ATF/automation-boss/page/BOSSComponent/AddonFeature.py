"""Module for execution of Add on Feature functionalities
   File: AddonFeature.py
   Author: Megha Bansal
"""

import os
import sys
import pdb
import time
import imaplib
import time, re
import email
import datetime
from time import gmtime, strftime
from collections import defaultdict
import inspect
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# For console logs while executing ROBOT scripts
from robot.api.logger import console

# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))
# import base
import web_wrappers.selenium_wrappers as base

from log import log
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

__author__ = ""

_RETRY_COUNT = 3


class AddonFeature(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.counter = 10

    def add_globaluser_mobility(self, params):
        """
        `Description:` To add global user to mobility via add on features page

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """

        self.action_ele.explicit_wait("CosmoMobility_Grid")
        self.action_ele.click_element("CosmoMobility_Add")
        self.action_ele.explicit_wait("Add_grid")
        self.action_ele.explicit_wait("Addgrid_checkbox")
        if params['gu_name']:
            self.action_ele.clear_input_text("Addgrid_Name")
            self.action_ele.input_text("Addgrid_Name", params['gu_name'])

        self.action_ele.click_element("Addgrid_checkbox")
        self.action_ele.click_element("Addgrid_Next")
        time.sleep(2)

        self.action_ele.explicit_wait("Summary")
        self.action_ele.explicit_wait("Requestedby")
        self.action_ele.select_from_dropdown_using_index("Requestedby", 1)
        self.action_ele.explicit_wait("Requestedsources")
        self.action_ele.select_from_dropdown_using_index("Requestedsources", 1)
        self.action_ele.click_element("Addgrid_Finish")

        for i in range(self.counter):
            try:
                # okbutton = self._browser.element_finder("Click_Ok")
                # if okbutton.is_displayed():
                isDisplayed = self.query_ele.element_displayed("Click_Ok")
                if isDisplayed:
                    break
                else:
                    time.sleep(5)
            except:
                self._browser._browser.refresh()

        verify_success = self.query_ele.text_present("Mobility has been activated")
        if verify_success == False:
            verify_success = self.query_ele.text_present("Order has been created")
            if verify_success == False:
                return verify_success
            else:
                return True
        else:
            return True
