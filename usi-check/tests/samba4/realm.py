#!/usr/bin/python

import sys
import os
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN=[]

if ucr.get('kerberos/realm').lower() != ucr.get('domainname').lower():
	if ucr.get('samba/role') == "DC":
		RETURN.append('CRITICAL: Kerberos realm \'%s\' and DNS domainname \'%s\' does not match\n\tsamba role is \'%s\'' % (ucr.get('kerberos/realm'), ucr.get('domainname'), ucr.get('samba/role')))
	else:
		RETURN.append('INFO: Kerberos realm \'%s\' and DNS domainname \'%s\' does not match\n\tdue to samba role \'%s\' this is not critical' % (ucr.get('kerberos/realm'), ucr.get('domainname'), ucr.get('samba/role')))

if RETURN:
	for line in RETURN:
		print line
	sys.exit(1)


# vim: set ts=4 sw=4 tw=0 noet :
