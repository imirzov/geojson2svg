#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a collection of multiple separate polygons."""

from __future__ import annotations
from typing import Any, override

from base import get_nested_list_depth
from dom.obj import Obj
from dom.point import Point
from dom.polygon import POLYGONS, pg_type, Polygon, create_polygon


MULTIPOLYGONS: dict[str | int, MultiPolygon] = dict()  # id_: MultiPolygon
_next_id = 0
mp_type = list[pg_type]


class MultiPolygon(Obj):
    """Parent of Polygon, consists of multiple Polygon objects."""

    def __init__(self, path_id: str, coordinates: mp_type) -> None:
        super().__init__()
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        self.path_id = path_id
        self.set_children(coordinates)
        self.set_bbox()

    def set_children(self, coordinates: mp_type) -> None:
        assert is_multipolygon(coordinates), str(coordinates)[:100]
        for coords in coordinates:
            # Filter triangles/cross-intersections
            # sgp = shapely.geometry.Polygon(coords)
            # sgp = cleanup_shapely_polygon(sgp)
            # coords = list(sgp.exterior.coords)
            polygon = create_polygon(coords)
            self.children.append(polygon.id_)
        assert len(self.children), 'MultiPolygon has no children!'

    @override
    def get_children(self) -> list[Polygon]:
        return list([POLYGONS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for polygon in self.get_children():
            points.extend(polygon.get_points())
        return points


def create_multipolygon(path_id: str, coordinates: mp_type) -> MultiPolygon:
    mp = MultiPolygon(path_id, coordinates)
    MULTIPOLYGONS[path_id] = mp
    return mp


def find_overlapping_multipolygons(
        multipolygons: list[MultiPolygon]) \
            -> list[tuple[MultiPolygon, MultiPolygon]]:
    overlapping_pairs: list[tuple[MultiPolygon, MultiPolygon]] = []
    for i in range(len(multipolygons) - 1):
        mp1 = multipolygons[i]
        for j in range(i + 1, len(multipolygons)):
            mp2 = multipolygons[j]
            if mp1.is_overlapping_with(mp2):
                overlapping_pairs.append((mp1, mp2))
    return overlapping_pairs


def is_multipolygon(coordinates: list[Any]) -> bool:
    return get_nested_list_depth(coordinates) == 4
