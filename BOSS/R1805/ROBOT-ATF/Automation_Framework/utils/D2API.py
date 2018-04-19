import sys
import requests
import urllib, base64
import re
import json
from robot.api.logger import console

class D2API():

    def __init__(self, ip, username, password):
        self.client = requests.session()
        self.ip = ip
        self.create_connection(ip, username, password)

    def create_connection(self, hqIp, username, password):
        """
        """
        # Retrieve the CSRF token first
        LOGIN_URL = 'http://'+hqIp+':5478/director/login'
        self.client.get(LOGIN_URL)  # sets cookie
        d2_cookie = self.client.cookies['_director2_session']
        ##print d2_cookie
        csrftoken = re.match('(.+)--',d2_cookie).group(1)
        ##print csrftoken
        csrftoken = urllib.unquote(d2_cookie)
        ##print csrftoken
        csrftoken = base64.b64decode(csrftoken)
        # csrftoken = r'{I"session_id:EFI"%8cb0cc7d1645b236e217e3e35826b9dd; TI"abc; F{:	hostI"localhost; FI"_csrf_token; FI"1lC0TGuAk9D6C0f68Fy9T8UsQ0RaQg9uXiTRnPra+iLE=; F'
        ##print csrftoken
        # csrftoken = re.match('.*_csrf_token.*1(.*=).*', csrftoken).group(1)
        csrftoken = re.match('.*_csrf_token.*\"1(.*=).*', csrftoken).group(1)
        ##print csrftoken

        # 'admin@mt.com', 'changeme'
        self.client.post(LOGIN_URL,data={"user_session[login_name]": username, "user_session[login_password]": password, "authenticity_token": csrftoken})
        # r = client.get(LIST_SWITCH_URL)

    def fetch_tenants_info(self):
        """
        """
        #self.create_connection(ip, username, password)
        LIST_TENANTS_URL = 'http://'+self.ip+':5478/director/tenants/list?_search=false&rows=600'
        result = self.client.get(LIST_TENANTS_URL)

        d = json.loads(result.text)
        tInfo = []
        for device in d['rows']:
            tmpList = [str(device['cell'][0]), str(device['cell'][1]), str(device['cell'][2])]
            tInfo.append(tmpList)
        tInfo.pop(0)
        return tInfo

    def get_specific_tenants(self, tenantNames):
        info = self.fetch_tenants_info()
        specificTenants = []
        tenantNamesList = tenantNames.split(",")
        for tname in tenantNamesList:
            for tinfo in info:
                if tname.lstrip(" '").rstrip("'") == tinfo[0]:
                    specificTenants.append(tinfo)
                    break
        print "ok",specificTenants
        return specificTenants

    def get_specific_tenants(self, tenantNames):
        info = self.fetch_tenants_info()
        specificTenants = []
        tenantNamesList = tenantNames.split(",")
        for tname in tenantNamesList:
            for tinfo in info:
                if tname.lstrip(" '").rstrip("'") == tinfo[0]:
                    print("matched")
                    specificTenants.append(tinfo)
                    break
        print "ok",specificTenants
        return specificTenants

    def fetch_tenant_specific_sites(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames)
        sites = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':5478/director/sites/list?filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%22'+str(tenant[1])+r'%22%7D%5D%7D'
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                sites.append(str(userData['cell'][0]))
        print "sites from specific : ", sites
        return sites

    def fetch_tenant_specific_hunt_group(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':5478/director/users/list'
        hunt_group = []
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':5478/director/dns/list?list=hunt_group&rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                hunt_group.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print "hunt_group from specific : ", hunt_group
        return hunt_group

    def fetch_tenant_specific_pickup_group(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        # LIST_USERS_URL = 'http://'+ip+':5478/director/users/list'
        pickup_group = []
        for tenant in tList:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            LIST_USERS_URL_NEW = r'http://'+self.ip+':5478/director/group_pickups/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                pickup_group.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
        print "pickup_group from specific : ", pickup_group
        return pickup_group

    def fetch_tenant_specific_auto_attendant(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        auto_attendant=[]
        for tenant in tList:
            LIST_USERS_URL_NEW = r'http://'+self.ip+':5478/director/menus/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            #print(LIST_USERS_URL_NEW)
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            #print(d)
            for userData in d['rows']:
                auto_attendant.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
            print("auto_attendant from specific : ", auto_attendant)
            return auto_attendant

    def fetch_tenant_specific_page_group(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        paging_groups=[]
        for tenant in tList:
            #LIST_USERS_URL_NEW=r'http://'+self.ip+':5478/director/paging_groups/list?_search=true&nd=1495616642261&rows=50&page=1&sidx=&sord=asc&filters=%7B%22groupOp%22%3A%22OR%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22TenantID%22%2C%22op%22%3A%22eq%22%2C%22data%22%3A%'+str(tenant[1])+r'%22%7D%5D%7D'
            LIST_USERS_URL_NEW = r'http://'+self.ip+':5478/director/paging_groups/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                paging_groups.append((str(userData['cell'][0]), str(userData['cell'][1]).split('-')[-1]))
            print("auto_attendant from specific : ",paging_groups)
            return paging_groups

    def fetch_tenant_specific_custom_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':5478/director/users/list'
        custom_schedule = []
        for tenant in tList:
            # import pdb;
            # pdb.Pdb(stdout=sys.__stdout__).set_trace()
            LIST_USERS_URL_NEW =r'http://'+self.ip+':5478/director/schedules_customs/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                custom_schedule.append(str(userData['cell'][0]))
        print "custom_schedule from specific : ", custom_schedule
        return custom_schedule

    def fetch_tenant_specific_holiday_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        #LIST_USERS_URL = 'http://'+ip+':5478/director/users/list'
        holiday_schedule = []
        for tenant in tList:
            LIST_USERS_URL_NEW =r'http://'+self.ip+':5478/director/schedules_holidays/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            print LIST_USERS_URL_NEW
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                holiday_schedule.append((str(userData['cell'][0]), str(userData['cell'][1]), str(userData['cell'][2])))
        print "Holiday schedule from specific : ", holiday_schedule
        return holiday_schedule

    def fetch_tenant_specific_Extension_List(self,tenantNames):
        tenantNames = tenantNames.strip('"')
        tList = self.get_specific_tenants(tenantNames)
        extension_List=[]
        for tenant in tList:
            LIST_USERS_URL_NEW=r'http://'+self.ip+':5478/director/extension_lists/list?rows=1000&_filter_tenant_id='+str(tenant[1])+r'&_filter_system_tenant_id='+str(tenant[1])+r''
            result = self.client.get(LIST_USERS_URL_NEW)
            d = json.loads(result.text)
            for userData in d['rows']:
                extension_List.append(str(userData['cell'][0]))
            print("Extension List from specific : ",extension_List)
            return extension_List

    def fetch_tenant_specific_on_hours_schedule(self, tenantNames):
        tList = self.get_specific_tenants(tenantNames.strip('"'))
        # LIST_USERS_URL = 'http://'+ip+':5478/director/users/list'
        on_hours_schedule = []
        for tenant in tList:
            list_users_url_new = r'http://' + self.ip + ':5478/director/schedules_on_hours/list?rows=1000&_filter_tenant_id=' + str(
                tenant[1]) + r'&_filter_system_tenant_id=' + str(tenant[1]) + r''
            print list_users_url_new
            result = self.client.get(list_users_url_new)
            d = json.loads(result.text)
            print d
            for userData in d['rows']:
                on_hours_schedule.append(str(userData['cell'][0]))
        print "on_hours_schedule from specific : ", on_hours_schedule
        return on_hours_schedule

if __name__ == "__main__":
    fo = D2API("10.197.108.10", "admin@mt.com", "changeme1#")
    t=fo.fetch_tenant_specific_sites("AutoTest_Acc_tPlVvmZA")