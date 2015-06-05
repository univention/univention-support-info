#!/usr/bin/python

import sys
import os
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN=[]

if ucr.get('samba4/autostart', 'no').lower() in ('yes', 'true', '1'):
	if ucr.get('kerberos/autostart', 'no').lower() in ('yes', 'true', '1'):
		RETURN.append('CRITICAL: both "kerberos/autostart" and "samba4/autostart" active')
	with open( os.path.join( sys.argv[1], 'info', 'ps'), 'r') as infile:
		h_lines = list()
		for line in infile:
			if 'heimdal' in line:
				h_lines.append(line.strip())
	if h_lines:
		RETURN.append('CRITICAL: heimdal running on samba4 system:')
		RETURN.extend(h_lines)




if RETURN:
	for line in RETURN:
		print line
	sys.exit(1)


# vim: set ts=4 sw=4 tw=0 noet :
