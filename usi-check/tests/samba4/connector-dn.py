#!/usr/bin/python

import sys
import os
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN=[]

if ucr.get('connector/s4/autostart', 'no').lower() in ('yes', 'true', '1'):
	if ucr.get('connector/ldap/binddn', 'none').lower() not in ('none',  ucr.get('ldap/hostdn')):
		RETURN.append('WARNING: LDAP Host-DN and S4-Connector Bind-DN does not match!')

if RETURN:
	for line in RETURN:
		print line
	sys.exit(1)


# vim: set ts=4 sw=4 tw=0 noet :
