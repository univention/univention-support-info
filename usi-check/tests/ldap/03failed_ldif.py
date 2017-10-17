#!/usr/bin/python
import sys
import os
import re 
from ucr import UCR
from glob import glob


def failed_ldif_in_listener(listener_path, search_failed_ldif_string):
#		find failed.ldif message in listener.log 
	count = 0
	with open(listener_path) as infile:
		for line in infile:
			m = search_failed_ldif_string.match(line)
			if m:
				count += 1
	return count

def get_logfiles(filename):
	#logfiles einsammeln
	usi_path = sys.argv[1]
	path = os.path.join(usi_path, 'files')
	return glob(path + '/' + filename)

def logfile_count(search_failed_ldif_string):
	status = 0
	listenerlogfiles = get_logfiles('var_log_univention_listener.log_*')
	for logfile in listenerlogfiles:
		#print (logfile)
		try:
			failed_count = failed_ldif_in_listener(logfile, search_failed_ldif_string)
			if failed_count > 0:
				print('Listener.log %s enthaelt %s failed.ldifs' % (logfile, failed_count))
				status += 1
		except IOError as exc:
			print(repr(exc))
			print('Error opening var_log_univention_listener.log file %s: %s' % (listener_path, exc))
			return -1
	if status > 0:
		print ("We have a sdb-article for this issue: https://help.univention.com/t/what-to-do-if-a-failed-ldif-is-found/6432") 
	return status
	
def main():
	usi_path = sys.argv[1]
	search_failed_ldif_string = re.compile(r'.*\'failed.ldif\'\ exists\.\ Check\ for\ \/var\/lib\/univention-directory-replication\/failed.ldif.*',re.I)
	return logfile_count(search_failed_ldif_string)


exit_status = main()
sys.exit(exit_status)
#sys.exit(1)

# vim: set ts=4 sw=4 tw=0 noet :
