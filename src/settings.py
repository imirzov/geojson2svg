#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""© Ihor Mirzov, 2021.
Global application's settings.
"""

import logging
from pathlib import Path

src = Path(__file__).parent.resolve()
files = Path(src.parent / 'files').resolve()
logs = Path(src.parent / 'logs').resolve()
tests = Path(src / 'tests').resolve()


for d in [logs, files]:
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)

log_level = logging.DEBUG
encoding = 'utf-8'
geo = 'geo.json'
