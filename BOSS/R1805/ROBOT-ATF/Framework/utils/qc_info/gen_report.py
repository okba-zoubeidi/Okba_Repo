import re, sys
import os, glob
import csv
from collections import defaultdict
import time
import time

#Run 

fields = ["id", "user-14", "user-08",
			"name",	"status", "user-18",
			"subtype-id", "user-15", "owner",
			"user-01", "user-04", "user-05",
			"user-02", "user-03", "user-06"]

setups = ["st", "mt"]
states  = ["Scripted", "Done", "Blocked", "In Progress", "Future", "Declined", "Candidate"]
fields = ["auto_mt_status", "auto_st_status"]
count  = [ 0, 0, 0, 0, 0, 0, 0]
bco_totals  = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]
regr_totals  = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]

infile = 'gapps_st_bco.csv'

columns = defaultdict(list) # each value in each column is appended to a list

with open(infile) as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

print "Scripted, Done, Blocked, In Progress, Future, Declined, Candidate"								 
# print(columns['auto_st_status'])
#Count occurences and generate csv
count[0] = columns['auto_st_status'].count(states[0])
count[1] = columns['auto_st_status'].count(states[1])
count[2] = columns['auto_st_status'].count(states[2])
count[3] = columns['auto_st_status'].count(states[3])
count[4] = columns['auto_st_status'].count(states[4])
count[5] = columns['auto_st_status'].count(states[5])
count[6] = columns['auto_st_status'].count(states[6])

path, dirs, files = os.walk("st_bco").next()
file_count = len(files)
total = file_count 
unknown = total

for i in range(0,7):
	bco_totals[i] = count[i]

bco_totals[7] = total

for i in range(0,7):
	unknown -= count[i]

bco_totals[8] = unknown
	
print str(count[0]) + ", " + str(count[1]) + ", " + str(count[2]) + ", " + str(count[3]) + ", " + str(count[4]) + ", " + str(count[5]) + ", " + str(count[6])
print "ST BCO Total: %s" % total

#Print html table
fh = open('weekly_report.html', 'w')
fh.write("<html><body>")
fh.write("<hr><h2 align=\"center\">BCO Test Cases</h2>")
fh.write("<p>Time Generated: " + time.strftime("%m/%d/%Y %H:%M") + "</p>")

fh.write("<table border=\"1\">")
# fh.write("<tr><th>BCO Test Cases</th></tr>")
fh.write("<tr bgcolor=\"#FFCC99\"><th>  Setup  </th><th>Total Tests</th><th>Accepted (Done)</th><th>Ready for Review (Scripted)</th><th>Waiting for API (Blocked)</th><th>Scripting/Re-work (In progress)</th><th>May be implementable (Future)</th><th>Not Automatable (Declined)</th><th>Ready to be Scripted (Candidate)</th><th>Not a Candidate (Unknown)</th></tr>")
fh.write("<tr><td align=\"center\">ST BCO</td><td align=\"center\">" + str(total) + "</td><td align=\"center\">" + str(count[1]) + "</td><td align=\"center\">" + str(count[0]) + "</td><td align=\"center\">" + str(count[2]) + "</td><td align=\"center\">" + str(count[3]) + "</td><td align=\"center\">" + str(count[4]) + "</td><td align=\"center\">" + str(count[5]) + "</td><td align=\"center\">" + str(count[6]) + "</td><td align=\"center\">" + str(unknown) + "</td></tr>")


infile = 'gapps_mt_bco.csv'
columns = defaultdict(list) # each value in each column is appended to a list

with open(infile) as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

# print(columns['auto_st_status'])
#Count occurences and generate csv
count[0] = columns['auto_mt_status'].count(states[0])
count[1] = columns['auto_mt_status'].count(states[1])
count[2] = columns['auto_mt_status'].count(states[2])
count[3] = columns['auto_mt_status'].count(states[3])
count[4] = columns['auto_mt_status'].count(states[4])
count[5] = columns['auto_mt_status'].count(states[5])
count[6] = columns['auto_mt_status'].count(states[6])

path, dirs, files = os.walk("mt_bco").next()
file_count = len(files)
total = file_count 
unknown = total

for i in range(0,7):
	bco_totals[i] += count[i]

bco_totals[7] += total

for i in range(0,7):
	unknown -= count[i]
	
bco_totals[8] += unknown

print str(count[0]) + ", " + str(count[1]) + ", " + str(count[2]) + ", " + str(count[3]) + ", " + str(count[4]) + ", " + str(count[5]) + ", " + str(count[6])
print "MT BCO Total: %s" % total

#Add mt bco to weekly report
fh.write("<tr><td align=\"center\">MT BCO</td><td align=\"center\">" + str(total) + "</td><td align=\"center\">" + str(count[1]) + "</td><td align=\"center\">" + str(count[0]) + "</td><td align=\"center\">" + str(count[2]) + "</td><td align=\"center\">" + str(count[3]) + "</td><td align=\"center\">" + str(count[4]) + "</td><td align=\"center\">" + str(count[5]) + "</td><td align=\"center\">" + str(count[6]) + "</td><td align=\"center\">" + str(unknown) + "</td></tr>")
#Add totals to weekly report
fh.write("<tr bgcolor=\"CCCCCC\"><td align=\"center\">Total</td><td align=\"center\">" + str(bco_totals[7]) + "</td><td align=\"center\">" + str(bco_totals[1]) + "</td><td align=\"center\">" + str(bco_totals[0]) + "</td><td align=\"center\">" + str(bco_totals[2]) + "</td><td align=\"center\">" + str(bco_totals[3]) + "</td><td align=\"center\">" + str(bco_totals[4]) + "</td><td align=\"center\">" + str(bco_totals[5]) + "</td><td align=\"center\">" + str(bco_totals[6]) + "</td><td align=\"center\">" + str(bco_totals[8]) + "</td></tr>")

fh.write("</table>")


infile = 'gapps_st_regr.csv'
columns = defaultdict(list) # each value in each column is appended to a list

with open(infile) as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

# print(columns['auto_st_status'])
#Count occurences and generate csv
count[0] = columns['auto_st_status'].count(states[0])
count[1] = columns['auto_st_status'].count(states[1])
count[2] = columns['auto_st_status'].count(states[2])
count[3] = columns['auto_st_status'].count(states[3])
count[4] = columns['auto_st_status'].count(states[4])
count[5] = columns['auto_st_status'].count(states[5])
count[6] = columns['auto_st_status'].count(states[6])

path, dirs, files = os.walk("st_regr").next()
file_count = len(files)
total = file_count 
unknown = total

for i in range(0,7):
	bco_totals[i] = count[i]

bco_totals[7] = total

for i in range(0,7):
	unknown -= count[i]
	
bco_totals[8] = unknown
	
print str(count[0]) + ", " + str(count[1]) + ", " + str(count[2]) + ", " + str(count[3]) + ", " + str(count[4]) + ", " + str(count[5]) + ", " + str(count[6])
print "ST Regr Total: %s" % total

fh.write("<br>")
fh.write("<br>")

fh.write("<hr><h2 align=\"center\">Regression Test Cases</h2>")
fh.write("<p>Time Generated: " + time.strftime("%m/%d/%Y %H:%M") + "</p>")

fh.write("<table border=\"1\">")
# fh.write("<tr><th>BCO Test Cases</th></tr>")
fh.write("<tr bgcolor=\"#FFCC99\"><th>Setup</th><th>Total Tests</th><th>Accepted (Done)</th><th>Ready for Review (Scripted)</th><th>Waiting for API (Blocked)</th><th>Scripting/Re-work (In progress)</th><th>May be implementable (Future)</th><th>Not Automatable (Declined)</th><th>Ready to be Scripted (Candidate)</th><th>Not a Candidate (Unknown)</th></tr>")
fh.write("<tr><td align=\"center\">ST Regression</td><td align=\"center\">" + str(total) + "</td><td align=\"center\">" + str(count[1]) + "</td><td align=\"center\">" + str(count[0]) + "</td><td align=\"center\">" + str(count[2]) + "</td><td align=\"center\">" + str(count[3]) + "</td><td align=\"center\">" + str(count[4]) + "</td><td align=\"center\">" + str(count[5]) + "</td><td align=\"center\">" + str(count[6]) + "</td><td align=\"center\">" + str(unknown) + "</td></tr>")


infile = 'gapps_mt_regr.csv'
columns = defaultdict(list) # each value in each column is appended to a list

with open(infile) as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

#Count occurences and generate csv
# print(columns['auto_st_status'])
count[0] = columns['auto_mt_status'].count(states[0])
count[1] = columns['auto_mt_status'].count(states[1])
count[2] = columns['auto_mt_status'].count(states[2])
count[3] = columns['auto_mt_status'].count(states[3])
count[4] = columns['auto_mt_status'].count(states[4])
count[5] = columns['auto_mt_status'].count(states[5])
count[6] = columns['auto_mt_status'].count(states[6])

path, dirs, files = os.walk("mt_regr").next()
file_count = len(files)
total = file_count 
unknown = total

for i in range(0,7):
	bco_totals[i] += count[i]

bco_totals[7] += total

for i in range(0,7):
	unknown -= count[i]
	
bco_totals[8] += unknown
	
print str(count[0]) + ", " + str(count[1]) + ", " + str(count[2]) + ", " + str(count[3]) + ", " + str(count[4]) + ", " + str(count[5]) + ", " + str(count[6])
print "MT Regr Total: %s" % total
	
fh.write("<tr><td align=\"center\">MT Regression</td><td align=\"center\">" + str(total) + "</td><td align=\"center\">" + str(count[1]) + "</td><td align=\"center\">" + str(count[0]) + "</td><td align=\"center\">" + str(count[2]) + "</td><td align=\"center\">" + str(count[3]) + "</td><td align=\"center\">" + str(count[4]) + "</td><td align=\"center\">" + str(count[5]) + "</td><td align=\"center\">" + str(count[6]) + "</td><td align=\"center\">" + str(unknown) + "</td></tr>")
#Add totals to weekly report
fh.write("<tr bgcolor=\"CCCCCC\"><td align=\"center\">Total</td><td align=\"center\">" + str(bco_totals[7]) + "</td><td align=\"center\">" + str(bco_totals[1]) + "</td><td align=\"center\">" + str(bco_totals[0]) + "</td><td align=\"center\">" + str(bco_totals[2]) + "</td><td align=\"center\">" + str(bco_totals[3]) + "</td><td align=\"center\">" + str(bco_totals[4]) + "</td><td align=\"center\">" + str(bco_totals[5]) + "</td><td align=\"center\">" + str(bco_totals[6]) + "</td><td align=\"center\">" + str(bco_totals[8]) + "</td></tr>")

fh.write("</table></body></html>")
fh.close()

