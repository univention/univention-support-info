#!/bin/bash

nID=$( cat $1/info/notifierID )
lID=$( cat $1/info/listenerID )
lBC=$( [ -f $1/files/var_lib_univention-directory-listener_bad_cache ]; echo $? )
result=""
exitcode=0

function quit() {
	echo -e $result
	exit $exitcode
}



if [ -z $nID ]; then
	result="${result}No notifier ID in info/notifierID\n"
	# Well, what does it mean? Not running?
	exitcode=1
fi
if [ -z $lID ]; then
	result="${result}No listener ID in info/listenerID\n"
	# Well, what does it mean? Not running?
	exitcode=1
fi
if [ $lBC -eq 0 ]; then
	result="${result}Listener Cache seems brocken [/var/lib/univention-directory-listener/bad_cache is present!]\n"
	exitcode=3
fi
if [ $exitcode -eq 1 ]; then #skip ID check when one or both IDs not found
	quit
fi


if [ $nID -ne $lID ]; then
	result="${result}Listener (${lID}) and Notified ID (${nID}) not equal!"
	exitcode=1
else
	result="${result}Listener and Notified ID okay"
#	exitcode=0 #initially set to 0; exitcode is 3 when bad_cache is detected
fi

quit
