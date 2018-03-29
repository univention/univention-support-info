#!/usr/bin/python

import os, sys

if os.stat("%s/info/dpkg--audit" % sys.argv[1]).st_size == 0:
	print "Everything okay"
	sys.exit(0)
	
else:
	print "Corrupt Package Status. Check dpkg--audit"
	sys.exit(1)
