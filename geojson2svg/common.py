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

from abc import ABC
import json
import os
import sys
from typing import Self, Any
import unidecode

import settings
from settings import report as r
from geojson2svg.lands import Land

PARENTS: dict[int, str] = dict()  # id_: name
POINTS: dict[str | int, Point] = dict()  # id_: (x, y)
POLYGONS: dict[str | int, Polygon] = dict()  # id_: Polygon
MULTIPOLYGONS: dict[str | int, MultiPolygon] = dict()  # id_: MultiPolygon


class Obj(ABC):

    def __init__(self) -> None:
        self.id_ = 0
        self.children: list[int | str] = list()
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0

    def get_bbox(self) -> tuple[float, float, float, float]:
        return get_obj_bbox(self)

    def get_children(self) -> Any:
        pass


class Point(Obj):

    def __init__(self, x: float, y: float,
                 parent: Polygon | None = None) -> None:
        self.id_ = len(POINTS)
        self.x = x
        self.y = y
        self.parent = parent
        self.xmin = self.x
        self.xmax = self.x
        self.ymin = self.y
        self.ymax = self.y
        self.merged = False
        self.tied_to = sys.maxsize
        self.utmost = False

    def set_parent(self, parent: Polygon) -> None:
        self.parent = parent

    def round(self, precision: int) -> None:
        self.x = round(self.x // precision * precision)
        self.y = round(self.y // precision * precision)
        self.xmin = self.x
        self.xmax = self.x
        self.ymin = self.y
        self.ymax = self.y

    def squared_distance_to(self, pt: Self) -> float:
        if self.id_ == pt.id_:
            return 1e+9
        return (pt.x - self.x)**2 + (pt.y - self.y)**2

    def close_to(self, pt: Self, precision: int) -> bool:
        if abs(self.x - pt.x) > precision:
            return False
        if abs(self.y - pt.y) > precision:
            return False
        return True

    def delete(self) -> None:
        if not self.utmost:
            pg = self.parent
            if pg is None:
                r.warning(f'Parent polygon is None for point {self.id_}')
                return
            pg.remove_point(self.id_)
            if self.tied_to < sys.maxsize:
                pg = POINTS[self.tied_to].parent
                if pg is None:
                    r.warning('Parent polygon is None '
                              f'for tied point {self.tied_to}')
                    return
                pg.remove_point(self.tied_to)

    def __str__(self) -> str:
        return 'Point {} x={} y={} tied_to={} utmost={}' \
            .format(self.id_, self.x, self.y, self.tied_to, self.utmost)


class Polygon(Obj, ABC):

    def __init__(self, coordinates: list[tuple[float, float]]) -> None:
        self.id_ = len(POLYGONS)
        assert is_polygon(coordinates)
        # self.children: list[int] = list()  # list of point ids
        self.set_children(coordinates)
        self.converted = False
        self.xmin, self.xmax, self.ymin, self.ymax =\
            get_bbox(self.get_children())

    def set_children(self, coordinates: list[tuple[float, float]]) -> None:
        for x, y in coordinates:
            new_pt = create_point(x, y, self)
            self.children.append(new_pt.id_)

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

    def convert_coords_to_px(self,
                             min_x: float, max_x: float,
                             min_y: float, max_y: float,
                             w: float, h: float) -> None:
        if not self.converted and max_x != min_x and max_y != min_y:
            for p in self.get_children():
                p.x = (p.x - min_x) / (max_x - min_x) * w
                p.y = (max_y - p.y) / (max_y - min_y) * h
        self.converted = True


class MultiPolygon(Obj, ABC):

    def __init__(self, path_id: str,
                 coordinates: list[list[list[tuple[float, float]]]]) -> None:
        self.path_id = path_id
        # self.children: list[int] = list()
        self.set_children(coordinates)
        self.xmin, self.xmax, self.ymin, self.ymax = get_obj_bbox(self)

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

    def get_children(self) -> list[Polygon]:
        return list([POLYGONS[id_] for id_ in self.children])


class MapObj(Obj):

    def __init__(self, klass: type[Land]) -> None:
        os.chdir(os.path.dirname(__file__))
        self.klass = klass
        self.svg_fpath = os.path.join(
            settings.files,
            os.path.splitext(self.klass.output_name)[0] + '.svg')
        # self.children: list[str] = []
        self.read_children()
        r.info('{}x{}, {} paths, {} points before, {}\n'
               .format(self.klass.w, self.klass.h,
                       len(self.children), len(POINTS),
                       unidecode.unidecode(self.klass.input_name)))

    def read_children(self) -> None:
        """Read polygon coordinates:
        {
            id1: [(x11, y11), (x12, y12), ...],
            id2: [(x21, y21), (x22, y22), ...],
            ...
        }
        """
        fpath = settings.files / self.klass.input_name
        if not fpath.exists():
            r.error(f'File not found: {fpath}')
            raise SystemExit

        with open(fpath, 'r', encoding=settings.encoding) as f:
            geojson = json.load(f)
        for feature in geojson['features']:
            p = feature['properties']
            path_id = p[self.klass.name]
            if self.klass.parent is not None:
                if self.klass.parent in p and self.klass.id in p:
                    if p[self.klass.parent] in PARENTS:
                        path_id = PARENTS[p[self.klass.parent]] + '_' + path_id
                    PARENTS[p[self.klass.id]] = path_id
            else:
                if self.klass.id in p:
                    PARENTS[p[self.klass.id]] = p[self.klass.name]
            path_id = settings.to_en(path_id)

            if feature['geometry']['type'] == 'MultiPolygon':
                coordinates = feature['geometry']['coordinates']
            else:
                coordinates = [feature['geometry']['coordinates']]
            mp = create_multipolygon(path_id, coordinates)
            self.children.append(mp.path_id)

    def get_children(self) -> list[MultiPolygon]:
        return list([MULTIPOLYGONS[id_] for id_ in self.children])

    def convert_coords_to_px(self) -> None:
        """Convert latitude and longitude GeoJson coords
        to Land's width (w) and height (h) in pixels.
        """
        min_x, max_x, min_y, max_y = get_obj_bbox(self)
        for mp in self.get_children():
            for pg in mp.get_children():
                pg.convert_coords_to_px(min_x, max_x, min_y, max_y,
                                        self.klass.w, self.klass.h)

    def round_point_coordinates(self, precision: int) -> None:
        """Round all point coordinates to precision."""
        assert type(precision) is int, 'Precision should be INT type.'
        for mp in self.get_children():
            for pg in mp.get_children():
                for pt in pg.get_children():
                    pt.round(precision)

    def remove_needles(self) -> None:
        for mp in self.get_children():
            for pg in mp.get_children():
                point_ids_to_remove: set[int] = set()
                points = pg.get_children()
                for i in range(len(points) - 3):
                    pt0 = points[i]
                    pt1 = points[i + 1]
                    pt2 = points[i + 2]
                    if pt0.x == pt2.x and pt0.y == pt2.y:
                        point_ids_to_remove.add(pt1.id_)
                for id_ in point_ids_to_remove:
                    pg.remove_point(id_)

    def remove_close_points(self, precision: int) -> None:
        """Remove close points (within precision)."""
        for mp in self.get_children():
            for pg in mp.get_children():
                prev_pt = None
                for pt in pg.get_children():
                    if prev_pt is not None:
                        if pt.close_to(prev_pt, precision):
                            pg.remove_point(pt.id_)
                            continue
                    prev_pt = pt

    def filter_points_with_same_coords(self) -> None:
        for mp in self.get_children():
            for pg in mp.get_children():
                points = pg.get_children()
                points = filter_points_with_same_coords(points)
                coords = [(pt.x, pt.y) for pt in points]
                pg.set_children(coords)

    def count_points(self) -> None:
        counter = 0
        for mp in self.get_children():
            for pg in mp.get_children():
                counter += len(pg.get_children())
        r.info('{} points after.\n'.format(counter))

    def __add__(self, map_obj: Self) -> Self:
        s1: str = os.path.splitext(self.svg_fpath)[0]
        s2: str = os.path.basename(
            os.path.splitext(map_obj.klass.output_name)[0])
        self.svg_fpath = s1 + '_' + s2 + '.svg'

        self.children.extend(map_obj.children)
        return self

    def generate_svg_code(self, show_ids: bool = False) -> None:
        """Create paths and place them into SVG code."""
        pad = ' ' * 4
        svg_paths: list[str] = []
        for mp in self.get_children():
            coords = ''
            for pg in mp.get_children():
                coords += 'M'  # NOTE use small letter for dx,dy
                for pt in pg.get_children():
                    # coords += ' {:.3f},{:.3f}'.format(dx, dy) # for dx,dy
                    coords += f' {pt.x} {pt.y}'
                    if show_ids:
                        svg_paths.append('<text x="{}" y="{}">{}</text>\n'
                                         .format(pt.x + 10 * pg.id_,
                                                 pt.y - 10 * pg.id_, pt.id_))
                coords += ' Z'  # NOTE use small letter for dx,dy
            svg_paths.append(f'{pad}<path d="{coords}" id="{mp.path_id}" />\n')
        # for pt in BORDER_UTMOST_POINTS:
        #     svg_paths.append(f'{pad}<circle cx="{pt.x}" cy="{pt.y}" '
        #                      'r="0.5" style="fill:black;" />\n')
        # for id_ in DISORDERED_POINTS:
        #     pt = POINTS[id_]
        #     r.debug(f'[{pt.x}, {pt.y}]')
        #     svg_paths.append(f'{pad}<circle cx="{pt.x}" cy="{pt.y}" '
        #                      'r="0.5" style="fill:red;" />\n')
        # TODO remove CSS
        svg_code: list[str] = [
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n',
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {self.klass.w} {self.klass.h}">\n',
            # pad + '<style>\n',
            # pad * 2 + 'path {fill: black; stroke: white; '
            #           'stroke-width: 0.2px}\n',
            # pad * 2 + 'path#plzensky-kraj {fill: transparent; '
            #           'stroke: black; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#karlovarsky-kraj {fill: transparent; '
            #           'stroke: red; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#pardubicky-kraj {fill: transparent; '
            #           'stroke: black; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#kralovehradecky-kraj {fill: transparent; '
            #           'stroke: red; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#stredocesky-kraj {fill: transparent; '
            #           'stroke: black; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#jihocesky-kraj {fill: transparent; '
            #           'stroke: red; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#ustecky-kraj {fill: transparent; stroke: blue; '
            #           'stroke-width: 0.5px}\n',
            # pad + '</style>\n',
            *svg_paths,
            '</svg>',
        ]
        with open(self.svg_fpath, 'w', encoding=settings.encoding) as f:
            f.writelines(svg_code)


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


def get_obj_bbox(obj: Obj | Polygon | MultiPolygon | MapObj) \
        -> tuple[float, float, float, float]:
    """Calculate bounding box: min and max X and Y coordinates."""
    min_x = 1e+9
    min_y = 1e+9
    max_x = -1e+9
    max_y = -1e+9
    for ch in obj.get_children():
        min_x = min(ch.xmin, min_x)
        max_x = max(ch.xmax, max_x)
        min_y = min(ch.ymin, min_y)
        max_y = max(ch.ymax, max_y)
    return min_x, max_x, min_y, max_y


def get_bbox(points: list[Point]) -> tuple[float, float, float, float]:
    """Calculate bounding box: min and max X and Y coordinates."""
    min_x = 1e+9
    min_y = 1e+9
    max_x = -1e+9
    max_y = -1e+9
    for pt in points:
        min_x = min(pt.x, min_x)
        max_x = max(pt.x, max_x)
        min_y = min(pt.y, min_y)
        max_y = max(pt.y, max_y)
    return min_x, max_x, min_y, max_y


def merge_points_to(points: list[Point], point: Point) -> None:
    for pt in points:
        pt.x = point.x
        pt.y = point.y


def is_overlapping_with(obj1: Obj, obj2: Obj) -> bool:

    def f(obj1: Obj, obj2: Obj) -> bool:
        # Conditions:
        c1 = False
        c2 = False

        if obj1.xmin <= obj2.xmin and obj2.xmin <= obj1.xmax:
            c1 = True
        if obj1.xmin <= obj2.xmax and obj2.xmax <= obj1.xmax:
            c1 = True

        if obj1.ymin <= obj2.ymin and obj2.ymin <= obj1.ymax:
            c2 = True
        if obj1.ymin <= obj2.ymax and obj2.ymax <= obj1.ymax:
            c2 = True

        if c1 and c2:
            return True
        return False

    return f(obj1, obj2) or f(obj2, obj1)


def filter_points_with_same_coords(points: list[Point]) -> list[Point]:
    filtered_points: list[Point] = []
    for pt1 in points:
        unique = True
        for pt2 in filtered_points:
            if pt1.x == pt2.x and pt1.y == pt2.y:
                unique = False
                pg = pt1.parent
                if pg is None:
                    r.warning(f'Point {pt1.id_} has no parent polygon.')
                else:
                    pg.remove_point(pt1.id_)
        if unique:
            filtered_points.append(pt1)
    r.debug('Before filtering: {}, after: {}'
            .format(len(points), len(filtered_points)))
    return filtered_points


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
