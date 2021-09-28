#!/usr/bin/env python
from __future__ import absolute_import

from datetime import datetime
from os import environ

import setuptools

try:
    ts = environ["CI_COMMIT_TIMESTAMP"]
    dt = datetime.fromisoformat(ts)
except LookupError:
    dt = datetime.now()
VERSION = "0.{0:%Y%m%d}.{0:%H%M%S}".format(dt)

setuptools.setup(version=VERSION)
