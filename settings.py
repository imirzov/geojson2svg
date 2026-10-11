#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""© Ihor Mirzov, 2021.
Global application's settings.
"""

import logging
from pathlib import Path
import re
import unidecode

SRC_DIR = Path(__file__).parent

files = Path(SRC_DIR / '..' / 'files').resolve()
logs = Path(SRC_DIR / '..' / 'logs').resolve()

report = logging.getLogger('report')

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
