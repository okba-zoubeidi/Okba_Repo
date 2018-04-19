import os
import sys
import time
from distutils.util import strtobool
from collections import defaultdict
import inspect
from selenium import webdriver
#import autoit
#For console logs while executing ROBOT scripts
from robot.api.logger import console

#TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

#import base
import web_wrappers.selenium_wrappers as base
import log

from CommonFunctionality import CommonFunctionality

__author__ = "Rahul Doshi"




class AddPartition(object):
    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)
        self.commonfunctionality = CommonFunctionality(self._browser)

    def add_partition(self, partition_data):
        '''
        `Description:` Add primary partition

        `Param:` partition_data: Dictionary contains partition information

        `Returns:` None

        `Created by:` rdoshi
        '''
        try:
            self.action_ele.click_element('partitionsGridAddButton')
            partition_data = defaultdict(lambda: '', partition_data)
            self.action_ele.explicit_wait('tbPartitionName')
            self.action_ele.input_text("tbPartitionName", partition_data["partitionName"])
            self.action_ele.select_from_dropdown_using_text("ddlClusters",partition_data["clusterName"])
            if(partition_data["add_sites"]=='True'):
                self.action_ele.select_checkbox("cbAddSites")
            else:
                self.action_ele.unselect_checkbox("cbAddSites")
            self.action_ele.click_element('addPartitionForm_OK')
            #import pdb;
            #pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if self._browser.location == "australia":
                self.action_ele.explicit_wait('Par_localAreaCode')
                self.action_ele.input_text('Par_localAreaCode', partition_data["localAreaCode"])
                self.action_ele.click_element('setLocalAreaCodesForm_OK')
            if self._browser.location == "uk":
                self.action_ele.explicit_wait('Par_localAreaCode')
                self.action_ele.input_text('Par_localAreaCode', partition_data["localAreaCode"])
                self.action_ele.click_element('setLocalAreaCodesForm_OK')
            self.action_ele.explicit_wait('setting_tab_checkbox')
        except Exception,e:
            print(e)
            print("Add Partition Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def verify_partition(self, partitionName):
        """
        `Description:` Verify the partition is created

        `Param:` partitionName:partitionName: to verify

        `Returns:` status - True/False

        `Created by:` Saurabh Singh
        """
        #self.commonfunctionality.switch_link_in_operations("Primary Partition")
        try:
            time.sleep(1)
            self.action_ele.input_text("primary_partition_header",partitionName)
            grid_elements = self._browser.elements_finder("name_grid")
            if grid_elements[0].text == partitionName:
                grid_elements[0].click()
                return True
            else:
                return False
        except Exception,e:
            print(e)
            print("Add Partition Failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)