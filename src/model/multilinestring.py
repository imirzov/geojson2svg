#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a collection of multiple separate lines - LineStrings."""

from __future__ import annotations
from typing import override

from model.linestring \
    import LINESTRINGS, ls_type, LineString, create_linestring
from model.obj import Obj
from model.point import Point


# {id_: MultiLineString}
MULTILINESTRINGS: dict[str | int, MultiLineString] = dict()

_next_id = 0
ml_type = list[ls_type]


class MultiLineString(Obj):
    """Parent of LineString, consisting of multiple LineString objects."""

    def __init__(self, coordinates: ml_type) -> None:
        super().__init__(coordinates)
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        assert self.check_coords(), str(coordinates)[:100]
        for coords in coordinates:
            ls = create_linestring(coords)
            self.children.append(ls.id_)
        self.set_bbox()

    @override
    def get_children(self) -> list[LineString]:
        return list([LINESTRINGS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for ls in self.get_children():
            points.extend(ls.get_points())
        return points


def create_multilinestring(coordinates: ml_type) -> MultiLineString:
    mls = MultiLineString(coordinates)
    MULTILINESTRINGS[mls.id_] = mls
    return mls
