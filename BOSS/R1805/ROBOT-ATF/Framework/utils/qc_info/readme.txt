Steps to generate xml, csv, and run set tcid list

1) Run tsids_to_tcids.py <project> <run type>
2) Run tcid_xml_to_csv.py <project> <run type>
3) Run csv_to_runset.py <testbedt type> <csv test data> <td status specifier>

TODO
----------

---------------------------
GET TEST SET INDEX
GET TEST SET INFO
---------------------------

To get the field index follow the procedure below. 

Step1 : Authenticate to http://percival.qa.shoretel.com/qcbin/authentication-point/login.jsp (QC Credentials) --> Navigates to blank page.
Step2 : Example Testcase ID 221795 -- http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/tests/221795
Same with testset  -- http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/test-instances?query={contains-test-set.id[$id]}&page-size=2000

You can get design steps given a test case id from url http://percival.qa.shoretel.com/qcbin/rest/domains/Default/projects/ShoreTel/design-steps?query={parent-id[$id]}  with previous procedure.

Populate ParentID txt file by find the parent ID via test set id
Navigating to test set 401379 with link below will show xml data for the test set. Find the parent-id in the xml
http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/test-sets?query={id[401379]}


You can get design steps given a test case id from url http://percival.qa.shoretel.com/qcbin/rest/domains/Default/projects/ShoreTel/design-steps?query={parent-id[$id]}  with previous procedure.
