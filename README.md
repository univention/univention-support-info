Univention Support Info
=======================

The tool [univention-support-info](univention-support-info) is used to collect
information from the customer system for Univention Support. The collected data
is then uploaded as an encrypted archive to the Univention web site, from where
is can be accessed and decrypted by Univention Support only.

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
