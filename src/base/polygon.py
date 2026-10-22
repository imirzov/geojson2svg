#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a bounded area. The coordinates consist of an outer boundary
ring (and optional inner rings/holes), where the first and last coordinates
must be identical to close the shape.
"""

from __future__ import annotations

from typing import Any, override

from base import get_wrapping_depth
from base.bbox import BBox
from base.obj import Obj
from base.point import POINTS, Point, create_point
from settings import report as r


POLYGONS: dict[str | int, Polygon] = dict()  # id_: Polygon


class Polygon(Obj):
    """Parent of Point, consists of multiple Point objects."""

    def __init__(self, coordinates: list[tuple[float, float]]) -> None:
        super().__init__()
        self.id_ = len(POLYGONS)
        self.set_children(coordinates)
        self.set_bbox()
        self.converted = False

    def set_children(self, coordinates: list[tuple[float, float]]) -> None:
        assert is_polygon(coordinates)
        for x, y in coordinates:
            new_pt = create_point((x, y), self)
            self.children.append(new_pt.id_)

    @override
    def get_children(self) -> list[Point]:
        return list([POINTS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        return self.get_children()

    def remove_point(self, id_: int) -> None:
        a = id_ in POINTS
        b = id_ in self.children
        if not a:
            r.warning(f'Point {id_} not found in POINTS.')
        if not b:
            r.warning(f'Polygon {self.id_} has no point {id_}')
        if a:
            pt = POINTS[id_]
            if pt.utmost:
                r.warning(f'Point {id_} is utmost and cannot be removed.')
            else:
                POINTS.pop(id_)
                if b:
                    self.children.remove(id_)

    def convert_coords_to_px(self, map_bbox: BBox,
                             w: float, h: float) -> None:
        if not self.converted and map_bbox.xmax != map_bbox.xmin \
                and map_bbox.ymax != map_bbox.ymin:
            for p in self.get_children():
                p.x = (p.x - map_bbox.xmin) / map_bbox.dx * w
                p.y = (map_bbox.ymax - p.y) / map_bbox.dy * h
        self.converted = True


def create_polygon(coordinates: list[tuple[float, float]] = []) -> Polygon:
    pg = Polygon(coordinates)
    POLYGONS[pg.id_] = pg
    return pg


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
    # if type(coordinates) is not list:
    #     r.warning('Coordinates must be a list.')
    #     return False
    # for coords in coordinates:
    #     if len(coords) != 2:
    #         len_ = len(coords)
    #         r.warning('Each coordinate must have '
    #                   f'exactly 2 elements, not {len_}.')
    #         return False
    #     for c in coords:
    #         if type(c) not in [int, float]:
    #             r.warning('Each coordinate must be an int or float.')
    #             return False
    # return True
    return get_wrapping_depth(coordinates) == 2
