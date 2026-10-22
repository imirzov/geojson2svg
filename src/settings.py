#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""© Ihor Mirzov, 2021.
Global application's settings.
"""

import datetime
import logging
from pathlib import Path
import re
import unidecode

src = Path(__file__).parent.resolve()
files = Path(src.parent / 'files').resolve()
logs = Path(src.parent / 'logs').resolve()
tests = Path(src / 'tests').resolve()


for d in [logs, files]:
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)

report = logging.getLogger('report')
log_level = logging.INFO
encoding = 'utf-8'
geo = 'geo.json'


def to_en(s: str) -> str:
    """Utility for internationalization - i18n.
    Convert a string to EN. Removes special characters
    leaving only lowercase EN letters and hyphen.
    """
    s = unidecode.unidecode(s)
    s = s.lower()
    s = re.sub(r'\s', '-', s)
    return s


def time_now() -> str:
    """Last update time for HTML pages.
    2023-12-17 17:34:42
    """
    return str(datetime.datetime.now())[:19]
