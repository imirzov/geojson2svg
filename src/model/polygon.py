#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a bounded area. The coordinates consist of an outer boundary
ring (and optional inner rings/holes), where the first and last coordinates
must be identical to close the shape.
"""

from __future__ import annotations
from typing import override, Any

from base import get_nested_list_depth
from model.obj import Obj
from model.point import POINTS, Point, create_point
from model.linestring import ls_type


POLYGONS: dict[str | int, Polygon] = dict()  # id_: Polygon
_next_id = 0
pg_type = list[ls_type]


class Polygon(Obj):
    """Parent of Point, consists of multiple Point objects."""

    def __init__(self, coordinates: pg_type) -> None:
        super().__init__()
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        self.set_children(coordinates)
        self.set_bbox()

    def set_children(self, coordinates: pg_type) -> None:
        assert is_polygon(coordinates), str(coordinates)[:100]
        for ring in coordinates:
            for x, y in ring:
                new_pt = create_point((x, y), self)
                self.children.append(new_pt.id_)

    @override
    def get_children(self) -> list[Point]:
        return list([POINTS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        return self.get_children()

    def remove_point(self, id_: int) -> None:
        assert id_ in POINTS, \
            f'Point {id_} not found in POINTS.'
        pt = POINTS[id_]
        assert pt.utmost is False, \
            f'Point {id_} is utmost and cannot be removed.'
        POINTS.pop(id_)
        assert id_ in self.children, \
            f'Polygon {self.id_} has no point {id_}'
        self.children.remove(id_)


def create_polygon(coordinates: pg_type = []) -> Polygon:
    polygon = Polygon(coordinates)
    POLYGONS[polygon.id_] = polygon
    return polygon


def find_overlapping_polygons(polygons: list[Polygon]) \
        -> list[tuple[Polygon, Polygon]]:
    overlapping_pairs: list[tuple[Polygon, Polygon]] = []
    for i in range(len(polygons) - 1):
        p1 = polygons[i]
        for j in range(i + 1, len(polygons)):
            p2 = polygons[j]
            if p1.is_overlapping_with(p2):
                overlapping_pairs.append((p1, p2))
    return overlapping_pairs


def is_polygon(coordinates: list[Any]) -> bool:
    return get_nested_list_depth(coordinates) == 3
