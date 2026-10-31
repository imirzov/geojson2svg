#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a line formed by an ordered sequence of positions."""

from __future__ import annotations
from typing import Any, override

from base import get_nested_list_depth
from model.obj import Obj
from model.point import POINTS, Point, pt_type, create_point


LINESTRINGS: dict[str | int, LineString] = dict()  # id_: LineString
_next_id = 0
ls_type = list[pt_type]


class LineString(Obj):
    """Parent of Point, consisting of multiple Point objects."""

    def __init__(self, coordinates: ls_type) -> None:
        super().__init__()
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        self.set_children(coordinates)
        self.set_bbox()

    def set_children(self, coordinates: ls_type) -> None:
        assert is_linestring(coordinates), str(coordinates)[:100]
        for x, y in coordinates:
            new_pt = create_point((x, y), self)
            self.children.append(new_pt.id_)

    @override
    def get_children(self) -> list[Point]:
        return list([POINTS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        return self.get_children()


def create_linestring(coordinates: ls_type) -> LineString:
    linestring = LineString(coordinates)
    LINESTRINGS[linestring.id_] = linestring
    return linestring


def is_linestring(coordinates: list[Any]) -> bool:
    return get_nested_list_depth(coordinates) == 2
