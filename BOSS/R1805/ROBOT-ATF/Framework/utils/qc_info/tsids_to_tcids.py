from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree
from lxml import objectify
import time
import sys
import re
import os

__author__ = "mvilleda"

QC_SiteURL = "http://percival.qa.shoretel.com/qcbin/authentication-point/login.jsp"
QC_TITLE = "HP ALM - Quality Center"
qc_LoginName_Locator = "j_username"
qc_LoginName = "mvilleda"
Parent_TestSetInfoURL = "http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/test-sets?query={parent-id[##PID##]}"
TestSetInfoURL = "http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/test-instances?query={contains-test-set.id[##TSID##]}&page-size=2000"

TestcaseInfoURL = "http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/tests/"


if len(sys.argv) < 3:
	print """\
	Usage:  tsids_to_tcids.py <automation project> <run type>
	example:  tsids_to_tcids.py gsuite st_bco
	
	run type: st_bco, mt_bco, st_regression, mt_regression
	"""
	sys.exit() 
	
project = sys.argv[1]
testset_type = sys.argv[2]

fname = "tsid.xml"
new_dir = project + "_" + testset_type
result_dir = os.path.join(project,new_dir)

parentID_list = project + "_parentIDs.txt"
parentID_infile =  os.path.join(project ,parentID_list)

tsidxml_fname = "tsid_list.xml"
tsidlist_fname = "tsid_list.txt"
tsidxml_outfile = os.path.join(result_dir,tsidxml_fname)
tsidlist_outfile = os.path.join(result_dir,tsidlist_fname)

tsidtmpxml_outfile = "tsid.xml"
tsidtmp_outfile = os.path.join(result_dir,tsidtmpxml_outfile)
tcid_fname = "tcids.txt"
tcid_infile = os.path.join(result_dir,tcid_fname)

def login_to_QC(driver):
	driver.get(QC_SiteURL)
	assert QC_TITLE in driver.title
	elem = driver.find_element_by_name(qc_LoginName_Locator)
	elem.clear()
	elem.send_keys(qc_LoginName)
	elem.send_keys(Keys.RETURN)
	time.sleep(4)

def  copy_page_bodytext(driver,outfile):
	elem = driver.find_element_by_css_selector("body")
	time.sleep(2)
	elem.send_keys(Keys.CONTROL + 'a')

	# Todo - improve this efficiency 
	with open("tmp.xml", 'w') as fh:
		fh.write(elem.text)
		
	with open("tmp.xml", 'r') as fhr:
		with open(outfile, 'w') as fh:
			fhr.next()
			for line in fhr:
				fh.write(line)


def  save_page_bodytext(driver,outfile):
	elem = driver.find_element_by_css_selector("body")
	time.sleep(2)
	elem.send_keys(Keys.CONTROL + 'a')

	# Todo - improve this efficiency 
	with open("tmp.xml", 'w') as fh:
		fh.write(elem.text)
		
	outf = os.path.join(result_dir,outfile)
	print "Writing xml file \"%s\"" % outf
	with open("tmp.xml", 'r') as fhr:
		with open(outf, 'w') as fh:
			fhr.next()
			for line in fhr:
				fh.write(line)


def scrape_tsid_data(infile,outfile):
	print "LXML Parsing file %s" % infile
	parser = etree.XMLParser(recover=True)
	tree = etree.parse(infile,parser)

	totalTests = tree.xpath("//Entities/@TotalResults")

	# Todo - improve this section
	tcid = [None] * 32
	owner = [None] * 32
	name = [None] * 32
	status = [None] * 32
	test_instance = {}
	for i in range(1,int(totalTests[0]) + 1):
		j = i - 1
		tcid[i] = str(tree.xpath('//Entity[%s]/Fields/Field[@Name="%s"]/Value/text()' % (i,"test-id")))	
		owner[i] = tree.xpath('//Entity[%s]/Fields/Field[@Name="%s"]/Value/text()' % (i,"owner"))
		name[i] = tree.xpath('//Entity[%s]/Fields/Field[@Name="%s"]/Value/text()' % (i,"name"))
		status[i] = tree.xpath('//Entity[%s]/Fields/Field[@Name="%s"]/Value/text()' % (i,"status"))
		
		tcid_i = re.findall(r"\d{6}",tcid[i])[0]
		print tcid_i
		with open(outfile, 'a') as fh:
			fh.write(tcid_i + '\n')

# def navigate_to_url(url):
	# driver.get(url)	
	
def dump_tsid_field_info(driver):
	url = "http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/tests/256169"
	driver.get(url)
	print 	tree.xpath('//Entity[%s]/Fields')	

def dump_tcid_field_info(driver):
	tree = etree.parse(infile)
	url = "http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/tests/256169"
	driver.get(url)
	print tree.xpath('//Entity[0]/Fields/@Name')	


def write_tcids_xml():
	#WRITE TCID QC INFO TO FILE
	with open(tcid_infile) as fh_in:
		for i, line in enumerate(fh_in):
			tcid_url = TestcaseInfoURL + line # str(re.findall(r"\d{6}",line))
			# print tcid_url
			driver.get(tcid_url)
			
def get_parent_id(testset_type,infile):
	with open(infile) as fh_in:
		for i, line in enumerate(fh_in):
			if testset_type in line:
				id = line.split('=')[1]
				return id.strip()

def generate_tsids_from_parentid(driver,id, outfile):
	#GENERATE TSIDS
	url = Parent_TestSetInfoURL.replace("##PID##",str(id))
	driver.get(url)
	copy_page_bodytext(driver, tsidxml_outfile)
	
	print "LXML Parsing file %s" % tsidxml_outfile
	tree = etree.parse(tsidxml_outfile)

	totalSets = tree.xpath("//Entities/@TotalResults")
	print "%s total test sets found..." % totalSets
	# Todo - improve this section
	print "Deleting tsid list to \"%s\"" % outfile
	if os.path.isfile(outfile):
		os.remove(outfile)
	print "Writing tsid list to \"%s\"" % outfile
	for i in range(1,int(totalSets[0]) + 1):
		id = str(tree.xpath('//Entity[%s]/Fields/Field[@Name="%s"]/Value/text()' % (i,"id")))	
		# tcid_i = re.findall(r"\d{6}",tcid)
		tsid = id.strip("]'[")
		with open(outfile, 'a') as fh:
			fh.write(tsid + '\n')
			
def generate_tcids_file(driver, tsids,tsid_count, infile):
	#GENERATE TCIDS
	print "Removing tcids list \"%s\"" % infile 
	for i in range(0,tsid_count):
		if tsids[i] == '':
			break
		print "*** TSID %s ***" % tsids[i]
		tsid_url = TestSetInfoURL.replace("##TSID##",str(tsids[i]))
		driver.get(tsid_url)
		copy_page_bodytext(driver, tsidtmp_outfile)
		time.sleep(2)
		scrape_tsid_data(tsidtmp_outfile, infile)

	

if  __name__ in "__main__":
	tsids = [None] * 128
	tsid_count = 0

	print "*** Program START ***"
	if not os.path.exists(result_dir):
		os.makedirs(result_dir)
	
	print "Reading Parent ID to extract %s tsids from \"%s\"" % (testset_type,parentID_infile)
	parent_id = get_parent_id(testset_type,parentID_infile)
	print "Searching parent ID \"%s\"" % parent_id
	
	driver = webdriver.Chrome()
	login_to_QC(driver)
	
	generate_tsids_from_parentid(driver,parent_id,tsidlist_outfile)
	
	with open(tsidlist_outfile) as fh_in:
		for i, line in enumerate(fh_in):
			if "#" in line:
				continue
			tsids[tsid_count] = line.replace("\n","")
			tsid_count = tsid_count + 1
	# print tsids

	generate_tcids_file(driver,tsids,tsid_count,tcid_infile)
	
	# write_tcids_xml()
	#WRITE TCID QC INFO TO FILE
	with open(tcid_infile) as fh_in:
		for i, line in enumerate(fh_in):
			tcid_url = TestcaseInfoURL + line
			# print tcid_url
			driver.get(tcid_url)
			tc_fname = line.replace("\n","") + ".xml"
			save_page_bodytext(driver, tc_fname)

	print "*** Program COMPLETE ***"
	driver.close()