#!/usr/bin/env python

import re
import os
import sys

RETURN = []
RESULT = 0

# load join status from file
file_path = os.path.join(sys.argv[1], 'info', 'join-status')
try:
	statusfile = open(file_path)
	statuscontent = statusfile.read()

	if re.compile(r"Joined successful").match(statuscontent) is None:
		RETURN.append(statuscontent)
		RESULT = 1
except IOError as ex:
	RETURN.append("ERROR: %s" % (ex))
	RESULT = 3
finally:
	try:
		statusfile.close()
	except NameError:
		RESULT = -1

if RETURN:
	for line in RETURN:
		print line
	sys.exit(RESULT)
