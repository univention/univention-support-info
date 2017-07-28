#!/usr/bin/python
import sys
import os
import re
from ucr import UCR
from glob import glob


def segfaults_in_syslog(syslog_path, search_string):
#	   find segfaults in syslogfiles
	count = 0
	with open(syslog_path) as infile:
		for line in infile:
			m = search_string.match(line)
			if m:
				count += 1
	return count


def get_logfiles(filename):
	#logfiles einsammeln
	usi_path = sys.argv[1]
	path = os.path.join(usi_path, 'files')
	return glob(path + '/' + filename)

def logfile_count(search_string):
	status = 0
	syslogfiles = get_logfiles('var_log_syslog_*')
	for logfile in syslogfiles:
		#print (logfile)
		try:
			syslog_count = segfaults_in_syslog(logfile, search_string)
			if syslog_count > 0:
				print("'%s' enthaelt %s segfaults" % (logfile,syslog_count))
				status += 1
		except IOError as exc:
			print(repr(exc))
			print("Error opening '%s': %s" % (syslog_path, exc))
			return -1
	return status

def main():
	usi_path = sys.argv[1]
	search_string = re.compile(r'.*segfault.*',re.I)
	return logfile_count(search_string)


exit_status = main()
sys.exit(exit_status)

# vim: set ts=4 sw=4 tw=0 noet :
