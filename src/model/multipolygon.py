#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a collection of multiple separate polygons."""

from __future__ import annotations
from typing import override

from model.obj import Obj
from model.point import Point
from model.polygon import POLYGONS, pg_type, Polygon, create_polygon


# {id_: MultiPolygon}
MULTIPOLYGONS: dict[str | int, MultiPolygon] = dict()

_next_id = 0
mpg_type = list[pg_type]


class MultiPolygon(Obj):
    """Parent of Polygon, consists of multiple Polygon objects."""

    def __init__(self, path_id: str, coordinates: mpg_type) -> None:
        super().__init__(coordinates)
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        assert self.check_coords(), str(coordinates)[:100]
        self.path_id = path_id
        self.set_children(coordinates)
        self.set_bbox()

    def set_children(self, coordinates: mpg_type) -> None:
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


def create_multipolygon(path_id: str, coordinates: mpg_type) -> MultiPolygon:
    mpg = MultiPolygon(path_id, coordinates)
    MULTIPOLYGONS[path_id] = mpg
    return mpg


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
