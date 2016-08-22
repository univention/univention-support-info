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


def segfaults_in_daemon(daemon_path, search_string):
#		find segfaults in daemonlog 
	count = 0
	with open(daemon_path) as infile:
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
				print('Syslogfile %s enthaelt %s segfaults' % (logfile,syslog_count))
				status += 1
		except IOError as exc:
			print(repr(exc))
			print('Error opening var_log_syslog file %s: %s' % (syslog_path, exc))
			return -1
	daemonlogfiles = get_logfiles('var_log_daemon_*')
	for logfile in daemonlogfiles:
		print (logfile)
		try:
			daemon_count = segfaults_in_daemon(logfiles, search_string)
			if daemon_count > 0:
				print('Daemon.log %s enthaelt %s segfaults' % (logfile, daemon_count))
				status += 2
		except IOError as exc:
			print(repr(exc))
			print('Error opening var_log_syslog file %s: %s' % (syslog_path, exc))
			return -1
	return status
	
def main():
	usi_path = sys.argv[1]
	search_string = re.compile(r'.*segfault.*',re.I)
	return logfile_count(search_string)


exit_status = main()
sys.exit(exit_status)

# vim: set ts=4 sw=4 tw=0 noet :
