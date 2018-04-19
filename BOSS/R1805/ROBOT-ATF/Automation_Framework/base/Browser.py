###############################################################################
## Module: Browser
## File name: Browser.py
## Description: Browser module contains methods to control & retrieve information from web Browsers
##
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer              Description
##  ---------   ---------      -----------------------
##  16-AUG-2014  VHA              Module created
###############################################################################

#Selenium Modules
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#Python Modules
import time
import sys
import os

#STAF Modules
sys.path.append("../log")
from log import log
sys.path.append("../utils")
from mapMgr import mapMgr

from selenium.common.exceptions import (
    NoSuchAttributeException,
    NoSuchElementException,
    NoSuchFrameException,
    NoSuchWindowException,
    StaleElementReferenceException,
    WebDriverException,
)

sys.path.append("../log")
from log import log

class Browser:
    '''
        Base class for Web Automation uses python selenium Web Driver for this module
    '''
    _DEFAULT_TIMEOUT = 15

    def __init__(self, params):
        #self.browsertype = browser
        #console("BROWSER" + self.browsertype)
        #if self.browsertype in self._BROWSER_INFO.keys():
        #    self._browser = self.create_webdriver(self.browsertype)
        #else:
        #    raise Exception("\nBrowser not supported. Supported browsers: %s\n" %
        #                    self._BROWSER_INFO.keys())

        #self.elements = {
        #    "id": self._browser.find_elements_by_id,
        #    "name": self._browser.find_elements_by_name,
        #    "xpath": self._browser.find_elements_by_xpath,
        #    "tag": self._browser.find_elements_by_tag_name,
        #    "css_class": self._browser.find_elements_by_class_name,
        #   "text": self._browser.find_element_by_link_text
        #}

         self.server=(params["server"]) if "" else "localhost"
         self.port=params["port"]
         print("port is"+ self.port)
         self._browser = None
         self.caps = None
         #cap=DesiredCapabilities()
         if(params["component_type"].lower() == "manhattancomponent"):
             self.browserName = DesiredCapabilities.CHROME
         #Adding new component APPExtentionComponent
         elif(params["component_type"].lower() == "appextensioncomponent"):
             # Install the google app extension
             options = webdriver.ChromeOptions()
             options.add_extension("C:/NodeWebKit/gapps.crx")
             self.caps = options.to_capabilities()
             #print(" elif 1 CAPS is : ", self.caps)

         else:
             self.browserName = DesiredCapabilities.FIREFOX

         print("Freedom from if ....")
         #Added new Ecomponent "appextensioncomponent"
         if params["component_type"].lower() == "appextensioncomponent":
             #print("appextensioncomponent - CAPS is : ")
             self._browser = webdriver.Remote(command_executor='http://'+self.server+':'+self.port+'/wd/hub',
                                 desired_capabilities=self.caps)
             self._browser.get("chrome-extension://hbppcebaaffpmhkdmlamilbnkoipnnej/index.html")
         else:
             self._browser = webdriver.Remote(command_executor='http://'+self.server+':'+self.port+'/wd/hub',
                                       desired_capabilities=self.browserName)

         #self._browser = webdriver.Remote(command_executor='http://'+self.server+':'+self.port+'/wd/hub',cap)
         self.elements = {
                             "id":     self._browser.find_elements_by_id,
                             "name":   self._browser.find_elements_by_name,
                             "xpath":   self._browser.find_elements_by_xpath,
                             "tag":   self._browser.find_elements_by_tag_name,
                             "css_class":  self._browser.find_elements_by_class_name,
                             "text":   self._browser.find_element_by_link_text
                         }
         #self.remoteIp=(params["remoteIp"]) if params["remoteIp"] else '127.0.0.1'
         #self.remote_port=(params["remote_port"]) if params["remote_port"] else '4444'
         #self._browser=webdriver.Remote(
         #                             command_executor="http://"+self.remoteIp+":"+self.remote_port+"/wd/hub",
         #                             desired_capabilities=DesiredCapabilities.CHROME
         #                             )

         self._browser.implicitly_wait(10)
         #log.setLogHandlers()

    def get_current_browser(self):
        return self._browser

    def get_locator(self,by):
        '''
        get_locator() will return element identifier object e.g. find_elements_by_id
        '''
        if by is None:
            log.mjLog.LogReporter("Browser","error","Attribute to identify element is empty")
            return None

        return self.elements[by.lower()]

    def go_to(self, url):
        '''
            go_to() method goes to the specific URL after the browser instance launches
        '''
        self._browser.get(url)

    def get_screenshot_as_file(self, screenshot_file):
        '''
            get_screenshot_as_file() - Gets the screenshot of the current window.
            Returns False if there is any IOError, else returns True.
             Use full paths in your filename.
        '''
        self._browser.get_screenshot_as_file(screenshot_file)


    def get_elements(self, By = None, ByValue = None, index = None):
        '''
            get_elements() api works for multiple web elements Identification
            on web pages
        '''
        try:
            self.By = By
            self.ByValue = ByValue
            if self.By is None or self.ByValue is None:
                log.mjLog.LogReporter("Browser","error","Element by and Element attribute value is empty")
                return None

            #Getting element identifier object
            self.elementObj = self.get_locator(self.By.lower())

            #Returning identified element
            self.elementObjList = self.elementObj(self.ByValue)
            if index is None:
                # print "Index is None, return all elements found"
                return self.elementObjList
            else:
                if index >= len(self.elementObjList):
                    # print "Element index is outside of number of elements found."
                    log.mjLog.LogReporter("Browser","error","Element index is outside of number of elements found")
                    return None
                else:
                    # print "Returning elements at index %d" % index
                    if (not self.elementObjList[index].is_displayed()) or (not self.elementObjList[index].is_enabled()):
                        log.mjLog.LogReporter("Browser","error","The element is found but is not enabled/visible.")
                        return None
                    return self.elementObjList[index]

        except (WebDriverException, NoSuchElementException) as e:
            log.mjLog.LogReporter("Browser","error","Browser.get_elements: Exception: %s" % str(e))


    def get_element(self, By=None, ByValue=None, index = None ):
        '''
            get_element() api works for web element Identification
            on web pages uses get_elements() method and returns single
            element on call
        '''
        try:
            log.mjLog.LogReporter("Browser","debug","Browser.get_elements: By=%s, ByValue=%s" % (By, ByValue))
            if index:
                self.elementRef = self.get_elements(By ,ByValue, index)
            else:
                self.elementRef = self.get_elements(By ,ByValue)

            if len(self.elementRef) == 0:
                raise Exception("0 elements found.")
            elif len(self.elementRef) > 1:
                log.mjLog.LogReporter("Browser","warning",">1 Elements found using : By=%s, ByValue=%s" % (By, ByValue))
                raise AssertionError (">1 element found")
            elif (not self.elementRef[0].is_displayed()) or (not self.elementRef[0].is_enabled()):
                raise Exception("The element is found but is not enabled/visible.")
            else:
                log.mjLog.LogReporter("Browser","debug","Element identified: By=%s, ByValue=%s" % (By, ByValue))
                return self.elementRef[0]
        except (WebDriverException, NoSuchElementException) as e:
            import traceback
            raise AssertionError("Exception occured in element identification. Traceback: %s" % traceback.format_exc())


    def quit(self):
        '''
            Close the Browser
        '''
        try:
            self._browser.quit()
        except:
            import time
            time.sleep(2)
            try:
                self._browser.quit()
            except:
                log.mjLog.LogReporter("Browser","error","Webdriver was not able to close browser.")
                import traceback
                logger.debug(traceback.format_exc())

    def close(self):
        '''
        Close the current browser window
        '''
        try:
            self._browser.close()
        except:
            log.mjLog.LogReporter("Browser","error","Webdriver is not able to close corrent browser.")
            import traceback
            logger.debug(traceback.format_exc())

    def _map_converter(self,locator):
        '''
        map_converter() - Gets element attributes from map files
        Return dictionary
        '''
        self.elementAttr = mapMgr.__getitem__(locator)
        print("The Xpath value is : ",self.elementAttr)
        print("The Xpath Name is  : ",locator)
        return self.elementAttr

    def element_finder(self, locator):
        '''
        element_finder() - locates the element in the web applicatin
        return element object
        '''

        self.elementAttr = self._map_converter(locator)


        if self.elementAttr:
            if len(self.elementAttr.keys()) == 3:
                self.element = self.get_element(By=self.elementAttr["BY_TYPE"], ByValue=self.elementAttr["BY_VALUE"])
            elif len(self.elementAttr.keys()) == 4:
                self.element = self.get_element(By=self.elementAttr["BY_TYPE"], ByValue=self.elementAttr["BY_VALUE"],index=self.elementAttr["INDEX"])
            else:
                log.mjLog.LogReporter("WebUIOperation","error","Element property in map file are not proper  - %s" %(locator))
                raise AssertionError("Element property in map file are not proper  - %s" %(locator))
            return self.element

    def elements_finder(self, locator):
        '''
        elements_finder() - locates multiple elements in the web application
        return element object
        '''

        self.elementAttr = self._map_converter(locator)


        if self.elementAttr:
            if len(self.elementAttr.keys()) == 3:
                self.elementlist = self.get_elements(By=self.elementAttr["BY_TYPE"], ByValue=self.elementAttr["BY_VALUE"])
            elif len(self.elementAttr.keys()) == 4:
                self.elementlist = self.get_elements(By=self.elementAttr["BY_TYPE"], ByValue=self.elementAttr["BY_VALUE"],index=self.elementAttr["INDEX"])
            else:
                log.mjLog.LogReporter("WebUIOperation","error","Element property in map file are not proper  - %s" %(locator))
                raise AssertionError("Element property in map file are not proper  - %s" %(locator))
            return self.elementlist

    def select_item_from_table(self,locator,Search_Item):
        self.varlist=self.elements_finder(locator)
        for item in self.varlist:
            name_list = item.text
            if Search_Item == name_list:
                time.sleep(1)
                item.click()
                break

if __name__ == "__main__":
     browserDict = {"remote": "local"}
     driver = Browser(browserDict)
     driver.go_to("http://www.google.com")
     ElemntRef = driver.get_element(By="name", ByValue="q")
     ElemntRef.send_keys("Vinay")
     time.sleep(2)
     driver.quit()

