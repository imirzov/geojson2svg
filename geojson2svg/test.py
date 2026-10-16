#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test for good4 variant."""

from geojson2svg.geojson2svg_good4 \
    import (MapObj, tie_border_points,
            remove_points_without_pair, check_order)
from geojson2svg.lands import Land


class Test1(Land):
    input_name = 'test1.geojson'
    output_name = 'test1.svg'
    w = 1000
    h = 1000


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


def test() -> None:
    """Create SVG image from custom points.
    Coordinates are measured from top left display corner.
    """
    m = MapObj(Test1)
    m.round_point_coordinates(m.PRECISION)
    m.remove_close_points(m.PRECISION)
    for points1, points2 in m.get_border_points(m.PRECISION):
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
