#!/usr/bin/env python
from __future__ import absolute_import

import ast
from datetime import datetime
from os import environ

import setuptools

BIN = "univention-support-info"


def ver():
    with open("univention-support-info") as fd:
        code = fd.read()

    top_level = ast.parse(code, BIN)
    (ver,) = [
        ast.literal_eval(stmt.value)
        for stmt in top_level.body
        if isinstance(stmt, ast.Assign)
        for trgt in stmt.targets
        if isinstance(trgt, ast.Name) and trgt.id == "usiVersion"
    ]

    return ver


try:
    ts = environ["CI_COMMIT_TIMESTAMP"]
    dt = datetime.fromisoformat(ts)
except LookupError:
    dt = datetime.now()
VERSION = "{ver}.{dt:%Y%m%d}.{dt:%H%M%S}".format(ver=ver(), dt=dt)

setuptools.setup(version=VERSION)
