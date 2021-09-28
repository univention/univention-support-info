Univention Support Info
=======================

The tool [univention-support-info](univention-support-info) is used to collect
information from the customer system for Univention Support. The collected data
is stored in a compressed TAR file, which can optionally be encrypted before
the file is sent via email to <mailto:support@univention.de> or uploaded to
<https://upload.univention.de/> for Univention support.

More details are available from the Support database in
- [English](https://help.univention.com/t/29)
- [German](https://help.univention.com/t/6729)

Installation
------------
The script is available from different locations in different versions:
1. In this repository as [univention-support-info](univention-support-info)
2. From the [public download server](https://updates.software-univention.de/download/scripts/univention-support-info)
3. From the UCS package `univention-install univention-support-info`

Usage
-----
```
sudo ./univention-support-info
```

Included information
--------------------
The following collection is not complete; for details look at the code.

- Certificate validity `/etc/univention/ssl/`
- Configuration files from `/etc/`
- Log files from `/var/log/`
- System information from `/proc/`
- Licence information
- UCS version information
- APT package state
- UCR template files
- Listener / Notifier transaction files
- Process state
- Network configuration
- Hardware information
- `at` jobs
