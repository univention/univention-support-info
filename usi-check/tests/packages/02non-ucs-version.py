#!/usr/bin/python

import os, sys, re
from ucr import UCR
# load ucr variables
ucr = UCR(sys.argv[1])

ucsstamp = re.compile(r'.*\.\d{12}$')
ucs_version = ucr.get('version/version')
# Some packages do not have a univention buildstamp
whitelist = [
			'firefox',
			re.compile(r'firmware-\w'),
			re.compile(r'open-xchange\w*'),
			'gcc-4.2-base',
			'whois'
			]

def in_whitelist(pkgname):
	for item in whitelist:
		if isinstance(item, re._pattern_type):
			if item.match(pkgname):
				return True
		elif isinstance(item, str):
			if item == pkgname:
				return True
	return False

odd_packages = []
if (ucs_version != '4.2'):
	with open( os.path.join( sys.argv[1], 'info', 'dpkg-l'), 'r') as infile:
		for line in infile:
			if not line.startswith('install'):
				continue
			if not ucsstamp.match(line):
				# no ucs buildstamp
				line = line.strip()
				status, pkgname, pkgversion = line.split('\t')
				if not in_whitelist(pkgname):
					odd_packages.append( (status, pkgname, pkgversion) )


if odd_packages:
	print 'Some packages do not contain univention buildstamps:'
	for p in odd_packages:
		print '  ' + ' '.join(p)
	sys.exit(1)

sys.exit(0)
