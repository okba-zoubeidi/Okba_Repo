"""Director Portal Module
"""
import time
import sys
import stafenv
from D2API import D2API

_DEFAULT_TIMEOUT = 3

class DirectorComponent(object):
    """Component class for the director
    """
    def director_client_login(self, **params):
        """
        This function will login to D@ portal
        :param params:
        :return:
        """
        if params.keys():
            self.director = D2API(params["IP"], params["username"], params["password"])
        else:
            print("Please check that the input parameters have been provided")


    def director_verify_tenant_location(self, **params):
        """
        This function will verify the location created for tenant
        :param params:
        :return:
        """
        if params.keys():
            location_list = self.director.fetch_tenant_specific_sites(params["account"])
            for count in xrange(5):
                location_list = self.director.fetch_tenant_specific_sites(params["account"])
                if location_list:
                    break
                else:
                    time.sleep(_DEFAULT_TIMEOUT)
            for location in location_list:
                if location == params["exp_location"]:
                    return True
                else:
                    return False
        else:
            print("Please check that the input parameters have been provided")


    def director_verify_emergency_hunt_group(self, **params):
        """
        This function will verify the emergency hunt group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            HG_list = self.director.fetch_tenant_specific_hunt_group(params["newacc"])
            for count in xrange(5):
                HG_list = self.director.fetch_tenant_specific_hunt_group(params["newacc"])
                if HG_list:
                    break
                else:
                    time.sleep(2)

            for id, hg, extn in HG_list:
                if hg == params["exp_huntgroup"]:
                    return True
            return False
        else:
            print("Please check that the input parameters have been provided")


    def director_verify_hunt_group(self, **params):
        """
        This function will verify the hunt group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            HG_list = self.director.fetch_tenant_specific_hunt_group(params["newacc"])
            for count in xrange(5):
                HG_list = self.director.fetch_tenant_specific_hunt_group(params["newacc"])
                if HG_list:
                    break
                else:
                    time.sleep(_DEFAULT_TIMEOUT - 1)

            for id, hg, extn in HG_list:
                if hg == params["exp_huntgroup"] and extn == params["hg_extn"]:
                    return True
            return False
        else:
            print("Please check that the input parameters have been provided")

    def director_verify_hunt_group_member(self, **params):
        """
        This function will verify the hunt group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            HG_list = self.director.fetch_tenant_specific_hunt_group_member(params["newacc"], params["hg_extn"])
            for count in xrange(5):
                hunt_group_members = self.director.fetch_tenant_specific_hunt_group_member(params["newacc"], params["hg_extn"])
                if hunt_group_members:
                    break
                else:
                    time.sleep(_DEFAULT_TIMEOUT - 1)
            for hgmem in hunt_group_members:
                print hgmem
                if hgmem['id'].split('-')[-1] == params["hgmember"]:
                    memid = hgmem['id'].split('-')[-1]
                    print "Group Member id :" +memid+ " is found"
                    return True
            return False
        else:
            print("Please check that the input parameters have been provided")

    def director_verify_Extension_List(self, **params):
        """
        This funtion will veirfy the paging group in D2 page
        :param params:
        :return:
        """
        if params.keys():
            # AA_list = self.director.fetch_tenant_specific_auto_attendant(params["newacc"])
            for count in xrange(5):
                Ex_list = self.director.fetch_tenant_specific_Extension_List(params["newacc"])
                if Ex_list:
                    break
                else:
                    time.sleep(2)
            for extnName in Ex_list:

                if extnName == params["exp_D2extensionList"]:
                    return True
            return False
        else:
            print("Please check that the input parameters have been provided")

    def director_verify_pickup_group(self, **params):
        """
        This func will verify pick group from D2 page
        :param params:
        :return:
        """
        if params.keys():
            PG_list = self.director.fetch_tenant_specific_pickup_group(params["newacc"])
            for count in xrange(5):
                PG_list = self.director.fetch_tenant_specific_pickup_group(params["newacc"])
                if PG_list:
                    break
                else:
                    time.sleep(2)

            for pg, extn in PG_list:
                if pg == params["exp_pickupgroup"] and extn == params["pk_extn"]:
                    return True

            return False

        else:
             print("Please check that the input parameters have been provided")

    def director_verify_auto_attendant(self, **params):
        """
        Verify the Auto Attendant in D2 page
        :param params:  ditionary contain auto attendant information
        :return:
        """
        if params.keys():
            #import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            for count in xrange(5):
                AA_list = self.director.fetch_tenant_specific_auto_attendant(params["newacc"])
                if AA_list:
                    break
                else:
                    time.sleep(2)

            for aa, extn in AA_list:
                print(aa, extn)
                if aa == params["Aa_Name"] and extn==params["Aa_Extension"] :
                    print("Match Found")
                    return True
            return False
        else:
            print("Please check that the input parameters have been provided")

    def director_verify_custom_schedule(self, **params):
        """
        Verification of custom schedle in D2 page
        :param params:
        :return: status
        """
        if params.keys():
            cs_list = self.director.fetch_tenant_specific_custom_schedule(params["newacc"])
            for count in xrange(5):
                cs_list = self.director.fetch_tenant_specific_custom_schedule(params["newacc"])
                if cs_list:
                    break
                else:
                    time.sleep(2)

            for cs in cs_list:
                if cs == params["exp_customschedule"]:
                    return True

            return False
        else:
             print("Please check that the input parameters have been provided")

    def director_verify_paging_group(self,**params):
        """
        Verify the paging group in D2 page
        :param params:  Dictionary of paging group  information
        :return:
        """
        if params.keys():
                for count in xrange(5):
                    Pg_list = self.director.fetch_tenant_specific_page_group(params["newacc"])
                    if Pg_list:
                        break
                    else:
                        time.sleep(2)
                for pg, extn in Pg_list:
                    if pg == params["Pg_Name"] and extn==params["Pg_Extension"] :
                        return True
                return False
        else:
            print("Please check that the input parameters have been provided")
            raise

    def director_verify_holiday_schedule(self, **params):
        """
        Verification of holiday schedule in D2 page
        :param params:
        :return: status
        """
        if params.keys():
            HS_list = self.director.fetch_tenant_specific_holiday_schedule(params["newacc"])
            for count in xrange(5):
                HS_list = self.director.fetch_tenant_specific_holiday_schedule(params["newacc"])
                if HS_list:
                    break
                else:
                    time.sleep(2)
            for hs, date, timezone in HS_list:
                if hs == params["exp_holidayschedule"] and date == params["exp_date"] and timezone == params["exp_timezone"]:
                    print "Holiday schedule name: ", hs
                    print "Holiday schedule day date: ", date
                    print "Holiday schedule timezone: ", timezone
                    return True

        else:
             print("Please check that the input parameters have been provided")
        return False

    def director_verify_on_hours_schedule(self, **params):
        """
        Verification of on hours schedule in D2 page
        :param params:
        :return: status
        """
        if params.keys():
            ohs_list = self.director.fetch_tenant_specific_on_hours_schedule(params["newacc"])
            for count in xrange(5):
                ohs_list = self.director.fetch_tenant_specific_on_hours_schedule(params["newacc"])
                if ohs_list:
                    break
                else:
                    time.sleep(2)

            for ohs in ohs_list:
                if ohs == params["exp_on_hours_schedule"]:
                    return True

            return False
        else:
            print("Please check that the input parameters have been provided")

    def director_verify_bridged_call_appearance(self, **params):
        '''
        Description: Verify the Bridged call appearance created in BOSS is reflected in D2
        param: params contains D2 information
        return: status True/False
        Created by: Immani Mahesh Kumar
        Modified by: Prasanna
        '''

        if params.keys():
            for count in xrange(5):
                bca_list = self.director.fetch_tenant_specific_bridged_call_appearance(params["newacc"])
                if bca_list:
                    break
                else:
                    time.sleep(2)
            else:
                print("Fetching from D2 failed!")
                return False

            for bca in bca_list:
                # if bca == params["exp_Bca"]:
                if params["exp_Bca"] in bca:
                    return True

            return False
        else:
             print("Please check that the input parameters have been provided")
             return False

    def director_fetch_and_verify_dnis(self, **params):
        '''
        Description: fetch and verify the DNIS associated with BCA/aBCA from D2
        param: params contains D2 information
        return: status True/False
        Created by: Prasanna
        '''

        if params.keys():
            for count in xrange(5):
                dnis_list = self.director.fetch_tenant_specific_dnis(params["tenant"])
                if dnis_list:
                    break
                else:
                    time.sleep(2)
            else:
                print("Fetching from D2 failed!")
                return False

            for dnis in dnis_list:
                if dnis == params["dnis"]:
                    return True

            return False
        else:
             print("Please check that the input parameters have been provided")
             return False

    def director_verify_user_groups(self, **params):
        """
        This function will verify the user group location in D2 page
        :param params:
        :return:
        """
        if params.keys():
            ug_list = self.director.fetch_tenant_specific_user_groups(params["newacc"])
            for count in xrange(5):
                ug_list = self.director.fetch_tenant_specific_user_groups(params["newacc"])
                if ug_list:
                    break
                else:
                    time.sleep(_DEFAULT_TIMEOUT - 1)
            for ug_name in ug_list:
                if ug_name.split('-')[0] == params["exp_user_group"]:
                    return True
            return False
        else:
            print("Please check that the input parameters have been provided")
