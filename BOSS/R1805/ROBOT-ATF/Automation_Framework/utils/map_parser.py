###############################################################################
## Module: map_parser
## File name: map_parser.py
## Description: Map files parser class
##
##
##  -----------------------------------------------------------------------
##  Modification log:
##
##  Date        Engineer            Description
##  ---------   ---------        -----------------------
##  12-AUG-14    VHA                  created
################################################################################

import re
import os
import sys
#sys.path.append('../log')
#from StafLogger import StafLogger

class mapParser:
    """ mapParser class is used to read and write configuration files. """

    def __init__(self, filename=None, rtool=None):
        
        """ 1 map and 1 list is used to maintain an ordered map"""
        self.map_dict={}
        self.map_key_list=[]
        self.rtool = rtool
        if filename == None:
            print ("File name not mentioned")
            return None
      
        try:		
            fileobj = open(filename, "r")
            other_value_line_count=0
            for line in fileobj:
                if '==' in line: 
                    eleList = line.split('==')
                    if len(eleList) >= 2:
                        # Remove \n and leading and trailing spaces from value and then save
                        value_parts = [ele.strip() for ele in eleList[1].split('#')]
                        key = eleList[0].strip()

                        self.map_key_list.append(key)
                        self.map_dict[key] = {
                                        "ELEMENT_TYPE"    : value_parts[0],
                                        "BY_TYPE"        : value_parts[1],
                                        "BY_VALUE"        : value_parts[2]
                                    }
                
                if len(value_parts) > 3:
                    self.map_dict[key]["INDEX"] = int(value_parts[3])
                else:
                    key = 'other_value_line_count_' + str(other_value_line_count)
                    other_value_line_count = other_value_line_count + 1
                    self.map_dict[key] = line
                    self.map_key_list.append(key)
            fileobj.close()	
                            
        except :
            msg = "mapParser errorr " + str(sys.exc_info())
            print(msg) 
            raise Exception
                        
    def __str__(self):	
        ret_str = ""
        for key in self.map_key_list:
                value = self.map_dict[key]
    #		print " * * * * kay=", key, " value =",  value
                if re.search("other_value_line_count", key):
                        ret_str = ret_str + str(value)
                else:
                        ret_str = ret_str + str(key) + '=' + str(value) + '\n'
        #print ret_str
        return ret_str

    def __getitem__(self,key):
        if key in list(self.map_dict.keys()):
                return self.map_dict[key]
        else:
                return None

    def __setitem__(self, key, value):
        self.map_dict[key] = str(value).strip()
        if not key in self.map_key_list: self.map_key_list.append(key)

    def remove(self, key):
        value = None
        if key in self.config.key_list:
                value = self.map_dict[key]
                self.map_key_list.remove(key)
                del self.map_dict[key]

    def update_dictionary(self, param_dict):
        for key in param_dict.keys():
            self.map_dict[key]=param_dict[key]
        #print(self.map_dict['$mdn_post'],param_dict['$mdn_post'])
        
    def write(self, fileobj):
        fileobj.write(str(self))
	
if __name__ == "__main__":
    #conf_file_name = os.path.join(os.pardir(), "/map/Login.map")
    print (os.getcwd())
    #conf_file_name = "F:\\PaxterraKT\STAF\map\Login.map"
    conf_file_name="..\\map\\Login.map"
    confManager = mapParser(conf_file_name)
    print(confManager['Login_Password'])

	
