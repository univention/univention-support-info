#!/usr/bin/python

import sys
import os
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN=[]

if ucr.get('kerberos/realm').lower() != ucr.get('domainname').lower():
		RETURN.append('CRITICAL: Kerberos realm and DNS domainname does not match')

if RETURN:
	for line in RETURN:
		print line
	sys.exit(1)


# vim: set ts=4 sw=4 tw=0 noet :
