import re
import sys
import os
import csv
from collections import defaultdict
import time

__author__ = "mvilleda"

if len(sys.argv) < 4:
	print """\
	Usage:  csv_to_runset.py <st or mt> <csv file> <test status> 
	example:  csv_to_runset.py st some_csv_file.csv Done
	
	test statuses: Scripted, Done, Blocked, In Progress, Future, Declined, Candidate
	Notes: Case sensitive. If there is no output on std out then something went wrong
	"""
	sys.exit() 
	

ST_or_MT = sys.argv[1]
infile = sys.argv[2]
test_status = sys.argv[3]
outfile = infile.split('.')[0] + "_" + test_status +".txt"



states  = ["Scripted", "Done", "Blocked", "In Progress", "Future", "Declined", "Candidate"]
fields = ["auto_mt_status", "auto_st_status"]
output = []
count = 0

f = open( infile, 'rU' ) #open the file in read universal mode
firstline = f.readline()

if "st" in ST_or_MT:
	status_index = firstline.split(",").index("auto_st_status")
else:
	status_index = firstline.split(",").index("auto_mt_status")

fh = open(outfile, 'w')
print "Converting csv file \"%s\" to tcid run set file \"%s\"" % (infile,outfile)
for line in f:
	cells = line.split( "," )
	if test_status in cells[status_index]:
		count = count + 1
		tcid = cells[0].strip("\'")
		print "%s : %s" %(test_status,tcid)
		fh.write(tcid+'\n')

f.close()
fh.close()

print "%s tcids found. Exiting..." % count

