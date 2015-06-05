#!/bin/bash

grep -q "Joined successful" $1/info/join-status
if [ $? -eq 0 ]
then
	result="OK"
	exitcode=0
else
	result="$(cat $1/info/join-status)"
	exitcode=1
fi

echo -e $result
exit $exitcode
