#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import os
from typing import Self, override

from base.lands import Land
from model.feature import Feature, get_features
from model.point import Point, create_point
from model.linestring import create_linestring
from model.polygon import create_polygon
from model.obj import Obj


PARENTS: dict[int, str] = dict()  # id_: name


class MapObj(Obj):
    """Parent of MultiPolygon, consists of multiple MultiPolygon objects."""

    def __init__(self, klass: type[Land]) -> None:
        super().__init__([])
        os.chdir(os.path.dirname(__file__))
        self.klass = klass
        self.svg_fpath = klass.fpath.with_suffix('.svg')
        self.read_features()
        self.set_bbox()

    def read_features(self) -> None:
        assert self.klass.fpath.exists(), \
            f'File not found: {self.klass.fpath}'

        for feature in get_features(self.klass.fpath):
            """
            p = feature.properties
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
            """

            g = feature.geometry
            if g.type == 'Point':
                pt = create_point(g.coordinates, self)
                feature.add_child(pt)
            elif g.type == 'LineString':
                ls = create_linestring(g.coordinates)
                feature.add_child(ls)
            elif g.type == 'Polygon':
                pg = create_polygon(g.coordinates)
                feature.add_child(pg)
            elif g.type == 'MultiPoint':
                for xy in g.coordinates:
                    pt = create_point(xy, self)
                    feature.add_child(pt)
            elif g.type == 'MultiLineString':
                for c in g.coordinates:
                    ls = create_linestring(c)
                    feature.add_child(ls)
            elif g.type == 'MultiPolygon':
                for coord in g.coordinates:
                    pg = create_polygon(coord)
                    feature.add_child(pg)
            self.children.append(feature)

    @override
    def get_children(self) -> list[Feature]:
        return self.children

    @override
    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for feature in self.get_children():
            for ch in feature.get_children():
                if isinstance(ch, Point):
                    points.append(ch)
                else:
                    points.extend(ch.get_points())
        return points

    @override
    def get_svg_code(self) -> str:
        return '\n'

    @override
    def get_svg_style(self) -> str:
        return '\n'

    def remove_close_points(self, precision: int) -> None:
        """Remove close points (within precision).
        TODO Move to services.filters
        """
        for feature in self.get_children():
            for ch in feature.get_children():
                points = ch.get_points()
                if len(points) == 0:
                    continue
                prev_pt = points[0]
                for i in range(1, len(points)):
                    pt = points[i]
                    if pt.close_to(prev_pt, precision):
                        ch.remove_point(pt.id_)
                    else:
                        prev_pt = pt

    def __add__(self, map_obj: Self) -> Self:
        s1: str = self.klass.fpath.stem
        s2: str = map_obj.klass.fpath.stem
        self.svg_fpath = s1 + '_' + s2 + '.svg'

        self.children.extend(map_obj.children)
        return self

    def __str__(self) -> str:
        return f'{self.klass.fpath.name}\n' \
            + f'{self.klass.w}x{self.klass.h}\n' \
            + f'{self.bbox}\n' \
            + f'{len(self.children)} paths\n'
