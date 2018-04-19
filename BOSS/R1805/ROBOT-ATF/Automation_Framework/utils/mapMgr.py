###############################################################################
## Module: mapMgr
## File name: mapMgr.py
## Description: Map files manager class
##
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer            Description
##  ---------   ---------        -----------------------
##  12-AUG-14    VHA                  created
##  25-AUG-14    VHA                  Added support for highball & UCB components 
###############################################################################
import os
import sys
from map_parser import mapParser

from robot.api.logger import console

class mapMgr:
    '''
        mapMgr parsers all the map file inside map directory and converts them into dictionary
    '''
    objRepository = {}
    objRepoList = []
    @staticmethod
    def create_maplist(component = "ManhattanClient"):
        try:
            #Listing all the file in the map directory
            if isinstance(component,str):
                if os.path.isdir("../map/"+component):
                    mapdirectory = "../map/"+component
                else:
                    raise AssertionError("Directory not found %s" %component)
           
            
            for dirname, dirnames, filenames in os.walk(mapdirectory):
                pass
            filelist = [os.path.join(dirname, filename) for filename in filenames]           
                 
            for file in filelist:
                #Parsing single map file and updating objRepository dictionary
                map_obj = mapParser(file)
                mapMgr.objRepository.update(map_obj.map_dict)
                mapMgr.objRepoList.append(map_obj.map_key_list)
            #print (mapMgr.objRepository)
        except:
            return False
        
    #Method to get objList
    @staticmethod
    def getMapKeyList():
        return mapMgr.objRepoList
    #Method to get objDictionary
    @staticmethod
    def getMapDict():        
        return mapMgr.objRepository
    #Method to get element from objRepository
    @staticmethod
    def __getitem__(key):
        if key in list(mapMgr.objRepository.keys()):
                return mapMgr.objRepository[key]
        else:
                return None


if __name__ == "__main__":
    mapMgr.create_maplist()
    print (mapMgr.__getitem__('Login_Password'))
    print (mapMgr.getMapDict()['Login1_Password'])
