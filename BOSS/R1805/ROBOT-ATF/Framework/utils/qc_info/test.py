
import requests
session = requests.session()
user='mvilleda'
password=''
r = session.get("http://bill.qa.shoretel.com/qcbin/authentication-point/authenticate",auth=(user,password))
r = session.get("http://bill.qa.shoretel.com/qcbin/rest/domains/DEFAULT/projects/ShoreTel/test-sets/400706?login-form-required=y")

print r.text