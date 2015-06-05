#!/bin/bash

nofile_logs="$(grep -s -l -i "too many open" ${1}/files/var_log_* |  sed "s#${1}/files/##")"

if [ -n "$nofile_logs" ]; then
	result="\"Too many open files\" messages in:"
	for fname in $nofile_logs; do
		result="${result}\n    $fname"
	done
	exitcode=1
else
	result="OK"
	exitcode=0
fi

echo -e $result
exit $exitcode
