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

# TODO replace line below with sys.path...
sys.path.append("C:\ATF_ROBOT\Framework\utils")
from robot.api.logger import console

class mapMgr:
    '''
        mapMgr parsers all the map file inside map directory and converts them into dictionary
    '''
    objRepository = {}
    objRepoList = []
    @staticmethod
    def create_maplist(component = "ManhattanComponent"):  
        try:
            #Listing all the file in the map directory
            if isinstance(component,str):
                if os.path.isdir("../map/"+component):
                    mapdirectory = "../map/"+component
                # if os.path.isdir(os.path.dirname(os.path.dirname(__file__))+"\\map\\"+component):
                    # mapdirectory = os.path.dirname(os.path.dirname(__file__))+"\\map\\"+component
                    # #console(mapdirectory)
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
                # console(mapMgr.objRepository[key])
                return mapMgr.objRepository[key]
        else:
                return None


if __name__ == "__main__":
    mapMgr.create_maplist("GsuiteComponent")
    mapDict = mapMgr.getMapDict()

    print (mapMgr.__getitem__('MAP_GOOGLE_USERNAME'))
    print  (mapMgr.getMapDict().keys())
    print (mapMgr.getMapDict()['MAP_GOOGLE_USERNAME'])
