#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a collection of separate geographic positions."""

from __future__ import annotations
from typing import override

from model.point import POINTS, pt_type, Point, create_point
from model.obj import Obj


# {id_: MultiPoint}
MULTIPOINTS: dict[str | int, MultiPoint] = dict()

_next_id = 0
mpt_type = list[pt_type]


class MultiPoint(Obj):
    COORDINATES_LIST_DEPTH = 2

    def __init__(self, path_id: str, coordinates: mpt_type) -> None:
        super().__init__(coordinates)
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        assert self.check_coords(), str(coordinates)[:100]
        self.path_id = path_id
        self.set_children(coordinates)
        self.set_bbox()

    def set_children(self, coordinates: mpt_type) -> None:
        for coords in coordinates:
            pt = create_point(coords, self)
            self.children.append(pt.id_)
        assert len(self.children), 'MultiPoint has no children!'

    @override
    def get_children(self) -> list[Point]:
        return list([POINTS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        return self.get_children()


def create_multipoint(path_id: str, coordinates: mpt_type) -> MultiPoint:
    multipoint = MultiPoint(path_id, coordinates)
    MULTIPOINTS[path_id] = multipoint
    return multipoint


def find_overlapping_multipoints(
        multipoints: list[MultiPoint]) \
            -> list[tuple[MultiPoint, MultiPoint]]:
    overlapping_pairs: list[tuple[MultiPoint, MultiPoint]] = []
    for i in range(len(multipoints) - 1):
        mp1 = multipoints[i]
        for j in range(i + 1, len(multipoints)):
            mp2 = multipoints[j]
            if mp1.is_overlapping_with(mp2):
                overlapping_pairs.append((mp1, mp2))
    return overlapping_pairs
