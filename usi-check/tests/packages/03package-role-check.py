#!/usr/bin/python

import os
import sys
import re
from ucr import UCR


# 1. Use descriptive names. What is "srvrlmtch" going to tell anybody?
# 2. If you cannot find a descriptive name it indicated that it's hard to tell what the given object is, i.e. it indicates that one should re-think if the conglomerate of information stored in the object makes sense.
# 3. Object to store Server-Role Information is not needed because role is constant in usecase
# 4. Keep it simple: Objects are for a) encapsulation b) combining methods with scoped data. The SRM class doesn't fit these criteria: you access srm.packages.update() so you don't need srm.count()
# 5. Don't introduce new data for no reason, e.g. pkgrole instead of simply using pkgname
# 6. Don't do work twice: you apply a regexp, so let it extract the relevant parts from the line
# 7. Make a line to one thing, avoid nested constucts like: function_call(data.subobject[index])

# -----

def package_is_ok_on_server_role(pkgname, server_role):
	package_allowed = False
	if pkgname == "univention-server-master": # univention-server-master
		if server_role == "domaincontroller_master":
			package_allowed = True
	elif pkgname == "univention-server-backup": # univention-server-backup
		if server_role == "domaincontroller_backup":
			package_allowed = True
	elif pkgname == "univention-server-slave": # univention-server-slave
		if server_role == "domaincontroller_slave":
			package_allowed = True
	elif pkgname == "univention-server-member": # univention-server-member
		if server_role == "memberserver":
			package_allowed = True
	return package_allowed


def check_server_pkgs(matches, server_role):

	installed_metapackages = []
	for match in matches:
		(pkgstat, pkgname) = match
		if pkgstat.startswith('install'): # heed only installed packages
			package_allowed = package_is_ok_on_server_role(pkgname, server_role)
			installed_metapackages.append({pkgname: package_allowed})

	return installed_metapackages


# load ucr variables
usi_path = sys.argv[1]
ucr = UCR(usi_path)

# load package stati from file
dpkglist_path = os.path.join(usi_path, 'info', 'dpkg-l')
try:
	infofile = open(dpkglist_path)
	dpkglist = infofile.read()
finally:
	infofile.close()

# only check relevant packages if they (it) matches server/role
server_role = ucr.get('server/role')
role_packages_in_dpkglist = re.compile(r"(.*)\t(univention-server-.*|univention-basesystem)\t.*")
metapackage_check_result = check_server_pkgs(role_packages_in_dpkglist.findall(dpkglist), server_role)

# print check result
if len(metapackage_check_result) > 1:
	print("ERROR: more than 1 server package found! %s" % (metapackage_check_result,) )
	sys.exit(3)

elif not metapackage_check_result[0].values()[0]:
	print("Warning: server/role (%s) does NOT match installed Package" % (server_role,) )
	sys.exit(1)

else:
	print("Info: server/role (%s) does match installed Package" % (server_role,) )
	sys.exit(0)
