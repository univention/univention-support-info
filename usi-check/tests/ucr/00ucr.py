#!/usr/bin/python

import sys
from ucr import UCR

# load ucr variables
ucr = UCR(sys.argv[1])
RETURN=[]

def nameserver():
	if ucr.get('server/role').startswith('domaincontroller'):
		interfaces = ucr.getall('interfaces/.*/address$')
		IPs = [interfaces[x] for x in interfaces]

		if ucr.get('nameserver1') not in IPs:
			RETURN.append( 'nameserver1 (%s) does not point to a local ip' % ucr.get('nameserver1') )
nameserver()

def samba_bindonly():
	if ucr.get('samba/interfaces/bindonly', '0').lower() in ('true', 'yes', '1'):
		samba_interfaces = ucr.get('samba/interfaces').lower()
		for i in ('127.0.0.1', 'lo', '0.0.0.0'):
			if i in samba_interfaces:
				return
		if ucr.get('kerberos/kdc') == '127.0.0.1':
			RETURN.append('samba/interfaces does not contain loopback but kerberos/kdc is set to 127.0.0.1')
		if ucr.get('kerberos/kpasswdserver') == '127.0.0.1':
			RETURN.append('samba/interfaces does not contain loopback but kerberos/kpasswdserver is set to 127.0.0.1')
samba_bindonly()

if RETURN:
	for line in RETURN:
		print line
	sys.exit(1)


# vim: set ts=4 sw=4 tw=0 noet :
