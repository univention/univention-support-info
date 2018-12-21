#!/bin/bash

version=($( grep -i "version/version" info/ucr-dump | cut -d " " -f 2))
major=($( echo $version | cut -d "." -f 1))
minor=($( echo $version | cut -d "." -f 2))
# echo "$major.$minor"

status="${status}\e[1;32mok\e[0m"
exitcode=0

if [[ $major -ge 4 ]]; then
	if [[ $minor -ge 3 ]]; then
		# Version greater or equal 4.3 - do check
		grep -E -q "open-xchange-meta|open-xchange-gui" info/dpkg-l
		err=$?
		if [[ $err == 0  ]]; then
			status="${status}\e[1;31mOX Metapackages installed! Check bug #47394.\e[0m"
			exitcode=1
		fi
	fi
		
fi


echo -e "$status"
exit $exitcode
