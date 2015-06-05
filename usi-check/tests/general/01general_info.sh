#!/bin/bash

#TODO Pythonisieren -> UCR-Lib benutzen

version="UCS Version: $(grep "version/version" $1/info/ucr-dump | cut -d" " -f2)-$(grep "version/patchlevel" $1/info/ucr-dump | cut -d" " -f2)-Errata$(grep "version/erratalevel" $1/info/ucr-dump | cut -d" " -f2)"
role="Rolle: $(grep "server/role" $1/info/ucr-dump | cut -d" " -f2)"

result="$version\n$role"

if ! [ -n "$result" ]
then
	result="Error while parsing ucr"
	exitcode=1
else
	exitcode=1
fi

echo -e $result
exit $exitcode
