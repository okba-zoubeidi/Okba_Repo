from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree
from lxml import objectify
import time
import sys
import re
import os

__author__ = "mvilleda"

fields = ["id", "user-14", "user-08",
			"name",	"status", "user-18",
			"user-02", "user-15", "owner",
			"user-01", "user-04", "user-05",
			"subtype-id", "user-03", "user-06"]
			
items = ["tcid","base_release","auto_suite",
		"test_name","status","auto_mt_status",
		"auto_st_status","auto_base","designer","priority",
		"scope","keyword_high_level","type",
		"usage","keyword_specific"]
		

if len(sys.argv) < 3:
	print """\
	Usage:  tcid_xml_to_csv.py <automation project> <run type>
	example:  tcid_xml_to_csv.py gsuite st_bco
	
	run type: st_bco, mt_bco, st_regression, mt_regression
	"""
	sys.exit() 
	
project = sys.argv[1]
testset_type = sys.argv[2]

new_dir = project + "_" + testset_type
result_dir = os.path.join(project,new_dir)

tcidcsv_outfile = project + "_" + testset_type + "_tcid.csv"
tcidcsv_path = os.path.join(result_dir,tcidcsv_outfile)
tcid_dir = result_dir

def print_tcid_field_data(infile,keys):
	fname = os.path.join(tcid_dir,infile)
	print "LXML Parsing file %s" % fname

	tree = etree.parse(fname)

	for key in fields:
		val = tree.xpath('//Entity/Fields/Field[@Name="%s"]/Value/text()' % key)	

		print "%s : %s" % (key,val)

def tcid_field_data_to_csv(infile,keys):
	fname = os.path.join(tcid_dir,infile)
	print "LXML Parsing file %s" % fname
	
	parser = etree.XMLParser(recover=True)
	tree = etree.parse(fname,parser)
	fh_w = open(tcidcsv_path, "a")

	for key in fields:
		val = str(tree.xpath('//Entity/Fields/Field[@Name="%s"]/Value/text()' % key)	)

		v = val[1:-1]
		#ignore commas in field name
		v = re.sub(',','',v)
		# print v
		fh_w.write("%s," % v)
	fh_w.write('\n')
	fh_w.close()

def dump_tcid_field_info(driver):
	tree = etree.parse(infile)
	url = "http://percival.qa.shoretel.com/qcbin/rest/domains/default/projects/ShoreTel/tests/256169"
	driver.get(url)
	print tree.xpath('//Entity[0]/Fields/@Name')	
			

if  __name__ in "__main__":
	print "*** Program START ***"
	# print "Reading tcid info from %s infile" % tsid_infile
	if os.path.isfile(tcidcsv_path):
		os.remove(tcidcsv_path)
	with open(tcidcsv_path, "w") as fh_w:
		#populate header
		for item in items:
			fh_w.write(item + ",")
		fh_w.write('\n')

	#PARSE FILES AND GEN RUN SET
	for filename in os.listdir(tcid_dir):
		if filename.endswith(".xml"):
			if filename.split(".")[0].isdigit():
				# only process tcid xml files
				tcid_field_data_to_csv(filename,fields)
	
	print "*** Program COMPLETE ***"
