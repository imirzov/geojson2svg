#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any


def get_wrapping_depth(list_: list[Any]) -> int:
    """Returns the wrapping depth of a nested list."""
    if len(list_) == 1:
        return 1 + get_wrapping_depth(list_[0])
    else:
        return 0

    # assert len(list_), 'empty list'
    # if all(isinstance(value, (int, float)) for value in list_):
    #     return 0
    # assert len(list_) == 1, f'list contains {len(list_)} elements'
