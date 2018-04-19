"""Module for execution of Service Page functionalities
   File: Service.py
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

class Service(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.counter = 15

    def verify_provisioning_details(self, params):
        """
        `Description:` This Function will verify provisioning details of selected service

        `Param:` params: Dictionary contains global user information

        `Returns:` status - True/False

        `Created by:` Megha Bansal
        """

        #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        params = defaultdict(lambda: '', params)

        self.action_ele.explicit_wait("datagrid_servicesExplorerDataGrid")
        if params['servicename']:
            self.action_ele.clear_input_text("headerRow_ServiceName")
            self.action_ele.input_text("headerRow_ServiceName", params['servicename'])
        if params['servicestatus']:
            self.action_ele.select_from_dropdown_using_text("headerRow_ServiceStatus", params['servicestatus'])

        serviceTnName = self.query_ele.get_text("ServiceGrid_Tn")
        self.action_ele.click_element("ServiceGrid_ServiceId_Link")
        self.action_ele.explicit_wait("ServiceDetails_Tabs")

        serviceTn = serviceTnName.split(',', 1)[0]
        isProvisioningDetailsPresent = self.query_ele.text_present("Provisioning Details")

        if params['servicename'].lower() == "global user tn service":
            isPhoneNumberPresent = self.query_ele.text_present("Phone Number")
            isTurnupPresent = self.query_ele.text_present("TN Port or Turnup Service")
            if isProvisioningDetailsPresent and isPhoneNumberPresent and isTurnupPresent:
                return True
            else:
                return False

        elif params['servicename'].lower() == "global user service":
            isUserPresent = self.query_ele.text_present("User")
            isTnPresent = self.query_ele.text_present(serviceTn)
            if isProvisioningDetailsPresent and isUserPresent and isTnPresent:
                return True
            else:
                return False
        else:
            return False


    def close_service(self, params):
        """
        `Description:` This Test case will close the Service from the services page

        `Param:` params: Dictionary contains global user service information

        `:return:` True/False

        `Created by:` Megha Bansal
        """
        params = defaultdict(lambda: '', params)

        #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

        self.action_ele.explicit_wait('ServiceGrid_Checkbox')
        self.action_ele.click_element("headerRow_ServiceName")
        self.action_ele.input_text("headerRow_ServiceName",params['serviceName'])
        time.sleep(1)
        self.action_ele.select_from_dropdown_using_text("headerRow_ServiceStatus", params['serviceStatus'])
        serviceId = self.query_ele.get_text('ServiceGrid_ServiceId_Link')
        self.action_ele.click_element('ServiceGrid_Checkbox')
        self.action_ele.click_element('ServiceGrid_CloseButton')
        time.sleep(1)
        self.action_ele.explicit_wait('confirm_box')
        self.action_ele.click_element("confirm_box")
        self.action_ele.explicit_wait("header_close_service")
        self.action_ele.click_element("close_user_date")
        self.action_ele.input_text('close_user_date', datetime.date.today().strftime('%m/%d/%Y'))
        self.action_ele.click_element("simple_click")

        self.action_ele.click_element("simple_click")
        if params['keepGlobalTn'] == 'no':
            self.action_ele.select_radio_button('keepGlobalTn_no')
        elif params['keepGlobalTn'] == 'yes':
            self.action_ele.select_radio_button('keepGlobalTn_yes')
        self.action_ele.select_from_dropdown_using_index("request_dropdown",1)
        self.action_ele.input_text("case_id",123)

        self.action_ele.click_element("closeServiceWizard_next")
        self.action_ele.click_element("closeServiceWizard_next")
        self.action_ele.click_element("CloseServiceWizard_finish")

        for i in range(self.counter):
            try:
                isDisplayed = self.query_ele.element_displayed("ok_box")
                if isDisplayed:
                    break
                else:
                    time.sleep(5)
            except:
                self._browser._browser.refresh()

        verify_order = self.query_ele.text_present("Order has been created")
        self.action_ele.click_element("ok_box")

        if verify_order != False:
            return True
        else :
            try:
                self.action_ele.explicit_wait('ServiceGrid_Checkbox')
                self.action_ele.click_element('ServiceGrid_ClearFilter')
                self.action_ele.click_element('ServiceGrid_Refresh')
                self.action_ele.explicit_wait('ServiceGrid_Checkbox')
                self.action_ele.input_text('headerRow_ServiceId', serviceId)
                status = self.query_ele.get_text('ServiceGrid_ServiceStatus_Retrieve')

                if status.tolower() == 'closed':
                    return True
                else:
                    self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                    return False

            except Exception:
                print "Service is not closed successfully"
                self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
                return False

    def void_global_user_service(self, params):
        """
        `Description:` This Test case will void the global user service from the services page

        `Param:` params: Dictionary contains global user service information

        `:return:` True/False

        `Created by:` Megha Bansal
        """
        params = defaultdict(lambda: '', params)

        #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

        self.action_ele.explicit_wait('ServiceGrid_Checkbox')
        self.action_ele.click_element("headerRow_ServiceName")
        if params['serviceName']:
            self.action_ele.input_text("headerRow_ServiceName", params['serviceName'])
        time.sleep(1)
        if params['serviceStatus']:
            self.action_ele.select_from_dropdown_using_text("headerRow_ServiceStatus", params['serviceStatus'])
        #serviceId = self.query_ele.get_text('ServiceGrid_ServiceId_Link')

        serviceTnName = self.query_ele.get_text("ServiceGrid_Tn")
        serviceTn = serviceTnName.split(',', 1)[0]
        self.action_ele.click_element('ServiceGrid_ServiceId_Link')
        self.action_ele.explicit_wait('LNP_service_Detail_tab')

        self.action_ele.select_from_dropdown_using_text('LNP_service_status', params['newStatus'])
        time.sleep(1)
        self.action_ele.explicit_wait('Service_Void_Yes')
        self.action_ele.click_element("Service_Void_Yes")
        self.action_ele.explicit_wait("header_void_service")

        self.action_ele.click_element("Void_EffectiveDate")
        self.action_ele.input_text('Void_EffectiveDate', datetime.date.today().strftime('%m/%d/%Y'))
        self.action_ele.click_element("simple_click")

        time.sleep(1)
        if params['keepGlobalTn'] == "no":
            self.action_ele.select_radio_button('Void_keepGlobalTn_no')
        elif params['keepGlobalTn'] == "yes":
            self.action_ele.select_radio_button('Void_keepGlobalTn_yes')

        self.action_ele.select_from_dropdown_using_index("Void_RequestedBy", 1)
        self.action_ele.select_from_dropdown_using_index("Void_RequestSource", 1)

        self.action_ele.click_element("VoidWizard_next")
        self.action_ele.click_element("VoidWizard_finish")

        for i in range(self.counter):
            try:
                isDisplayed = self.query_ele.element_displayed("LNP_ok")
                if isDisplayed:
                    break
                else:
                    time.sleep(5)
            except:
                self._browser._browser.refresh()

        verify_order = self.query_ele.text_present("successfully updated.")
        self.action_ele.click_element("ok_box")

        if verify_order == False:
            return serviceTn, False
        else:
            self.action_ele.explicit_wait('datagrid_servicesExplorerDataGrid')
            return serviceTn, True
