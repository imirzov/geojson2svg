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

from geojson2svg.model.polygon import Polygon
from geojson2svg.model.multipolygon import MultiPolygon

PARENTS: dict[int, str] = dict()  # id_: name


def find_overlapping_polygons(
        multipolygon_pairs: list[tuple[MultiPolygon, MultiPolygon]]) \
            -> list[tuple[Polygon, Polygon]]:
    mergable_polygon_pairs: list[tuple[Polygon, Polygon]] = []
    for mp1, mp2 in multipolygon_pairs:
        for pg1 in mp1.get_children():
            for pg2 in mp2.get_children():
                if pg1.is_overlapping_with(pg2):
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
