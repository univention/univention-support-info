#!/usr/bin/python

import sys
import os
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN=[]

if ucr.get('kerberos/realm').lower() != ucr.get('domainname').lower():
	if (ucr.get('samba/role') == "DC"):
		RETURN.append('CRITICAL: Kerberos realm \'%s\' and DNS domainname \'%s\' does not match\n\tsamba role is \'%s\'' % (ucr.get('kerberos/realm'), ucr.get('domainname'), ucr.get('samba/role')))
	elif (ucr.get('samba4/role') == "DC"):
		RETURN.append('CRITICAL: Kerberos realm \'%s\' and DNS domainname \'%s\' does not match\n\tsamba4 role is \'%s\'' % (ucr.get('kerberos/realm'), ucr.get('domainname'), ucr.get('samba4/role')))
	else:
		if (ucr.get('samba/role') != None):
			RETURN.append('INFO: Kerberos realm \'%s\' and DNS domainname \'%s\' does not match\n\tdue to samba role \'%s\' this is not critical' % (ucr.get('kerberos/realm'), ucr.get('domainname'), ucr.get('samba/role')))
		elif (ucr.get('samba4/role') != None):
			RETURN.append('INFO: Kerberos realm \'%s\' and DNS domainname \'%s\' does not match\n\tdue to samba4 role \'%s\' this is not critical' % (ucr.get('kerberos/realm'), ucr.get('domainname'), ucr.get('samba4/role')))
		else:
			RETURN.append('WARNING: Kerberos realm \'%s\' and DNS domainname \'%s\' does not match\n\tSamba seems not installed (can not determine samba server role)!' % (ucr.get('kerberos/realm'), ucr.get('domainname')))

if RETURN:
	for line in RETURN:
		print line
	sys.exit(1)

# vim: set ts=4 sw=4 tw=0 noet :
