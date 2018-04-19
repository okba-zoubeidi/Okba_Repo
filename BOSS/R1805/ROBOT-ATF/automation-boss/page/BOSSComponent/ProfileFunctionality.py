"""Module for creating and verifying profiles
   File: ProfileFunctionality.py
"""

import os
import sys
import time
import random
import string
from web_wrappers import selenium_wrappers as base
from mapMgr import mapMgr
import inspect


# TODO move path dependency to stafenv.py and import here
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils"))

class ProfileFunctionality(object):

    def __init__(self, browser):
        self._browser = browser
        self.action_ele = base.WebElementAction(self._browser)
        self.query_ele = base.QueryElement(self._browser)
        self.assert_ele = base.AssertElement(self._browser)

    # Start -- Function "click_ok_button"
    def click_ok_button(self):
        """
            `Description:` This function verifies the page contents before clicking on OK button.
            In case of Error message it throws an exception
            `Returns:` True / False
        """
        status = True
        self.action_ele.explicit_wait("ProfileOperationSuccessOK")
        try:
            self._browser.element_finder("ProfileSaveSuccessPageTitle")
        except Exception as error:
            print(error.message)
            status = False
        time.sleep(5)
        self.action_ele.click_element("ProfileOperationSuccessOK")
        return status
    # End -- Function "click_ok_button"

    def handle_next_operation(self, params, len_list):
        """
             `Description:` Handling of the next button in case of add Profile operations
             `Param1:` params: profile info
             `Param2:` len_list: length of the list of phone numbers
             `Returns:` True / False
         """
        status = True

        i = 2
        while True:
            self.action_ele.explicit_wait("ProfileAddNextButton")
            self.action_ele.click_element("ProfileAddNextButton")
            try:
                self.action_ele.explicit_wait("RequestedByAdd", 3)
                status = True
            except Exception as error:
                print(error.message)
                status = False

            if status:
                break
            elif i >= len_list:
                print("Wait for the next page out of phone numbers")
                # cancel the operation
                self.action_ele.explicit_wait("ProfileAddCancelButton")
                self.action_ele.click_element("ProfileAddCancelButton")
                self.action_ele.explicit_wait("ProfileConfirmYesButton")
                self.action_ele.click_element("ProfileConfirmYesButton")

            elif not status:
                if 'customExtn' in params:
                    print("EXTENSION IN USE, try another custom one")
                    self.action_ele.explicit_wait('ErrorMessageAddExtension')
                    message = (self.query_ele.get_text("ErrorMessageAddExtension"))
                    new_extn = 1000
                    if "Suggested extension" in message:
                        msg_to_list = message.split(" ")
                        new_extn = int(msg_to_list.pop())
                    else:
                        new_extn = random.randint(1000, 9999)
                    self.action_ele.input_text('AddExtension', new_extn)

                else:
                    print("EXTENSION IN USE, try the next one")
                    self.action_ele.select_from_dropdown_using_index("AddTnId", i)
                    params["selectedPhoneNumber"] = (self.query_ele.get_text_of_selected_dropdown_option("AddTnId").strip())

                params["selectedExtn"] = self.query_ele.get_value("AddExtension")
                i += 1

        return status

    # Start --- Function "handle_save_operation"
    def handle_save_operation(self, params, len_list):
        """
            `Description:` Handling of the save button in case of add Profile operations
            `Param1:` params: profile info
            `Param2:` len_list: length of the list of phone numbers
            `Returns:` True / False
        """
        status = True

        self.action_ele.explicit_wait("ProfileAddSaveButton")
        self.action_ele.click_element("ProfileAddSaveButton")
        status = self.click_ok_button()

        if not status:
            # cancel the operation
            self.action_ele.explicit_wait("ProfileAddCancelButton")
            self.action_ele.click_element("ProfileAddCancelButton")
            self.action_ele.explicit_wait("ProfileConfirmYesButton")
            self.action_ele.click_element("ProfileConfirmYesButton")

        return status
    # End --- Function "handle_save_operation"

    def add_user_profile(self, params):
        self.action_ele.explicit_wait("partitionProfilesDataGridAddButton")
        self.action_ele.click_element('partitionProfilesDataGridAddButton')
        self.action_ele.explicit_wait("AddLocationToAssign")
        self.action_ele.select_from_dropdown_using_text('AddLocationToAssign', params['profileLocation'])

        # only select a phone number if there is a parameter for phoneNumber
        listLen = 0;
        if 'phoneNumber' in params:
            self.action_ele.explicit_wait("TnEnabled")
            self.action_ele.select_checkbox("TnEnabled")
            self.action_ele.explicit_wait("AddTnId")
            # if the param is randon, then select the first one
            if params['phoneNumber'] == 'random':
                phoneNumberList= self.query_ele.get_text_list_from_dropdown("AddTnId")
                listLen=    len(phoneNumberList);
                self.action_ele.select_from_dropdown_using_index("AddTnId", listLen-1)
                self.action_ele.explicit_wait("AddTnId")
                params["selectedPhoneNumber"]=  (self.query_ele.get_text_of_selected_dropdown_option("AddTnId").strip())
            else:
                self.action_ele.select_from_dropdown_using_index("AddTnId", params['phoneNumber'])

        # autoExtn should only exist if this open should be selected
        if 'customExtn' in params:
            self.action_ele.input_text('AddExtension', params['customExtn'])
        elif 'autoExtn' in params:
            self.action_ele.explicit_wait("AddAutoAssignExtn")
            self.action_ele.select_checkbox("AddAutoAssignExtn")

        params["selectedExtn"] = self.query_ele.get_value("AddExtension")
        self.action_ele.input_text('AddFirstName', params['firstName'])
        self.action_ele.input_text('AddLastName', params['lastName'])
        self.action_ele.input_text('AddEmail', params['email'])
        result=     self.handle_next_operation(params, listLen)
        if result:
            self.action_ele.explicit_wait("RequestedByAdd")
            self.action_ele.select_from_dropdown_using_index("RequestedByAdd", 1)
            self.action_ele.select_from_dropdown_using_index("RequestSourcesAdd", 1)
        return self.handle_save_operation(params, listLen)

    def preview_profile_import(self):
        self.action_ele.explicit_wait("ImportPreviewButton")
        self.action_ele.click_element('ImportPreviewButton')
        return True


    def unassign_profile(self):
        """
        `Description:` Unassign selected profiles

        `:param`

        `:return:`

        """
        print("Start unassign_profile ")
        self.action_ele.explicit_wait('ProfileUnassignButton')
        self.action_ele.click_element("ProfileUnassignButton")
        #Select the first person in the request by  dropdown. There should be at least one
        self.action_ele.select_from_dropdown_using_index("RequestedByDropdown", 1)
        #Select email as the request source
        self.action_ele.select_from_dropdown_using_index("RequestSources", 1)
        self.action_ele.explicit_wait('ProfileUnassignOKButton')
        self.action_ele.click_element("ProfileUnassignOKButton")
        self.action_ele.explicit_wait_not_visible('ProfileUnassignProcessing')
        self.action_ele.explicit_wait('ProfileUnassignSuccessOK')
        self.action_ele.click_element("ProfileUnassignSuccessOK")
        print("End unassign_profile ")


    def import_previewed_profiles(self):
        try:
            self.action_ele.explicit_wait("ImportFormRequestedBy")
            self.action_ele.select_from_dropdown_using_index("ImportFormRequestedBy", 1)
            self.action_ele.select_from_dropdown_using_index("ImportFormRequestedSources", 1)
            self.action_ele.explicit_wait("ImportFormImportButton")
            self.action_ele.click_element('ImportFormImportButton')
            self.action_ele.explicit_wait("ImportFormMessageText", 70)
            msgText = self.query_ele.get_text("ImportFormMessageText")
            if "Order has been created" in msgText:
                self.action_ele.click_element('ImportFormCloseButton')
                return True
            return False
        except Exception as e:
            print("Exception when trying to import profiles " + e.message)
            return False

    def read_profiles_from_import_file(self, file_path):
        try:
            profile_list=[]
            with open(file_path) as fp:
                i = 0
                for line in fp:
                    if i == 0:
                        i += 1
                        continue
                    print(line)
                    line = line.replace('\n', '').replace('\r', '')
                    profile_data = line.split(',')
                    profile = dict()
                    profile['type'] = profile_data[1]
                    profile['phoneNumber'] = profile_data[2]
                    profile['extn'] = profile_data[3]
                    profile['firstName'] = profile_data[4]
                    profile['lastName'] = profile_data[5]
                    profile['email'] = profile_data[6]
                    profile['profileLocation'] = profile_data[7]
                    profile_list.append(profile)
                    i += 1
            fp.close()
            return profile_list
        except Exception as e:
            print("Exception when trying to read the import profiles file" + e.message)
            return None

