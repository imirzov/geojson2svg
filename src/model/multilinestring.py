#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a collection of multiple separate lines."""

from __future__ import annotations
from typing import Any, override

from base import get_nested_list_depth
from model.obj import Obj
from model.point import Point
from model.linestring import (
    LINESTRINGS,
    LineString,
    create_linestring,
    ls_type,
)


MULTILINESTRINGS: dict[str | int, MultiLineString] = dict()
_next_id = 0
ml_type = list[ls_type]


class MultiLineString(Obj):
    """Parent of LineString, consisting of multiple LineString objects."""

    def __init__(self, coordinates: ml_type) -> None:
        super().__init__()
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        self.set_children(coordinates)
        self.set_bbox()

    def set_children(self, coordinates: ml_type) -> None:
        assert is_multilinestring(coordinates), str(coordinates)[:100]
        for coords in coordinates:
            linestring = create_linestring(coords)
            self.children.append(linestring.id_)
        assert len(self.children), 'MultiLineString has no children!'

    @override
    def get_children(self) -> list[LineString]:
        return list([LINESTRINGS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for linestring in self.get_children():
            points.extend(linestring.get_points())
        return points


def create_multilinestring(
        coordinates: ml_type) -> MultiLineString:
    multilinestring = MultiLineString(coordinates)
    MULTILINESTRINGS[multilinestring.id_] = multilinestring
    return multilinestring


def is_multilinestring(coordinates: list[Any]) -> bool:
    return get_nested_list_depth(coordinates) == 3
