"""This is an updated Browser class that inherites the remote driver version of Browser
"""
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
from log import log

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from robot.api.logger import console

import base

__author__ = "Kenash Kanakaraj"

#todo if the user already has the config for the webdriver enabled then they can use the installed driver

class LocalBrowser(base.Browser):
    _DEFAULT_TIMEOUT = 15
    _BROWSER_INFO = {'firefox': {'webdriver_path': '..\\ext_web_driver\\geckodriver.exe'},
                     'ie': {'webdriver_path': os.path.join(
                         os.path.dirname(os.path.dirname(__file__)),
                         'ext_web_driver', 'IEDriverServer.exe')},
                     'edge': {'webdriver_path': '..\\ext_web_driver\\MicrosoftWebDriver.exe'},
                     #'chrome': {'webdriver_path': '..\\ext_web_driver\\chromedriver.exe'},
                     'chrome': {'webdriver_path': os.path.join(
                         os.path.dirname(os.path.dirname(__file__)),
                         'ext_web_driver', 'chromedriver.exe')},
                     'ghost': {'webdriver_path': os.path.join(
                         os.path.dirname(os.path.dirname(__file__)),
                         'ext_web_driver', 'phantomjs.exe')}}
    _FIREFOX_WIN_DEFAULT_PATH = os.path.join(os.environ["ProgramFiles"], "Mozilla Firefox\\firefox.exe")

    def __init__(self, browser="chrome"):
        self.browsertype = browser
        console("BROWSER: " + self.browsertype)
        if self.browsertype in self._BROWSER_INFO.keys():
            self._browser = self.create_webdriver(self.browsertype)
        else:
            raise Exception("\nBrowser not supported. Supported browsers: %s\n" %
                            self._BROWSER_INFO.keys())

        self.elements = {
            "id": self._browser.find_elements_by_id,
            "name": self._browser.find_elements_by_name,
            "xpath": self._browser.find_elements_by_xpath,
            "tag": self._browser.find_elements_by_tag_name,
            "css_class": self._browser.find_elements_by_class_name,
            "text": self._browser.find_element_by_link_text
        }
        #log.setLogHandlers()

    def create_webdriver(self, browser="chrome"):
        '''Create the webdriver object depending on the browser type

                Args:
                    browser - type of browser. Supported options: chrome, firefox, ie, headless, edge

                Returns:
                    Webdriver(object) depending on the type of the browser
        '''

        if browser == 'firefox':
            try:
                firefoxCap = DesiredCapabilities.FIREFOX
                # we need to explicitly specify to use Marionette
                firefoxCap['marionette'] = True
                # and the path to firefox
                firefoxCap['binary'] = self._FIREFOX_WIN_DEFAULT_PATH

                testdriver = webdriver.Firefox(capabilities=firefoxCap, firefox_binary=FirefoxBinary(
                    self._FIREFOX_WIN_DEFAULT_PATH),
                                               executable_path=self._BROWSER_INFO[browser]['webdriver_path'])
            except Exception as err:
                console(err)

        elif browser == 'ghost':
            testdriver = webdriver.PhantomJS(self._BROWSER_INFO[browser]['webdriver_path'])

        elif browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            testdriver = webdriver.Chrome(self._BROWSER_INFO[browser]['webdriver_path'],
                                                                  chrome_options=chrome_options)

        else:
            testdriver = getattr(webdriver, browser.capitalize())(
                self._BROWSER_INFO[browser]['webdriver_path'])

        testdriver.implicitly_wait(self._DEFAULT_TIMEOUT)
        return testdriver