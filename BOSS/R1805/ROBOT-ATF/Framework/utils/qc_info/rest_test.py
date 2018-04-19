
import requests
session = requests.session()
user='mvilleda'
password=''
r = session.get("http://bill.qa.shoretel.com/qcbin/authentication-point/authenticate",auth=(user,password))
r = session.get("http://bill.qa.shoretel.com/qcbin/rest/domains/DEFAULT/projects/ShoreTel/test-sets/400706?login-form-required=y\")

r = session.get("http://bill.qa.shoretel.com/qcbin/rest/domains/DEFAULT/projects/ShoreTel/requirements/1202")
r = session.get("http://bill.qa.shoretel.com/qcbin/rest/domains/DEFAULT/projects/ShoreTel/Root/")

r.text

td://shoretel.default.frodo.qa.shoretel.com/qcbin/[AnyModule]?EntityType=ITestSetFolder&EntityID=144914

http://bill.qa.shoretel.com/qcbin/rest/domains/DEFAULT/projects/ShoreTel/test-set-folders?query={name['Root/]}


http://bill.qa.shoretel.com/qcbin/rest/domains/DEFAULT/projects/ShoreTel/test-set-folders?query={name['Subject/]}



td://shoretel.default.frodo.qa.shoretel.com/qcbin/[AnyModule]?EntityType=ITestFolder&EntityID=39702

r = session.get("http://bill.qa.shoretel.com/qcbin/rest/domains/DEFAULT/projects/ShoreTel/test-set-folders?query={name['Root/]}")

r = session.get("")


import pywintypes
import win32com.client as w32c
from win32com.client import gencache, DispatchWithEvents, constants

qc = w32c.Dispatch("TDApiole80.TDConnection");
qc.InitConnectionEx(server); 


server= r"https://bill.qa.shoretel.com/qcbin"
username= "mvilleda"
password= ""
domainname= "DEFAULT"
projectname= "ShoreTel"

 
