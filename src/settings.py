#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""© Ihor Mirzov, 2021.
Global application's settings.
"""

import logging
from pathlib import Path

root = Path(__file__).parent.parent.resolve()
src = root / 'src'
files = root / 'files'
logs = root / 'logs'
tests = root / 'tests'
src_tests = src / 'tests'


for d in [logs, files]:
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)

log_level = logging.DEBUG
encoding = 'utf-8'
geo = 'geo.json'
