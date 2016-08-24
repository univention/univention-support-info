#!/usr/bin/python
import sys
import os
import re 
from ucr import UCR
from glob import glob


def servfail_in_daemon(daemon_path, search_daemon_string):
#		find segfaults in daemonlog 
	count = 0
	with open(daemon_path) as infile:
		for line in infile:
			m = search_daemon_string.match(line)
			if m:
				count += 1
	return count

def get_logfiles(filename):
	#logfiles einsammeln
	usi_path = sys.argv[1]
	path = os.path.join(usi_path, 'files')
	return glob(path + '/' + filename)

def logfile_count(search_daemon_string):
	status = 0
	daemonlogfiles = get_logfiles('var_log_daemon.log_*')
	for logfile in daemonlogfiles:
		print (logfile)
		try:
			daemon_count = servfail_in_daemon(logfile, search_daemon_string)
			if daemon_count > 0:
				print('Daemon.log %s enthaelt %s SERVFAILS' % (logfile, daemon_count))
				status += 1
		except IOError as exc:
			print(repr(exc))
			print('Error opening var_log_syslog file %s: %s' % (syslog_path, exc))
			return -1
	if status > 0:
		print ("We have a sdb-article for this issue: http://sdb.univention.de/1273") 
	return status
	
def main():
	usi_path = sys.argv[1]
	search_daemon_string = re.compile(r'.*unexpected\ rcode\ \(SERVFAIL\).*',re.I)
	return logfile_count(search_daemon_string)


exit_status = main()
sys.exit(exit_status)

# vim: set ts=4 sw=4 tw=0 noet :
