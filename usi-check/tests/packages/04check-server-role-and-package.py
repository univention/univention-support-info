#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
from ucr import UCR

# load ucr variables
usi_path = sys.argv[1]
ucr = UCR(usi_path)

ucsstamp = re.compile(r'.*\t(univention-server-.*|univention-basesystem)\t.*')


# check serverrole and installed server-package

server_role = ucr.get('server/role')
role_packages = []
with open( os.path.join( sys.argv[1], 'info', 'dpkg-l'), 'r') as infile:
	for line in infile:
		if line.startswith('deinstall') and ucsstamp.match(line):
				line = line.strip()
				status, pkgname, pkgversion = line.split('\t')
				role_packages.append( (status, pkgname, pkgversion) )

if role_packages:
	print ("ERROR: Server-Packages für Serverrolle: {0} nicht mehr installiert".format(server_role))
	sys.exit(1)

sys.exit(0)

# vim: set ts=4 sw=4 tw=0 noet :
