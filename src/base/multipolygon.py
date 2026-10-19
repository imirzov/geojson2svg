#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a collection of multiple separate polygons
(e.g., an archipelago of islands)."""

from __future__ import annotations
from typing import override

from base.obj import Obj
from base.polygon import POLYGONS, Polygon, create_polygon
from base.point import Point


MULTIPOLYGONS: dict[str | int, MultiPolygon] = dict()  # id_: MultiPolygon


class MultiPolygon(Obj):
    """Parent of Polygon, consists of multiple Polygon objects."""

    def __init__(self, path_id: str,
                 coordinates: list[list[list[tuple[float, float]]]]) -> None:
        super().__init__()
        self.path_id = path_id
        self.set_children(coordinates)
        self.set_bbox()

    def set_children(self, coordinates:
                     list[list[list[tuple[float, float]]]]) -> None:
        for mp in coordinates:
            for coords in mp:
                # # Filter triangles/cross-intersections
                # sgp = shapely.geometry.Polygon(coords)
                # sgp = cleanup_shapely_polygon(sgp)
                # coords = list(sgp.exterior.coords)
                pg = create_polygon(coords)
                self.children.append(pg.id_)
        assert len(self.children), 'MultiPolygon has no children!'

    @override
    def get_children(self) -> list[Polygon]:
        return list([POLYGONS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for pg in self.get_children():
            points.extend(pg.get_points())
        return points


def create_multipolygon(
        path_id: str,
        coordinates: list[list[list[tuple[float, float]]]]) -> MultiPolygon:
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
