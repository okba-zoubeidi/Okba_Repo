"""Module for handling account functionalities such as Add user, Add Contract etc
   File: AccountHandler.py
   Author: Kenash Kanakaraj
"""

import os
import sys
import time
import datetime
from distutils.util import strtobool
from collections import defaultdict

from selenium import webdriver

#For console logs while executing ROBOT scripts
from robot.api.logger import console

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

import web_wrappers.selenium_wrappers as base
import log
import CommonFunctionality

import inspect

__author__ = "Kenash Kanakaraj"




#login to BOSS portal
class AccountHandler(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    def verify_contract_state(self, accountName, exp_state):
        '''
        `Description:` Verify the contract state

        `Param1:` params: accountName: Name of account

        `Param2:` params: exp_state: State of account

        `Returns:` status - True/False

        `Created by:` Kenash K
        '''
        try:
            status = False
            self.action_ele.explicit_wait('cp_allContractsbtnRefresh',60)
            self.action_ele.click_element('cp_allContractsbtnRefresh')
            self.action_ele.explicit_wait('cp_headerRow_AccountName')
            self.action_ele.input_text('cp_headerRow_AccountName', accountName)
            time.sleep(3)   #time for the table to come up
            var = self.query_ele.text_present(exp_state)
            console(var)
            if var:
                status = True
            return status
        except AssertionError, e:
            print(e)
            print("Verify Contract failed")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return status

    def add_contract(self, params):
        """
        `Description:` To add contract. This method can run on windows only due to dependency on
        "autoit" package.

        `Param:` params: Dictionary contains contract information

        `Returns:` contract_state

        `Created by:` Kenash K
        """
        try:
            contract_state = False
            self.action_ele.click_element("ac_addcontract")
            self.add_account_for_contract(params)
            self.add_locations(params)
            self.add_products(params)

            contract_state = self.add_terms(params)
            return contract_state
        except AssertionError, e:
            print(e)
            print("Failed to add contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return contract_state

    def add_account_for_contract(self, params):
        """
        `Description:` To add account for contract

        `Param:` params: Dictionary contains account information

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.explicit_wait("ac_type")
            self.action_ele.select_from_dropdown_using_text("ac_type", params["accountType"])
            self.action_ele.input_text("ac_companyName", params["accountName"])
            self.action_ele.select_from_dropdown_using_text("ac_salesPerson", params["salesPerson"])
            self.action_ele.select_from_dropdown_using_text("ac_partnerType", params["partnerType"])
            self.action_ele.select_from_dropdown_using_text("ac_platformType", params["platformType"])
            self.action_ele.select_from_dropdown_using_text("ac_country1", params["country"])
            self.action_ele.select_from_dropdown_using_text("ac_currency", params["currency"])
            self.action_ele.input_text("ac_firstName", params["firstName"])
            self.action_ele.input_text("ac_lastName", params["lastName"])
            self.action_ele.input_text("ac_password", params["password"])
            self.action_ele.input_text("ac_passwordConfirm", params["confirmPassword"])
            self.action_ele.input_text("ac_email", params["email"])
            self.action_ele.input_text("ac_password", params["password"])
            #self.action_ele.input_text("ac_passwordConfirm", params["passwordConfirm"])
            self.action_ele.click_element("ac_nextbut_0")
        except Exception, e:
            print(e)
            print("Failed to add account for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_locations(self, params):
        """
        `Description:` To add location detail

        `Param:` params: Dictionary contains location information

        `Returns:` None

        `Created by:` Kenash K

        `Modified by :` Vasuja K
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("ac_addLocation")
            self.action_ele.input_text("ac_locationName", params["locationName"])
            self.action_ele.select_from_dropdown_using_text("ac_country2", params["Country"])
            if params['country'] == 'Australia':
                self.add_location_australia(params)
            if params['country']=='United States':
                self.add_location_united_states(params)
            if params['country']=='United Kingdom':
                self.add_location_united_kingdom(params)
            self.action_ele.input_text("ac_city", params["city"])
            self.action_ele.input_text("ac_zip", params["zip"])
            if params["no_validation"] == 'True':
                self.action_ele.select_checkbox("ac_validate")
            else:
                self.action_ele.unselect_checkbox("ac_validate")
            self.action_ele.click_element("ac_addlocationformok")
            self.action_ele.select_from_dropdown_using_text("ac_connectivity",
                                                            params["connectivity"])
            self.action_ele.click_element("ac_nextbut_1")
        except Exception, e:
            print(e)
            print("Failed to add location for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_location_australia(self, params):
        """
        `Description:` To add location details for Country Australia

        `Param:` params: Dictionary contains location information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.action_ele.input_text("ac_SubPremises", params["streetNo"])
            self.action_ele.input_text("ac_Address6", params["streetName"])
            self.action_ele.select_from_dropdown_using_text("ac_Address7", params["streetType"])
            self.action_ele.select_from_dropdown_using_text("ac_state", params["state"])
            self.action_ele.input_text("ac_ER_firstName", params["locfirstName"])
            self.action_ele.input_text("ac_ER_LastName", params["loclastName"])
            self.action_ele.input_text("ac_ER_PhoneNumber", params["phoneNumber"])
        except:
            print("Failed to add location with respect to Australia while creating contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_location_united_states(self, params):
        """
        `Description:` To add location details for Country US

        `Param:` params: Dictionary contains location information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.action_ele.input_text("ac_address1", params["Address1"])
            self.action_ele.input_text("ac_address2", params["Address2"])
            self.action_ele.select_from_dropdown_using_text("ac_state", params["state"])
        except:
            print("Failed to add location with respect to United States while creating contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_location_united_kingdom(self, params):
        """
        `Description:` To add location details for Country UK

        `Param:` params: Dictionary contains location information

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.action_ele.input_text("ac_address2", params["buildingName"])
            self.action_ele.input_text("ac_address1", params["streetName"])
        except:
            print("Failed to add location with respect to United kingdom while creating contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_products(self, params):
        """
        `Description:` To add products

        `Param:` params: Dictionary contains products information

        `Returns:` None

        `Created by:` Kenash K
        """
        try:
            params = defaultdict(lambda: '', params)
            self.action_ele.click_element("ac_addProducts")
            self.action_ele.select_from_dropdown_using_text("ac_class", params["class"])
            self.action_ele.select_from_dropdown_using_text("ac_Product", params["product"])
            self.action_ele.input_text("ac_Quantity", params["quantity"])
            self.action_ele.select_from_dropdown_using_text("ac_location", params["location"])
            self.action_ele.input_text("ac_MRR", params["MRR"])
            self.action_ele.input_text("ac_NRR", params["NRR"])
            if params["waiveNRR"] == 'True':
                self.action_ele.select_checkbox("ac_waiveNRR")
            #self.action_ele.click_element("ac_addProducts")
            #self.action_ele.select_from_dropdown_using_text("ac_class01", params["class01"])
            #self.action_ele.select_from_dropdown_using_text("ac_Product01", params["product01"])
            #self.action_ele.input_text("ac_Quantity01", params["quantity01"])
            #self.action_ele.select_from_dropdown_using_text("ac_location01", params["location01"])
            #self.action_ele.input_text("ac_MRR01", params["MRR01"])
            #self.action_ele.input_text("ac_NRR01", params["NRR01"])
            #if params["waiveNRR01"] == 'True':
            #    self.action_ele.select_checkbox("ac_waiveNRR01")
            self.action_ele.click_element("ac_nextbut_2")
        except Exception, e:
            print(e)
            print("Failed to add product for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_terms(self, params):
        """
        `Description:` To add terms

        `Param:` params: ictionary contains terms information

        `Returns:` contract_state

        `Created by:` Kenash K
        """
        try:
            try:
                import autoit
            except ImportError as e:
                print e.msg
            verify_text = ''
            contract_state = False
            params = defaultdict(lambda: '', params)
            self.action_ele.input_text("ac_contractNumber", params["contractNumber"])
            #self.action_ele.input_text("ac_forecastDate", params["forecastDate"])
            if bool(params['forecastDate']):
                if params['forecastDate'] == "today":
                    cur_date = datetime.date.today()
                    self.action_ele.input_text('ac_forecastDate', cur_date.strftime('%m/%d/%Y'))
                else:
                    self.action_ele.input_text(
                        'ac_forecastDate', params['forecastDate'])

            self.action_ele.input_text("ac_notes", params["notes"])
            self.action_ele.click_element("ac_uploadContract")
            for i in range(5):
                #for clicking the browse button since another control overlaps the button
                ex = self.query_ele._element_finder("ac_uploadFile1")
                action = webdriver.common.action_chains.ActionChains(self._browser._browser)
                action.move_to_element_with_offset(ex, 5, 5).click().perform()
                time.sleep(5)
                #autoit.win_wait_active("[TITLE:Open]", 5)
                #status1 = autoit.win_active("[CLASS:#32770]")
                status1 = autoit.win_exists("[TITLE:Open]")
                #status1=1
                console(status1)
                if status1 == 0:
                    print("click on browse failed")
                    print("Retrying number: %s "% str(i))
                else:
                    #Exiting as Open Dialog box has been found
                    print("Exiting as Open Dialog box has been found")
                    break
            else:
                print("Raising Exception")
                raise
            time.sleep(2) #this is for the path to resolve in the browse window
            autoit.control_send("[TITLE:Open]", "Edit1", params["filePath"])
            time.sleep(1)
            autoit.control_click("[TITLE:Open]", "Button1")
            #autoit.send(params["filePath"])
            #time.sleep(2)
            #autoit.send("{ENTER}")
            self.action_ele.explicit_wait("ac_Ok")
            time.sleep(2)
            self.action_ele.click_element("ac_Ok")

            self.action_ele.select_from_dropdown_using_text("ac_termVersion", params["termVersion"])
            self.action_ele.select_from_dropdown_using_text("ac_termLength", params["termLength"])
            self.action_ele.select_from_dropdown_using_text("ac_termRenewalType", params["termRenewalType"])
            self.action_ele.select_from_dropdown_using_text("ac_termInstall", params["termInstall"])
            self.action_ele.click_element("ac_nextbut_3")
            #self.action_ele.explicit_wait("ac_finish")
            time.sleep(2)
            self.action_ele.click_element("ac_finish")
            self.action_ele.explicit_wait("ac_alert_ok", 120)
            verify_text = self.query_ele.text_present("New Contract successfully added")
            time.sleep(2)
            self.action_ele.click_element("ac_alert_ok")
            ##contract_message = self.query_ele.get_text('contract_alert_message')
            if verify_text:
                contract_state = True
            #self.action_ele.explicit_wait("ac_accountContractsDataGridAddContract", 20)  #remove exta wait to load grid uncomment if page is very slow
            return contract_state
        except Exception,e:
            print(e)
            print("Failed to add product for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)
            return False

    def confirm_contract(self, instance, location):
        """
        `Description:` To confirm the added contract

        `Param1:' instance: Instance of contact

        `Param2:' location:  Location for which contract is created

        `Returns:` order_number

        `Created by:` Kenash K
        """
        confirm_state = False
        verify_msg = ''
        try:
            self.add_instance(instance)
            time.sleep(2)
            self._browser._browser.refresh()
            self.action_ele.select_from_dropdown_using_text('cf_ContractBillingLocationId', location)
            self.action_ele.explicit_wait('contract_alert_ok')
            self.action_ele.click_element('contract_alert_ok')

            time.sleep(2)
            self._browser._browser.refresh()

            self.action_ele.explicit_wait('cf_btnConfirmContract')
            time.sleep(2)
            self.action_ele.click_element('cf_btnConfirmContract')

            if self._browser.location == "australia":
                self.action_ele.explicit_wait('Par_localAreaCode')
                time.sleep(1)
                self.action_ele.input_text('Par_localAreaCode', 2)
                self.action_ele.click_element('setLocalAreaCodesForm_OK')
            if self._browser.location == "uk":
                self.action_ele.explicit_wait('Par_localAreaCode')
                time.sleep(1)
                self.action_ele.input_text('Par_localAreaCode', 28)
                self.action_ele.click_element('setLocalAreaCodesForm_OK')

            #confirmation of proceeding
            self.action_ele.explicit_wait('contract_alert_ok')
            time.sleep(2)
            self.action_ele.click_element("contract_alert_ok")

            #wait for contract confirmation
            self.action_ele.explicit_wait('contract_alert_ok', 300)
            print("Clicked Confirm OK")
            time.sleep(2)
            #contract_message = self.query_ele.get_text('contract_alert_message')
            verify_msg = self.query_ele.text_present("Order has been created")

            if verify_msg:
                time.sleep(2)
                print("Message found: %s" %verify_msg)
                confirm_message = self.query_ele.get_text("ac_confirm_message")
                order_number = confirm_message.split("#")[-1]
                print(order_number)
                self.action_ele.click_element("contract_alert_ok")
                self._browser._browser.refresh()
                confirm_msg = self.query_ele.text_present("Confirmed")
                if confirm_msg:
                    confirm_state = True
            else:
                print("Message not found")
                time.sleep(1)
                self.action_ele.click_element("contract_alert_ok")
                self._browser._browser.refresh()

            return order_number

        except Exception, e:
            print(e)
            print("Failed to confirm contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def add_instance(self, instance_name):
        """
        To add instace
        :param instance_name: Name of instance
        :return:
        """
        try:
            self.action_ele.click_element('cf_clustersLink')
            self.action_ele.explicit_wait('ai_editClustersAddButton')
            self.action_ele.click_element('ai_editClustersAddButton')
            self.action_ele.explicit_wait('ai_ClusterId')

            self.action_ele.select_from_dropdown_using_text('ai_ClusterId', instance_name)
            time.sleep(1)
            self.action_ele.click_element('ai_addClusterForm_OK')
            #wait for instance checkbox to appear
            self.action_ele.click_element('ai_clustersForm_Close')

        except Exception, e:
            print(e)
            print("Failed to add product for contract")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def set_location_as_site(self):
        """
        `Description:` This function will set the location as Site

        `Param:` None

        `Returns:` None

        `Created by:` Vasuja K
        """
        try:
            self.action_ele.explicit_wait("site_checkbox")
            self.action_ele.click_element("site_checkbox")
            print("Checked site checkbox")
            time.sleep(2)    #for the site to be marked on UI
            self.action_ele.explicit_wait("ok_btnPartitionSitesOk")
            print("Clicking Ok button to set default location as site")
            self._browser._browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.action_ele.click_element("ok_btnPartitionSitesOk")
            self.action_ele.explicit_wait("site_checkbox")
            time.sleep(5)   #processing window appears
            for counter in range(20):
                if "Processing, please wait" in self._browser._browser.page_source:
                    print("Waiting for processing..!!!")
                    time.sleep(2)
                else:
                    break
            self.action_ele.explicit_wait("ok_btnPartitionSitesOk", 120)
            self.action_ele.explicit_wait("site_checkbox", 120)
            self.action_ele.explicit_wait("Phone_system_tab")
        except Exception, e:
            print(e)
            print("Failed to set default location as a site")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

    def modify_service_status(self, params):
        """
        To modify the service status.
        :param params: Dictionary contains service modify information
        :return:
        """
        try:
            self.action_ele.explicit_wait('service_headerRow_OrderId')
            self.action_ele.input_text("service_headerRow_OrderId", params['orderId'])
            self.action_ele.click_element('serviceid')
            self.action_ele.select_from_dropdown_using_text('serviceStatus', params['serviceStatus'])
            time.sleep(1)
            self.action_ele.click_element('btnServiceDetailsSave')
            time.sleep(3)
            self.action_ele.click_element('fnMessageBox_OK')
            time.sleep(3)
            self.action_ele.click_element('fnMessageBox_OK')

        except Exception, e:
            print(e)
            self.action_ele.clear_input_text("service_headerRow_OrderId")
            print("Failed to update service status")
            self.action_ele.takeScreenshot(inspect.currentframe().f_code.co_name)

        finally:
            self.action_ele.clear_input_text("service_headerRow_OrderId")

    def delete_contract(self, param):
        """
        To delete contract.
        :param param: Name of contract to delete
        :return:
        """
        try:
            self.action_ele.click_element("cp_allContractsbtnRefresh")
            time.sleep(2)
            self.action_ele.input_text('cp_headerRow_AccountName', param)
            time.sleep(2)
            self.action_ele.click_element('contract_grid_first_column')
            time.sleep(2)
            self.action_ele.click_element('Organization_tab')
            self.action_ele.click_element('orders_page')
            self.action_ele.select_from_dropdown_using_text('order_status_input', "Open")
            rows = self._browser.elements_finder("order_grid")
            rows = rows[1:]
            count = len(rows)
            while rows and count != 0:
                row = rows.pop(0)
                div_list = row.find_elements_by_tag_name("div")
                account_link = div_list[0].find_element_by_tag_name("a")
                account_link.click()
                self.action_ele.explicit_wait('process_button')
                time.sleep(2)
                self.action_ele.click_element('process_button')
                time.sleep(2)
                self.action_ele.click_element('close_yes')
                time.sleep(2)
                rows = self._browser.elements_finder("order_grid")
                rows = rows[1:]
                count = count - 1
            cm = CommonFunctionality.CommonFunctionality(self._browser)
            cm.switch_page_accounts(param)
            self.action_ele.click_element('ac_filter_link')
            # self.action_ele.select_from_dropdown_using_index('ac_filter',5)
            elements = self._browser.elements_finder('ac_filter')
            for element in elements:
                if (element.text == "All accounts"):
                    element.click()
            self.action_ele.input_text('ac_search_account', param)
            row = self._browser.element_finder('ac_contracts_grid')
            div_list = row.find_elements_by_tag_name("div")
            checkbox = div_list[0].find_element_by_tag_name("input")
            checkbox.click()
            self.action_ele.click_element('ac_contract_close')
            cur_date = datetime.date.today()
            self.action_ele.input_text('ac_cease_date', cur_date.strftime('%m/%d/%Y'))
            self.action_ele.select_from_dropdown_using_text('ac_cease_reason', "Lost For Cause")
            self.action_ele.select_from_dropdown_using_index('ac_requested_by', 2)
            self.action_ele.select_from_dropdown_using_text('ac_request_source', "Case")
            self.action_ele.input_text('ac_case_number', "12345")
            self.action_ele.input_text('ac_notify_mail', 'staff@shoretel.com')
            time.sleep(5)
            self.action_ele.click_element('ac_next')
            self.action_ele.click_element('ac_next')
            self.action_ele.click_element('ac_closeaccount_finish')
            try:
                element = self._browser.element_finder('ac_error')
                return False
            except Exception, e:
                return True
        except:
            print(e)
            print("Failed to delete contract")

    def verify_delete_contract(self, param):
        """
        To verify the contract is deleted.
        :param param: Contract name
        :return:
        """
        try:
            # self.action_ele.click_element('ac_filter_link')
            # elements = self._browser.elements_finder('ac_filter')
            # for element in elements:
            #     if (element.text == "All accounts"):
            #         element.click()
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.click_element("account_filter_button")
            elements = self._browser.elements_finder("filer_list")
            for ele in elements:
                if ele.text == "All accounts":
                    ele.click()
                    break
            self.action_ele.clear_input_text("contract_name_filed")
            self.action_ele.input_text("contract_name_filed",param)
            self.action_ele.click_element("contract_chk_box")
            self.action_ele.click_element("name_contract")
            elements_label=self._browser.elements_finder("disp_name")
            elements_data=self._browser.elements_finder("dis_value")
            for i in range(len(elements_label)):
                if elements_label[i].text == "Status" and elements_data[i].text == "Closed":
                    status = True
                    print("Contract Closed")
        except Exception,e:
            print(e)
        return status

    def provision_initial_order(self):
        """
        To verify the contract is deleted.
        :param param: Contract name
        :return:
        """
        try:
            status = False
            #import pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            self.action_ele.explicit_wait('order_status_input')
            self.action_ele.select_from_dropdown_using_text('order_status_input', "Pending")
            self.action_ele.select_from_dropdown_using_text('order_type', "Initial")
            rows = self._browser.elements_finder("order_grid")
            rows = rows[1:]
            count = len(rows)
            while rows and count != 0:
                row = rows.pop(0)
                div_list = row.find_elements_by_tag_name("div")
                account_link = div_list[0].find_element_by_tag_name("a")
                account_link.click()
                self.action_ele.explicit_wait('auto_provisioning')
                time.sleep(2)
                self.action_ele.click_element('auto_provisioning')
                time.sleep(2)
                self.action_ele.click_element('close_yes')
                time.sleep(2)
                rows = self._browser.elements_finder("order_grid")
                rows = rows[1:]
                count = count - 1
            status = True
        except Exception,e:
            print(e)
        return status

    def activate_all_service(self):
        """
        To verify the contract is deleted.
        :param param: Contract name
        :return:
        """
        try:
            status = False
            self.action_ele.explicit_wait("select_all_check_box")
            self.action_ele.click_element("select_all_check_box")
            if self.query_ele.element_enabled("service_update_button"):
                self.action_ele.click_element("service_update_button")
            time.sleep(1)
            self.action_ele.explicit_wait("service_next_button")
            self.action_ele.select_from_dropdown_using_text("service_list","Active")
            cur_date = datetime.date.today()
            self.action_ele.input_text("active_date",cur_date.strftime('%m/%d/%Y'))
            self.action_ele.click_element("service_next_button")
            cm = CommonFunctionality.CommonFunctionality(self._browser)
            cm.check_alert()
            time.sleep(2)
            self.action_ele.explicit_wait("service_finish_button")
            time.sleep(1)
            self.action_ele.click_element("service_finish_button")
            self.action_ele.explicit_wait("ac_alert_ok")
            time.sleep(1)
            self.action_ele.click_element("ac_alert_ok")
            time.sleep(2)
            status = True
        except Exception,e:
            print(e)
        return status


    def close_all_order(self):
        """
        To verify the contract is deleted.
        :param param: Contract name
        :return:
        """
        try:
            status = False
            self.action_ele.select_from_dropdown_using_text('order_status_input', "All")
            self.action_ele.select_from_dropdown_using_text('order_type', "All")
            ordersid = self._browser.elements_finder("order_id_list")
            for id in range(len(ordersid)):
                self._browser._browser.refresh()
                ordersid = self._browser.elements_finder("order_id_list")
                order_status = self._browser.elements_finder("current_order_status")
                if order_status[id].text != "Closed":
                    time.sleep(2)
                    ordersid[id].click()
                    self.action_ele.explicit_wait('save_button_order_page')
                    time.sleep(2)
                    self.action_ele.select_from_dropdown_using_text("order_status_to_close","Closed")
                    self.action_ele.click_element('save_button_order_page')
                    time.sleep(1)
                    el = self._browser.elements_finder("ac_error_ok")
                    el[1].click()
                    time.sleep(1)
                    self.action_ele.explicit_wait("expand_button")
                    time.sleep(3)
            time.sleep(3)
            status = True
        except Exception,e:
            print(e)
        return status

    def close_contract(self,name):
        """
        To verify the contract is deleted.
        :param param: Contract name
        :return:
        """
        try:
            status = False
            self.action_ele.click_element("account_filter_button")
            elements = self._browser.elements_finder("filer_list")
            for ele in elements:
                if ele.text == "All accounts":
                    ele.click()
                    break
            self.action_ele.input_text("contract_name_filed",name)
            time.sleep(3)
            self.action_ele.click_element("contract_chk_box")
            self.action_ele.click_element("close_conract")
            self.action_ele.explicit_wait("next_button")
            cur_date = datetime.date.today()
            self.action_ele.input_text("close_date", cur_date.strftime('%m/%d/%Y'))
            self.action_ele.click_element("label1")
            self.action_ele.select_from_dropdown_using_index("req_by",1)
            self.action_ele.select_from_dropdown_using_text("req_source","Email")
            self.action_ele.click_element("next_button")
            self.action_ele.click_element("next_button")
            self.action_ele.click_element("finishbtn")
            self.action_ele.explicit_wait("ac_error_ok",40)
            time.sleep(1)
            self.action_ele.click_element("ac_error_ok")
            time.sleep(2)
            status = True
        except Exception,e:
            print(e)
        return status
