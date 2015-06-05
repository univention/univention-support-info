#!/bin/bash

exitcode=0
output=""

# FIXME: This won't work under all circumstances, for example if there was no server password change in the first logfile but the 10th or 11th...
# alphabetical sort by grep! So var_log_univention_server_password_change.log_10 could be the first line ...
# Easiest "fix" seems to be to only have a look at 0-9
lastpwchange=$(grep -h "^done (" $1/files/var_log_univention_server_password_change.log?[0-9] 2>/dev/null | head -n1 | sed 's/done (\(.*\))/\1/')

if [ -n "$lastpwchange" ]
then
	output="Last server password change was at: ${lastpwchange}"
	exitcode=1
fi

echo $output
exit $exitcode
