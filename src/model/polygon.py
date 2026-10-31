#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Points forming a closed shape. Possibly with holes."""

from __future__ import annotations
from typing import override

from model.point import POINTS, pt_type, Point, create_point
from model.obj import Obj


# {id_: Polygon}
POLYGONS: dict[str | int, Polygon] = dict()
_next_ring_id = 0
ring_type = list[pt_type]

# {id_: Ring}
RINGS: dict[str | int, Ring] = dict()
_next_id = 0
pg_type = list[list[pt_type]]


class Ring(Obj):
    COORDINATES_LIST_DEPTH = 2

    def __init__(self, coordinates: ring_type) -> None:
        super().__init__(coordinates)
        global _next_ring_id
        self.id_ = _next_ring_id
        _next_ring_id += 1
        assert self.check_coords(), str(coordinates)[:100]
        for xy in coordinates:
            pt = create_point(xy, self)
            self.children.append(pt.id_)
        self.set_bbox()

    @override
    def get_children(self) -> list[Point]:
        return list([POINTS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        return self.get_children()

    @override
    def get_svg_code(self) -> str:
        coords = ' '.join(f'{pt.x},{pt.y}' for pt in self.get_children())
        return f'<polygon points="{coords}" />\n'

    @override
    def get_svg_style(self) -> str:
        return 'polygon {fill:none;stroke:black;stroke-width:0.2}\n'

    def remove_point(self, id_: int) -> None:
        assert id_ in POINTS, \
            f'Point {id_} not found in POINTS.'
        pt = POINTS[id_]
        assert pt.utmost is False, \
            f'Point {id_} is utmost and cannot be removed.'
        POINTS.pop(id_)
        assert id_ in self.children, \
            f'Ring {self.id_} has no point {id_}'
        self.children.remove(id_)


class Polygon(Obj):
    COORDINATES_LIST_DEPTH = 3

    def __init__(self, coordinates: pg_type) -> None:
        super().__init__(coordinates)
        global _next_id
        self.id_ = _next_id
        _next_id += 1
        assert self.check_coords(), str(coordinates)[:100]
        for coords in coordinates:
            ring = create_ring(coords)
            self.children.append(ring.id_)
        self.set_bbox()

    @override
    def get_children(self) -> list[Ring]:
        return list([RINGS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for ring in self.get_children():
            points.extend(ring.get_points())
        return points

    @override
    def get_svg_code(self) -> str:
        code = '<path d="'
        # code += 'M 50,50 L 350,50 L 350,350 L 50,350 Z '
        # code += 'M 90,90 L 180,90 L 180,180 L 90,180 Z '
        # code += 'M 220,220 L 310,220 L 310,310 L 220,310 Z'
        for ring in self.get_children():
            points = ring.get_points()
            if points:
                code += f'M {points[0].x},{points[0].y} '
                for pt in points[1:]:
                    code += f'L {pt.x},{pt.y} '
                code += 'Z'
        code += '" fill-rule="evenodd" />\n'
        return code

    @override
    def get_svg_style(self) -> str:
        return 'path {fill:black; stroke:white; stroke-width:0.2}\n'

    def remove_point(self, id_: int) -> None:
        assert id_ in POINTS, \
            f'Point {id_} not found in POINTS.'
        pt = POINTS[id_]
        assert pt.utmost is False, \
            f'Point {id_} is utmost and cannot be removed.'
        POINTS.pop(id_)
        found = False
        for ring_id in self.children:
            ring = RINGS[ring_id]
            if id_ in ring.children:
                ring.remove_point(id_)
                found = True
                break
        assert found, \
            f'Polygon {self.id_} has no point {id_}'


def create_ring(coordinates: ring_type) -> Ring:
    rg = Ring(coordinates)
    RINGS[rg.id_] = rg
    return rg


def create_polygon(coordinates: pg_type) -> Polygon:
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
