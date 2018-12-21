#!/bin/bash

if [ "$(grep "Found 0" $1/info/check-templates)" ]
then
	status="OK"
	exitcode=0
else
	status="Modified Templates Found."
	cat $1/info/check-templates
	exitcode=1
fi

result="$status"

echo $result
exit $exitcode
