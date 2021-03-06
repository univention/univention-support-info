#!/usr/bin/python

import sys
import os
import re
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN = []

school_ver = ucr.get('appcenter/apps/ucsschool/version')
smb_role = ucr.get('samba/role')
smb4_role = ucr.get('samba4/role')

RETURN.append("UCS Version:  %s-%s Errata %s" % (ucr.get('version/version'), ucr.get('version/patchlevel'), ucr.get('version/erratalevel')))
if (school_ver != "") and (school_ver is not None):
	RETURN.append("UCS@school:   %s" % (school_ver))
RETURN.append("Server Rolle: %s" % (ucr.get('server/role')))

# if samba is running display samba role
if (smb_role != "") and (smb_role is not None):
	RETURN.append("Samba Rolle:  %s" % (smb_role))

# if samba4 is running display samba role
if (smb4_role != "") and (smb4_role is not None):
	RETURN.append("Samba4 Rolle: %s" % (smb4_role))

# if no maintenance display the message
fname = '%s/info/maintenance' % sys.argv[1]
if os.path.exists(fname):
	with open(fname, 'r') as fsock:
		maintenance = fsock.read().strip()
		if re.search(r'^maintenance ok', maintenance) is None:
			RETURN.append("Maintenance Info: \033[31;1m'%s'\033[0m" % (maintenance))
		else:
			RETURN.append("Maintenance Info: \033[32;1m%s\033[0m" % (maintenance.splitlines()[0]))

if RETURN:
	for line in RETURN:
		print line
else:
	print("Error while parsing ucr")

sys.exit(1)

# vim: set ts=4 sw=4 tw=0 noet :
