#!/bin/bash

ldap_lic=($( grep -i "univentionLicenseKeyID:" info/univention-license-object ))
ucr_lic=($( grep -i "uuid/license:" info/ucr-dump ))

status="checking license IDs: "
if [[ ${ldap_lic[1]} == ${ucr_lic[1]} ]]; then
	status="${status}\e[1;32mok\e[0m"
	exitcode=0
else
	status="${status}\e[1;31mLDAP and UCR differs!\e[0m"
	exitcode=1
fi

echo -e "$status"
exit $exitcode
