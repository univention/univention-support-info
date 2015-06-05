#!/usr/bin/python

import sys
import os
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN=[]

if ucr.get('connector/s4/autostart', 'yes').lower() in ('yes', 'true', '1'):
	with open( os.path.join( sys.argv[1], 'info', 'ps'), 'r') as infile:
		h_lines = list()
		for line in infile:
			if 's4connector' in line:
				h_lines.append(line.strip())
	if len(h_lines) > 1:
		RETURN.append('CRITICAL: multiple instances of s4-connector are running:')
		RETURN.extend(h_lines)

if RETURN:
	for line in RETURN:
		print line
	sys.exit(1)


# vim: set ts=4 sw=4 tw=0 noet :
