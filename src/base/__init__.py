#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import Any
import unidecode


def get_nested_list_depth(list_: Any) -> int:
    """Returns the wrapping depth of a nested list.
    Takes into account only the first list element.
    """
    if not isinstance(list_, (list, tuple)):
        return 0
    else:
        if not list_:
            return 1
        return 1 + get_nested_list_depth(list_[0])


def to_en(s: str) -> str:
    """Utility for internationalization - i18n.
    Convert a string to EN. Removes special characters
    leaving only lowercase EN letters and hyphen.
    """
    s = unidecode.unidecode(s)
    s = s.lower()
    s = re.sub(r'\s', '-', s)
    return s
