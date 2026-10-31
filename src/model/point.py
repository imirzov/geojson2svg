#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a single geographic position (longitude, latitude)."""

from __future__ import annotations
import sys
from typing import Self, Any, override

from base.bbox import BBox
from model.obj import Obj


# {id_: Point}
POINTS: dict[str | int, Point] = dict()

_next_id = 0
pt_type = tuple[float, float]


class Point(Obj):
    COORDINATES_LIST_DEPTH = 1

    def __init__(self, coordinates: pt_type, parent: Any = None) -> None:
        super().__init__(coordinates)
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        assert self.check_coords(), str(coordinates)[:100]
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.parent = parent
        self.bbox = BBox(self.x, self.x, self.y, self.y)
        self.merged = False
        self.tied_to = sys.maxsize
        self.utmost = False

    @override
    def get_children(self) -> list[Any]:
        return []

    @override
    def get_points(self) -> list[Any]:
        return []

    @override
    def get_svg_code(self) -> str:
        return f'<circle cx="{self.x}" cy="{self.y}" r="0.5" />\n'

    @override
    def get_svg_style(self) -> str:
        return 'circle {fill:black; stroke:white; stroke-width:0.2px;}\n'

    def round(self, precision: int) -> None:
        self.x = round(self.x // precision * precision)
        self.y = round(self.y // precision * precision)
        self.bbox = BBox(self.x, self.x, self.y, self.y)

    def close_to(self, pt: Self, precision: int) -> bool:
        dx = abs(self.x - pt.x)
        dy = abs(self.y - pt.y)
        if dx <= precision and dy <= precision:
            return True
        return False

    def __str__(self) -> str:
        return 'Point {} x={} y={} tied_to={} utmost={}' \
            .format(self.id_, self.x, self.y, self.tied_to, self.utmost)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def create_point(coordinates: pt_type, parent: Any = None) -> Point:
    pt = Point(coordinates, parent)
    POINTS[pt.id_] = pt
    return pt


def merge_points_to(points: list[Point], p: Point) -> None:
    for point in points:
        point.x = p.x
        point.y = p.y
