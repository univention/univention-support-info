#!/bin/bash

nID=$(cat $1/info/notifierID)
lID=$(cat $1/info/listenerID)
result=""
exitcode=0

function quit() {
	echo -e $result
	exit $exitcode
}





if [ -z $nID ]; then
	result="${result}No notifier ID}\n"
	exitcode=1
fi
if [ -z $lID ]; then
	result="${result}No listener ID\n"
	exitcode=1
fi
if [ $exitcode -ne 0 ]; then
	quit
fi


if [ $nID -ne $lID ]; then
	result="Listener (${lID}) and Notified ID (${nID}) not equal!"
	exitcode=1
else
	result="Listener and Notified ID okay"
	exitcode=0
fi

quit
