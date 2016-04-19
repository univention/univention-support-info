#!/usr/bin/python

import sys
import os
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN=[]

RETURN.append("UCS Version:  %s-%s-Errata%s" % (ucr.get('version/version'), ucr.get('version/patchlevel'), ucr.get('version/erratalevel'))) 
RETURN.append("Server Rolle: %s" % (ucr.get('server/role')))

#if samba is running display samba role
if (ucr.get('samba/role') != "" and ucr.get('samba/role') != None):
  RETURN.append("Samba Rolle:  %s" % (ucr.get('samba/role')))

#if samba4 is running display samba role
if (ucr.get('samba4/role') != "" and ucr.get('samba4/role') != None):
  RETURN.append("Samba4 Rolle: %s" % (ucr.get('samba4/role')))

if RETURN:
	for line in RETURN:
		print line
else:
	print("Error while parsing ucr")

sys.exit(1)

# vim: set ts=4 sw=4 tw=0 noet :