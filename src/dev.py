#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test for good4 variant."""

import sys

from base.lands import Land
from base.point import POINTS, Point
from base.polygon import Polygon, find_overlapping_polygons
from base.multipolygon import find_overlapping_multipolygons
from core import Good4 as MapObj
from services.filters import Round
from services.log import r


class Qwe1(Land):
    input_name = 'qwe1.geojson'
    output_name = input_name
    w = 1000
    h = 1000


class Qwe2(Land):
    input_name = 'qwe2.geojson'
    output_name = input_name
    w = 1000
    h = 1000


class Qwe3(Land):
    input_name = 'qwe3.geojson'
    output_name = input_name
    w = 1000
    h = 1000


class Qwe4(Land):
    input_name = 'qwe4.geojson'
    output_name = input_name
    w = 1000
    h = 1000


class TestState(Land):
    input_name = '0.state.geojson'
    output_name = 'test_' + input_name


class TestRegion(Land):
    input_name = '1.regions.geojson'
    output_name = 'test_' + input_name


class TestDistrict(Land):
    input_name = '2.districts.geojson'
    output_name = 'test_' + input_name
    parent = 'vusc'


class TestCity(Land):
    input_name = '3.cities.geojson'
    output_name = 'test_' + input_name
    parent = 'okres'


class TestCityPart(Land):
    input_name = '4.city_parts.geojson'
    output_name = 'test_' + input_name
    parent = 'obec'


# def test():
#     MapObj(TestState).run()
#     MapObj(TestRegion).run()
#     MapObj(TestDistrict).run()
#     MapObj(TestCity).run()
#     MapObj(TestCityPart).run()
#     (MapObj(TestDistrict) + MapObj(TestCityPart)).run()
#     (MapObj(TestCity) + MapObj(TestCityPart)).run()
#     c = MapObj(City)
#     c.run()
#     p = MapObj(CityPart)
#     p.run()
#     map1 = d + p; map1.run()
#     map2 = c + p; map2.run()


def swap_points(id1: int, id2: int) -> None:
    pt1 = POINTS[id1]
    pt2 = POINTS[id2]
    pt1.id_ = id2
    pt2.id_ = id1
    POINTS[id1] = pt2
    POINTS[id2] = pt1


def check_order(points: list[Point]) -> None | list[Point]:
    if len(points) < 3:
        return

    for i in range(len(points) - 2):
        pt0 = points[i]
        pt1 = points[i + 1]
        pt2 = points[i + 2]
        a = all(points[i + j].tied_to <= points[i + j + 1].tied_to
                for j in range(2))
        b = all(points[i + j].tied_to >= points[i + j + 1].tied_to
                for j in range(2))
        if not (a or b):
            r.debug('{}, {}, {} - {}, {}, {} - {}, {}'
                    .format(pt0.id_, pt1.id_, pt2.id_,
                            pt0.tied_to, pt1.tied_to, pt2.tied_to, a, b))
            swap_points(pt1.tied_to, pt2.tied_to)
            points[i + 1], points[i + 2] = points[i + 2], points[i + 1]
            return points


def tie_border_points(points1: list[Point],
                      points2: list[Point], precision: int) \
                        -> tuple[list[Point], list[Point]]:
    for pt1 in points1:
        if pt1.tied_to:
            continue
        for pt2 in points2:
            if pt2.tied_to:
                continue
            if pt1.close_to(pt2, precision):
                pt2.x = pt1.x
                pt2.y = pt1.y
                pt2.tied_to = pt1.id_
                pt1.tied_to = pt2.id_
                break

    return points1, points2


def remove_points_without_pair(points: list[Point]) -> list[Point]:
    removed_points: list[Point] = []
    for pt in points:
        if pt.tied_to == sys.maxsize:
            removed_points.append(pt)
    for pt in removed_points:
        pg = pt.parent
        if pg is None:
            r.warning(f'Point {pt.id_} has no parent polygon.')
            continue
        pg.remove_point(pt.id_)
        points.remove(pt)
    return points


def get_border_points(
        mergable_polygon_pairs:
        list[tuple[Polygon, Polygon]], precision: int) \
        -> list[tuple[list[Point], list[Point]]]:
    """Find mergable neighbour points between multipolygons."""
    BORDER_UTMOST_POINTS: list[Point] = []
    counter = 0
    border_points_list: list[tuple[list[Point], list[Point]]] = []
    for pg1, pg2 in mergable_polygon_pairs:
        counter += 1
        points1 = pg1.get_children()
        points2 = pg2.get_children()
        print(f'Polygon pair {counter} of {len(mergable_polygon_pairs)}'
              + ' ' * 8 + '\r', end='')
        border_points1: list[Point] = []
        border_points2: list[Point] = []
        for pt1 in points1:
            for pt2 in points2:
                if pt1.close_to(pt2, precision):
                    border_points1.append(pt1)
                    break
        for pt2 in points2:
            for pt1 in points1:
                if pt2.close_to(pt1, precision):
                    border_points2.append(pt2)
                    break
        border_points_list.append((border_points1, border_points2))
        if len(border_points1) >= 2:
            border_points1[0].utmost = True
            border_points1[-1].utmost = True
            BORDER_UTMOST_POINTS.extend([border_points1[0],
                                         border_points1[-1]])
        if len(border_points2) >= 2:
            border_points2[0].utmost = True
            border_points2[-1].utmost = True
            BORDER_UTMOST_POINTS.extend([border_points2[0],
                                         border_points2[-1]])

    return border_points_list


def test() -> None:
    """Create SVG image from custom points.
    Coordinates are measured from top left display corner.
    """
    m = MapObj(Qwe1)
    Round(m.get_points()).apply(precision=m.PRECISION)
    m.remove_close_points(m.PRECISION)

    # Find overlapping multipolygons
    multipolygons = m.get_children()
    mergable_multipolygon_pairs =\
        find_overlapping_multipolygons(multipolygons)

    # Find overlapping polygons
    mergable_polygon_pairs: list[tuple[Polygon, Polygon]] = []
    for mp1, mp2 in mergable_multipolygon_pairs:
        polygons = mp1.get_children() + mp2.get_children()
        list_ = find_overlapping_polygons(polygons)
        mergable_polygon_pairs.extend(list_)

    for points1, points2 in \
            get_border_points(mergable_polygon_pairs, m.PRECISION):
        points1, points2 = tie_border_points(points1, points2, m.PRECISION)
        points2, points1 = tie_border_points(points2, points1, m.PRECISION)
        points1 = remove_points_without_pair(points1)
        points2 = remove_points_without_pair(points2)
        points1 = check_order(points1)
        i = 4
        while points1 and i > 0:
            i -= 1
            points1 = check_order(points1)
    m.generate_svg_code(show_ids=True)
