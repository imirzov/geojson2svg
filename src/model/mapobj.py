#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import os
from typing import Self, override

from base import to_en
from base.lands import Land
from model.feature import get_features
from model.obj import Obj
from model.point import POINTS, Point
from model.multipolygon import MULTIPOLYGONS, MultiPolygon, create_multipolygon

PARENTS: dict[int, str] = dict()  # id_: name


class MapObj(Obj):
    """Parent of MultiPolygon, consists of multiple MultiPolygon objects."""

    def __init__(self, klass: type[Land]) -> None:
        super().__init__()
        os.chdir(os.path.dirname(__file__))
        self.klass = klass
        self.svg_fpath = klass.fpath.with_suffix('.svg')
        self.read_children()
        self.set_bbox()

    def __str__(self) -> str:
        return f'{self.klass.fpath.name}\n' \
            + f'{self.klass.w}x{self.klass.h}\n' \
            + f'{self.bbox}\n' \
            + f'{len(self.children)} paths\n' \
            + f'{len(POINTS)} points before\n'

    def read_children(self) -> None:
        """Read polygon coordinates:
        {
            id1: [(x11, y11), (x12, y12), ...],
            id2: [(x21, y21), (x22, y22), ...],
            ...
        }
        """
        assert self.klass.fpath.exists(), \
            f'File not found: {self.klass.fpath}'

        for feature in get_features(self.klass.fpath):
            p = feature.properties
            g = feature.geometry
            path_id = p[self.klass.name]
            if self.klass.parent is not None:
                if self.klass.parent in p and self.klass.id in p:
                    if p[self.klass.parent] in PARENTS:
                        path_id = PARENTS[p[self.klass.parent]] \
                            + '_' + path_id
                    PARENTS[p[self.klass.id]] = path_id
            else:
                if self.klass.id in p:
                    PARENTS[p[self.klass.id]] = p[self.klass.name]
            path_id = to_en(path_id)

            if g.type == 'MultiPolygon':
                coordinates = g.coordinates
            else:
                coordinates = [g.coordinates]
            mpg = create_multipolygon(path_id, coordinates)
            self.children.append(mpg.path_id)

    @override
    def get_children(self) -> list[MultiPolygon]:
        return list([MULTIPOLYGONS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for mpg in self.get_children():
            points.extend(mpg.get_points())
        return points

    def remove_close_points(self, precision: int) -> None:
        """Remove close points (within precision)."""
        for mpg in self.get_children():
            for pg in mpg.get_children():
                points = pg.get_children()
                assert len(points)
                prev_pt = points[0]
                for i in range(1, len(points)):
                    pt = points[i]
                    if pt.close_to(prev_pt, precision):
                        pg.remove_point(pt.id_)
                    else:
                        prev_pt = pt

    def __add__(self, map_obj: Self) -> Self:
        s1: str = self.klass.fpath.stem
        s2: str = map_obj.klass.fpath.stem
        self.svg_fpath = s1 + '_' + s2 + '.svg'

        self.children.extend(map_obj.children)
        return self
