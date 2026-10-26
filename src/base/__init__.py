#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any


def get_nested_list_depth(list_: Any) -> int:
    """Returns the wrapping depth of a nested list.
    Takes into account only the first list element.
    """
    if not isinstance(list_, list):
        return 0
    else:
        if not list_:
            return 1
        return 1 + get_nested_list_depth(list_[0])
