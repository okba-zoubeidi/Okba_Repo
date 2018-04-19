__author__ = "nkumar@soretel.com"

import sys, requests, os, logging, ast, json
sys.path.append(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname((__file__))))))
from utils.decorators import func_logger

log = logging.getLogger("boss_api.vcfe")


class Vcfe():
    """
    Apis for the vcfe related operations.
    """

    @func_logger
    def create_auto_attendant(self, **params):
        '''
        This function will create an auto attendant
        phone system -> visual call flow editor -> Add -> Auto attendant
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("create_auto_attendant")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["data"] = str(self.get_cosmo_component(act_id, part_id, params['componentType'])['data'])
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        # replacing the default name and extension if provided by the user
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('aa_name') is not None:
            temp = json.loads(params['data'])
            temp['menu']['dn_attributes']['Description'] = params['aa_name']
            if params.get('aa_extension') is not None:
                temp['menu']['dn_attributes']['DN_formatted'] = params['aa_extension']
            # converting the dict back to string
            params['data'] = json.dumps(temp)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating auto attendant with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The auto attendant has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create auto attendant.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def edit_auto_attendant(self, comp_name, **params):
        '''
        This function will edit an auto attendant
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("edit_auto_attendant")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, comp_name)
        params['id'] = id
        params["data"] = str(self.get_cosmo_component(act_id, part_id, componentType=params['componentType'],id=id)['data'])
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        # replacing the default name and extension if provided by the user
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('aa_name') is not None:
            temp = json.loads(params['data'])
            temp['menu']['dn_attributes']['Description'] = params['aa_name']
            if params.get('aa_extension') is not None:
                temp['menu']['dn_attributes']['DN_formatted'] = params['aa_extension']
            # converting the dict back to string
            params['data'] = json.dumps(temp)
        params['data'] = params['data'].replace("'", '"')
        url = params.pop("url")
        log.info("Editing auto attendant with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The auto attendant has been edited successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not edit auto attendant.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def delete_auto_attendant(self, comp_name, **params):
        '''
        This function will delete an auto attendant
        :return: A tuple of a boolean status flag and the return object from the requested url
        '''
        result = False
        params_xml = self.config.getparams("delete_auto_attendant")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, comp_name)
        params['id'] = id
        # params["data"] = str(self.get_cosmo_component(act_id, part_id, componentType=params['componentType'], id=id)['data'])
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        url = params.pop("url")
        log.info("Editing auto attendant with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The auto attendant has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete auto attendant.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def create_hunt_group(self, **params):
        '''
        This function will create an hunt group
        phone system -> visual call flow editor -> Add -> Hunt Group
        :return: A tuple of a boolean status flag and the return object from the requested url

        Note: The back up extension must be assigned to a user.
        '''
        result = False
        params_xml = self.config.getparams("create_hunt_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["data"] = str(self.get_cosmo_component(act_id, part_id, params['componentType'])['data'])
        # replacing the default name and extension if provided by the user
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('hg_name') is not None:
            temp = json.loads(params['data'])
            temp['hunt_group']['dn_attributes']['Description'] = params['hg_name']
            if params.get('hg_extension') is not None:
                temp['hunt_group']['dn_attributes']['DN_formatted'] = params['hg_extension']
            # adding the back up extension
            temp['hunt_group']['BackupDN_formatted'] = params['hg_backup_extn']
            # setting the SiteID -- this step is questionable but seems mandatory to create hunt group
            temp['hunt_group']['SiteID'] = temp['collections']['sites'][0]['SiteID']
            # converting the dict back to string
            params['data'] = json.dumps(temp)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating hunt group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The hunt group has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create hunt group.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def edit_hunt_group(self, hg_to_edit, **params):
        '''
        This function will edit a hunt group
        phone system -> visual call flow editor -> Select hunt group -> Edit
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("edit_hunt_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["data"] = str(self.get_cosmo_component(act_id, part_id, params['componentType'])['data'])
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, hg_to_edit)
        params['id'] = id
        params["data"] = self.get_cosmo_component(act_id, part_id, componentType=params['componentType'], id=id)['data']
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        # replacing the default name and extension if provided by the user
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('hg_name') is not None:
            temp = json.loads(params['data'])
            temp['hunt_group']['dn_attributes']['Description'] = params['hg_name']
            if params.get('hg_extension') is not None:
                temp['hunt_group']['dn_attributes']['DN_formatted'] = params['hg_extension']
            # adding the back up extension
            temp['hunt_group']['BackupDN_formatted'] = params['hg_backup_extn']
            # setting the SiteID -- this step is questionable but seems mandatory to create hunt group
            temp['hunt_group']['SiteID'] = temp['collections']['sites'][0]['SiteID']
            # converting the dict back to string
            params['data'] = json.dumps(temp)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Editing hunt group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The hunt group has been edited successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not edit hunt group.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def delete_hunt_group(self, hg_to_delete, **params):
        '''
        This function will delete a hunt group
        phone system -> visual call flow editor -> Select hunt group -> Delete
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("delete_hunt_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, hg_to_delete)
        params['id'] = id
        # params["data"] = str(self.get_cosmo_component(act_id, part_id, componentType=params['componentType'], id=id)['data'])
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        url = params.pop("url")
        log.info("Deleting hunt group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The hunt group has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete hunt group.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def create_extension_list(self, **params):
        '''
        This function will create an extension list
        phone system -> visual call flow editor -> Add -> Extension List
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("create_extension_list")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        el_data = str(self.get_cosmo_component(act_id, part_id, params['componentType']))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('el_name') is not None:
            temp = ast.literal_eval(el_data)
            commondata = json.loads(temp['commondata'])
            data = json.loads(temp['data'])
            data['extension_list']['Name'] = params['el_name']
            # creating the list of extensions to be supplied in the request
            my_extn_list = []
            my_extn = {}
            dn_ids = []
            for extn in params['el_extns']:
                for row in commondata['rows']:
                    if extn == row['id'].split('-')[-1]:
                        my_extn["id"] = row['cell'][0]
                        my_extn["Description"] = row['cell'][1]
                        my_extn["DN"] = extn
                        dn_ids.append(row['cell'][0])
                        my_extn_list.append(my_extn)
                        break
                my_extn = {}

            data['extension_list']['selected_extension_list'] = my_extn_list
            data['extension_list']['dn_ids'] = dn_ids
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating extension list with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The extension list has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create extension list.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def edit_extension_list(self, el_to_edit, **params):
        '''
        This function will edit an extension list
        phone system -> visual call flow editor -> Select extension list -> Edit
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("edit_extension_list")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, el_to_edit)
        params['id'] = id
        el_data = str(self.get_cosmo_component(act_id, part_id, params['componentType'], id=id))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('el_name') is not None:
            temp = ast.literal_eval(el_data)
            commondata = json.loads(temp['commondata'])
            data = json.loads(temp['data'])
            data['extension_list']['Name'] = params['el_name']
            # creating the list of extensions to be supplied in the request
            my_extn_list = []
            my_extn = {}
            dn_ids = []
            for extn in params['el_extns']:
                for row in commondata['rows']:
                    if extn == row['id'].split('-')[-1]:
                        my_extn["id"] = row['cell'][0]
                        my_extn["Description"] = row['cell'][1]
                        my_extn["DN"] = extn
                        dn_ids.append(row['cell'][0])
                        my_extn_list.append(my_extn)
                        break
                my_extn = {}

            data['extension_list']['selected_extension_list'] = my_extn_list
            data['extension_list']['dn_ids'] = dn_ids
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'", '"')

        url = params.pop("url")
        log.info("Editing extension list with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The extension list has been edited successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not edit extension list.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def delete_extension_list(self, el_to_delete, **params):
        '''
        This function will delete an extension list
        phone system -> visual call flow editor -> Select extension list -> Delete
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("delete_extension_list")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, el_to_delete)
        params['id'] = id
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        url = params.pop("url")
        log.info("Deleting extension list with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The extension list has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete extension list.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def create_paging_group(self, **params):
        '''
        This function will create a paging group
        phone system -> visual call flow editor -> Add -> Paging Group
        :return: A tuple of a boolean status flag and the return object from the requested url

        Note: There must already be an existing extension list.
        '''
        result = False
        params_xml = self.config.getparams("create_paging_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        pg_data = str(self.get_cosmo_component(act_id, part_id, params['componentType']))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('pg_name') is not None:
            temp = ast.literal_eval(pg_data)
            data = json.loads(temp['data'])
            data['paging_group']['dn_attributes']['Description'] = params['pg_name']
            data['paging_group']['dn_attributes']['DN_formatted'] = params['pg_extension']
            collections = data['collections']
            #TODO The below step is not clear but is mandatory
            data['paging_group']['VMServerID'] = None
            # finding the id of extension list to use
            extn_list = None
            for e_list in collections['no_mbox_user_extension_list']:
                if params['pg_extn_list'] == e_list['description']:
                    extn_list = e_list['id']
            data['paging_group']['ExtensionListID'] = extn_list
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'",'"')
        url = params.pop("url")
        log.info("Creating paging group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The paging group has been created successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not create paging group.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def edit_paging_group(self, pg_to_edit, **params):
        '''
        This function will edit a paging group
        phone system -> visual call flow editor -> Select paging group -> Edit
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("edit_paging_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, pg_to_edit)
        params['id'] = id
        pg_data = str(self.get_cosmo_component(act_id, part_id, params['componentType'], id=id))
        # the ast module could not convert data to its dictionary representation therefore using the json module
        if params.get('pg_name') is not None:
            temp = ast.literal_eval(pg_data)
            data = json.loads(temp['data'])
            data['paging_group']['dn_attributes']['Description'] = params['pg_name']
            data['paging_group']['dn_attributes']['DN_formatted'] = params['pg_extension']
            collections = data['collections']
            # finding the id of extension list to use
            extn_list = None
            for e_list in collections['no_mbox_user_extension_list']:
                if params['pg_extn_list'] == e_list['description']:
                    extn_list = e_list['id']
            data['paging_group']['ExtensionListID'] = extn_list
            # converting the dict back to string
            params['data'] = json.dumps(data)
        params['data'] = params['data'].replace("'", '"')
        url = params.pop("url")
        log.info("Creating paging group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The paging group has been edited successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not edit paging group.Message from server : <%s>" % ret.text)

        return result, ret

    @func_logger
    def delete_paging_group(self, pg_to_delete, **params):
        '''
        This function will delete a paging group
        phone system -> visual call flow editor -> Select paging group -> Delete
        :return: A tuple of a boolean status flag and the return object from the requested url

        '''
        result = False
        params_xml = self.config.getparams("delete_paging_group")
        params = self.get_param_to_use(params_xml, **params)
        if self.accountId is None:  # switch account has not been called
            act_id = self.get_account_detail(act_name=params['account_name'])
        else:
            act_id = self.accountId
        params["accountId"] = act_id
        if self.part_id is None:
            part_id = self.get_partition_detail(act_id, params['part_name'])
        else:
            part_id = self.part_id
        params["partitionId"] = part_id
        # getting the component id
        id = self.get_vcfe_detail(act_id, part_id, pg_to_delete)
        params['id'] = id
        params["profileLocationId"] = self.get_location_detail(act_id, params['location_name'])
        url = params.pop("url")
        log.info("Deleting paging group with args <%s>" % params)
        ret = requests.post(url, data=params, headers=self.headers)
        if ret.status_code == 200 and len(ret.text) == 2:
            log.info("The paging group has been deleted successfully.Message from server : <%s>" % ret.text)
            result = True
        else:
            log.error("Could not delete paging group.Message from server : <%s>" % ret.text)

        return result, ret

