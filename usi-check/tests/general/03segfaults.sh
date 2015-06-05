#!/bin/bash

nofile_logs="$(grep -s -l -i "segfault" ${1}/files/var_log_syslog_* |  sed "s#${1}/files/##" | sort -V)"

if [ -n "$nofile_logs" ]; then
	result="\"Segfault\" messages in:"
	c=0
	for fname in $nofile_logs; do
		result="${result}\n    $fname"
		let c=c+1
		if [ $c -ge 5 ]; then
			let left=$(echo $nofile_logs | tr ' ' '\n' |wc -l)-c
			result="${result}\n    ... and $left more"
			break
		fi
	done
	exitcode=1
else
	result="OK"
	exitcode=0
fi

echo -e $result
exit $exitcode
