from CommonFunctionality import CommonFunctionality
from PersonalInformation import PersonalInformation
from AccountHandler import AccountHandler
from AddPartition import AddPartition
from PhoneNumber import PhoneNumber
from UserHandler import UserHandler
from VCFEHandler import VCFEHandler
from InvoicesPayments import InvoicesPayments
from ProgButtonHandler import ProgButtonHandler
from AOB_Functionality import AobFunctionality
from BCA_Operations import BCAOperations
from AddonFeature import AddonFeature
from Service import Service
from ProfileFunctionality import ProfileFunctionality
from PhoneUsers import PhoneUsers

class BossPage(object):
    """Module for all the BOSS pages"""

    def __init__(self, browser):
        self.commonfunctionality = CommonFunctionality(browser)
        self.personal_information = PersonalInformation(browser)
        self.account_handler = AccountHandler(browser)
        self.add_partition = AddPartition(browser)
        self.phone_number = PhoneNumber(browser)
        self.user_handler = UserHandler(browser)
        self.VCFE_Handler = VCFEHandler(browser)
        self.Invoices_Payments = InvoicesPayments(browser)
        self.prog_button_handler = ProgButtonHandler(browser)
        self.aobfunctionality = AobFunctionality(browser)
        self.BCAOperations = BCAOperations(browser)
        self.addonfeature = AddonFeature(browser)
        self.profileFunctionality = ProfileFunctionality(browser)
        self.service = Service(browser)
        self.phoneServiceUsers = PhoneUsers(browser)
