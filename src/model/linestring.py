#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a line formed by an ordered sequence of Points."""

from __future__ import annotations
from typing import override

from model.point import POINTS, pt_type, Point, create_point
from model.obj import Obj


# {id_: LineString}
LINESTRINGS: dict[str | int, LineString] = dict()

_next_id = 0
ls_type = list[pt_type]


class LineString(Obj):
    COORDINATES_LIST_DEPTH = 2

    def __init__(self, coordinates: ls_type) -> None:
        super().__init__(coordinates)
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        assert self.check_coords(), str(coordinates)[:100]
        for xy in coordinates:
            pt = create_point(xy, self)
            self.children.append(pt.id_)
        self.set_bbox()

    @override
    def get_children(self) -> list[Point]:
        return list([POINTS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        return self.get_children()

    @override
    def get_svg_code(self) -> str:
        coords = ' '.join(f'{pt.x},{pt.y}' for pt in self.get_children())
        return f'<polyline points="{coords}" />\n'

    @override
    def get_svg_style(self) -> str:
        return 'polyline {fill:none; stroke:white; stroke-width:0.2px;}\n'


def create_linestring(coordinates: ls_type) -> LineString:
    ls = LineString(coordinates)
    LINESTRINGS[ls.id_] = ls
    return ls
