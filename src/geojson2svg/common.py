#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Common classes and functions for geojson2svg.

Convert GeoJSON file to SVG and save.
CR map have proportions 2000x1155.
All parameters are set in Land child classes.

Conventions:
    mp - multipolygon
    pg - polygon
    pt - point

NOTE Call all images convertion at once (for correct inheritance):
    MapObj(State)
    MapObj(Region)
    MapObj(District)

NOTE Maps could be merged:
    MapObj(District) + MapObj(CityPart)

NOTE Apply style to see sublands in merged maps:
<style>
    path {fill: transparent; stroke: black; stroke-width: 1px}
    path#ceska-republika {fill: lightgray;}
    path#hlavni-mesto-praha {fill: pink;}
</style>
<style>
    path {stroke: red; stroke-width: 0.2px}
</style>

NOTE Граница области - это упорядоченный контур из точек.
Две области имеют одну общую границу, т.е. два склеенных контура.
Количество точек на общей границе с каждой стороны может быть разное.
Пограничный контур с каждой стороны должен иметь одинаковое число точек.
Точки на пограничных контурах должны иметь одинаковые координаты
(должны "склеиваться"). Не должно быть повторяющихся точек.

TODO Read svg_code from a file.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import sys
from typing import Self, Any, override

from settings import report as r

PARENTS: dict[int, str] = dict()  # id_: name
POINTS: dict[str | int, Point] = dict()  # id_: (x, y)
POLYGONS: dict[str | int, Polygon] = dict()  # id_: Polygon
MULTIPOLYGONS: dict[str | int, MultiPolygon] = dict()  # id_: MultiPolygon


class BBox:

    def __init__(self,
                 xmin: float = 0, xmax: float = 0,
                 ymin: float = 0, ymax: float = 0) -> None:
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.dx = xmax - xmin
        self.dy = ymax - ymin

    def __add__(self, other: BBox) -> BBox:
        return BBox(
            xmin=min(self.xmin, other.xmin),
            xmax=max(self.xmax, other.xmax),
            ymin=min(self.ymin, other.ymin),
            ymax=max(self.ymax, other.ymax)
        )

    def __str__(self) -> str:
        return f'BBox(xmin={self.xmin}, xmax={self.xmax}, ' \
                    f'ymin={self.ymin}, ymax={self.ymax})'


class Obj(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.id_ = 0
        self.children: list[int | str] = list()
        self.bbox = BBox()

    def set_bbox(self) -> None:
        for ch in self.get_children():
            self.bbox += ch.bbox

    @abstractmethod
    def get_children(self) -> list[Any]:
        ...

    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for obj in self.get_children():
            points.extend(obj.get_points())
        return points


class Point(Obj):

    def __init__(self, x: float, y: float,
                 parent: Polygon | None = None) -> None:
        super().__init__()
        self.id_ = len(POINTS)
        self.x = x
        self.y = y
        self.parent = parent
        self.bbox = BBox(x, x, y, y)
        self.merged = False
        self.tied_to = sys.maxsize
        self.utmost = False

    @override
    def get_children(self) -> list[Any]:
        return []

    @override
    def get_points(self) -> list[Point]:
        return []

    def round(self, precision: int) -> None:
        self.x = round(self.x // precision * precision)
        self.y = round(self.y // precision * precision)
        self.bbox = BBox(self.x, self.x, self.y, self.y)

    def close_to(self, pt: Self, precision: int) -> bool:
        if abs(self.x - pt.x) > precision:
            return False
        if abs(self.y - pt.y) > precision:
            return False
        return True

    def __str__(self) -> str:
        return 'Point {} x={} y={} tied_to={} utmost={}' \
            .format(self.id_, self.x, self.y, self.tied_to, self.utmost)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


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
            new_pt = create_point(x, y, self)
            self.children.append(new_pt.id_)

    @override
    def get_children(self) -> list[Point]:
        return list([POINTS[id_] for id_ in self.children])

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


def create_point(x: float, y: float, parent: Polygon | None = None) -> Point:
    pt = Point(x, y, parent)
    POINTS[pt.id_] = pt
    return pt


def create_polygon(coordinates: list[tuple[float, float]] = []) -> Polygon:
    pg = Polygon(coordinates)
    POLYGONS[pg.id_] = pg
    return pg


def create_multipolygon(
        path_id: str,
        coordinates: list[list[list[tuple[float, float]]]]) -> MultiPolygon:
    mp = MultiPolygon(path_id, coordinates)
    MULTIPOLYGONS[path_id] = mp
    return mp


def is_polygon(coordinates: list[tuple[float, float]]) -> bool:
    if type(coordinates) is not list:
        return False
    for coords in coordinates:
        if len(coords) != 2:
            return False
        for c in coords:
            if type(c) not in [int, float]:
                return False
    return True


def merge_points_to(points: list[Point], point: Point) -> None:
    for pt in points:
        pt.x = point.x
        pt.y = point.y


def is_overlapping_with(obj1: Obj, obj2: Obj) -> bool:
    # TODO rewrite as Obj method

    def f(obj1: Obj, obj2: Obj) -> bool:
        # Conditions:
        c1 = False
        c2 = False

        if obj1.bbox.xmin <= obj2.bbox.xmin \
                and obj2.bbox.xmin <= obj1.bbox.xmax:
            c1 = True
        if obj1.bbox.xmin <= obj2.bbox.xmax \
                and obj2.bbox.xmax <= obj1.bbox.xmax:
            c1 = True

        if obj1.bbox.ymin <= obj2.bbox.ymin \
                and obj2.bbox.ymin <= obj1.bbox.ymax:
            c2 = True
        if obj1.bbox.ymin <= obj2.bbox.ymax \
                and obj2.bbox.ymax <= obj1.bbox.ymax:
            c2 = True

        if c1 and c2:
            return True
        return False

    return f(obj1, obj2) or f(obj2, obj1)


def find_overlapping_multipolygons(
        multipolygons: list[MultiPolygon]) \
            -> list[tuple[MultiPolygon, MultiPolygon]]:
    overlapping_pairs: list[tuple[MultiPolygon, MultiPolygon]] = []
    for i in range(len(multipolygons) - 1):
        mp1 = multipolygons[i]
        for j in range(i + 1, len(multipolygons)):
            mp2 = multipolygons[j]
            if is_overlapping_with(mp1, mp2):
                overlapping_pairs.append((mp1, mp2))
    return overlapping_pairs


def find_overlapping_polygons(
        multipolygon_pairs: list[tuple[MultiPolygon, MultiPolygon]]) \
            -> list[tuple[Polygon, Polygon]]:
    mergable_polygon_pairs: list[tuple[Polygon, Polygon]] = []
    for mp1, mp2 in multipolygon_pairs:
        for pg1 in mp1.get_children():
            for pg2 in mp2.get_children():
                if is_overlapping_with(pg1, pg2):
                    mergable_polygon_pairs.append((pg1, pg2))
    return mergable_polygon_pairs


"""
def remove_unneeded_properties(feature, klass) -> dict:
    # Remove unneeded properties from geojson feature
    p = feature['properties']
    unusefulkeys = list(p.keys())
    unusefulkeys.remove(klass.id)
    unusefulkeys.remove(klass.name)
    if klass.parent:
        unusefulkeys.remove(klass.parent)
    if unusefulkeys:
        for k in unusefulkeys:
            del p[k]
        feature['properties'] = p
    return feature


def remove_duplicate_points(pg) -> list:
    result = []
    for x, y in pg:
        x = round(x, 3)
        y = round(y, 3)
        if not result or result and result[-1] != (x, y):
            result.append((x, y))
    return result


def compress_coodrinates(feature) -> dict:
    # Reduce coordinates precision. Duplicated points removed.
    c = feature['geometry']['coordinates']
    if feature['geometry']['type'] == 'MultiPolygon':
        for j, mp in enumerate(c):
            for i, pg in enumerate(mp):
                assert is_polygon(pg)
                pg = remove_duplicate_points(pg)
                feature['geometry']['coordinates'][j][i] = pg
    else:
        for i in range(len(c)):
            pg = c[i]
            assert is_polygon(pg)
            pg = remove_duplicate_points(pg)
            feature['geometry']['coordinates'][i] = pg
    return feature


def compress(klass) -> None:
    if os.path.exists(klass.input_name):
        with open(klass.input_name, 'r',
                  encoding=settings.encoding) as f:
            geojson = json.load(f)
        for i, feature in enumerate(geojson['features']):
            feature = remove_unneeded_properties(feature, klass)
            feature = compress_coodrinates(feature)
            geojson['features'][i] = feature
        with open(klass.output_name, 'w',
                  encoding=settings.encoding) as f:
            json.dump(geojson, f)


def cleanup_shapely_polygon(p: shapely.geometry.Polygon) \
        -> shapely.geometry.base.BaseGeometry:
    if p.is_valid:
        return p
    mp = p.buffer(0)
    if mp.geom_type == 'Polygon' and mp.is_valid:
        return p
    assert mp.geom_type == 'MultiPolygon'
    maap: dict[float, shapely.geometry.Polygon] = dict()
    for p in mp.geoms:
        maap[p.area] = p
    return maap[max(maap.keys())].normalize()
"""
