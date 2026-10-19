#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a single geographic position (longitude, latitude)."""

from __future__ import annotations

import sys
from typing import Self, Any, override

from base.bbox import BBox
from base.obj import Obj


POINTS: dict[str | int, Point] = dict()  # id_: (x, y)


class Point(Obj):

    def __init__(self, coordinates: tuple[float, float],
                 parent: Any | None = None) -> None:
        super().__init__()
        self.id_ = len(POINTS)
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

    def round(self, precision: int) -> None:
        self.x = round(self.x // precision * precision)
        self.y = round(self.y // precision * precision)
        self.bbox = BBox(self.x, self.x, self.y, self.y)

    def close_to(self, pt: Self, precision: int) -> bool:
        if abs(self.x - pt.x) > precision:
            return False
        if abs(self.y - pt.y) > precision:
            return False
        return True

    def __str__(self) -> str:
        return 'Point {} x={} y={} tied_to={} utmost={}' \
            .format(self.id_, self.x, self.y, self.tied_to, self.utmost)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def create_point(coordinates: tuple[float, float],
                 parent: Any | None = None) -> Point:
    pt = Point(coordinates, parent)
    POINTS[pt.id_] = pt
    return pt


def merge_points_to(points: list[Point], point: Point) -> None:
    for pt in points:
        pt.x = point.x
        pt.y = point.y
