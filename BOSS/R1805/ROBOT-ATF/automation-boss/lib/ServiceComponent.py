"""Module for Service page
   Developer: Megha Bansal
"""


class ServiceComponent(object):
    ''' Module for Service page
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def close_service(self, **params):
        '''
        `Description:` This Function will close the service
        `Param:` Dictionary contains service information
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            result = self.boss_page.service.close_service(params)
            return result
        except:
            print("Could not access link", self.close_service.__doc__)
            raise AssertionError("Close Service failed!!")


    def void_global_user_service(self, **params):
        '''
        `Description:` This Function will void the global user service
        `Param:` Dictionary contains service information
        `Returns: ` result - True/False
        `Created by:` Megha Bansal
        '''
        try:
            serviceTn, result = self.boss_page.service.void_global_user_service(params)
            return serviceTn, result
        except:
            print("Could not access link", self.void_global_user_service.__doc__)
            raise AssertionError("Void Global user Service failed!!")
