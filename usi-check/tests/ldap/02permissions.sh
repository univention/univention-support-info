#!/bin/bash


#  FIXME: I think this is broken. There are many setups where license check does not work (DC-Slaves, UCS@school, Memberservers ... ... )
## This is a problem with the Script itself (univention-lecense-check) sie also Bug#45476

if [ "$(grep "Permission denied" $1/info/univention-license-check)" ];
then
	result="Wrong LDAP permissions for machine account to test license [info/univention-license-check]!"
	exitcode=1
else
	result="LDAP permissions okay"
	exitcode=0
fi

echo $result
exit $exitcode
