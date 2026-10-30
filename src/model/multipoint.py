#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a collection of separate geographic positions."""

from __future__ import annotations
from typing import Any, override

from base import get_nested_list_depth
from model.obj import Obj
from model.point import POINTS, Point, create_point, pt_type


MULTIPOINTS: dict[str, MultiPoint] = dict()  # path_id: MultiPoint
_next_id = 0
mpt_type = list[pt_type]


class MultiPoint(Obj):
    """Parent of Point, consists of multiple Point objects."""

    def __init__(self, path_id: str, coordinates: mpt_type) -> None:
        super().__init__()
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        self.path_id = path_id
        self.set_children(coordinates)
        self.set_bbox()

    def set_children(self, coordinates: mpt_type) -> None:
        assert is_multipoint(coordinates), str(coordinates)[:100]
        for coords in coordinates:
            point = create_point(coords, self)
            self.children.append(point.id_)
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


def is_multipoint(coordinates: list[Any]) -> bool:
    return get_nested_list_depth(coordinates) == 2
