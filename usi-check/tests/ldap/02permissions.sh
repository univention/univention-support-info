#!/bin/bash


#FIXME: I think this is broken. There are many setups where license check does not work (DC-Slaves, UCS@school, Memberservers ... ... )
if [ "$(grep "Permission denied" $1/info/univention-license-check)" ];
then
	result="Wrong LDAP permissions for machine account!"
	exitcode=1
else
	result="LDAP permissions okay"
	exitcode=0
fi

echo $result
exit $exitcode
