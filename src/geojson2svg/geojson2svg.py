#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg.common import (
    Point, Polygon, find_overlapping_multipolygons,
    find_overlapping_polygons, merge_points_to)
from geojson2svg.mapobj import MapObj
from geojson2svg.utils import (
    recursive_quad_merge, collapse_gap_1, collapse_gap_2)


class Good0(MapObj):

    def run(self) -> None:
        self.convert_coords_to_px()
        self.round_point_coordinates(1)
        self.remove_needles()
        self.count_points()
        self.generate_svg_code()


class Good1(MapObj):

    PRECISION: int = 3  # px

    def run(self) -> None:
        self.convert_coords_to_px()

        # Find overlapping multipolygons
        multipolygons = self.get_children()
        mergable_multipolygon_pairs =\
            find_overlapping_multipolygons(multipolygons)

        # Find overlapping polygons
        mergable_polygon_pairs = \
            find_overlapping_polygons(mergable_multipolygon_pairs)

        self.collapse_gaps(mergable_polygon_pairs, self.PRECISION)
        self.remove_close_points(self.PRECISION)
        self.round_point_coordinates(1)
        self.remove_needles()
        self.count_points()
        self.generate_svg_code()

    def collapse_gaps(self, mergable_polygon_pairs:
                      list[tuple[Polygon, Polygon]],
                      precision: int) -> None:
        """Merge neighbour points of different polygons
        to avoid gaps between paths.

        If polygons are crossed by X and Y,
        then search for close points. Otherwise - do not waste time.

        TODO This alg is too slow - can not process 3.cities.geojson.
        """
        counter = 0
        for pg1, pg2 in mergable_polygon_pairs:
            counter += 1
            print(f'Polygon pair {counter} of {len(mergable_polygon_pairs)}'
                  + ' ' * 8 + '\r', end='')

            points1 = pg1.get_children()
            points2 = pg2.get_children()
            while points1 and points2 and len(points1 + points2) >= 2:
                points_to_merge1: list[Point] = list()
                points_to_merge2: list[Point] = list()
                pt1 = points1[0]

                # Merge points on 2nd polygon
                for pt2 in points2:
                    if pt1.close_to(pt2, precision):
                        points_to_merge2.append(pt2)
                for pt in points_to_merge2:
                    points2.remove(pt)
                merge_points_to(points_to_merge2, pt1)

                # Merge points on 1st polygon
                for pt2 in points1[1:]:
                    if pt1.close_to(pt2, precision):
                        points_to_merge1.append(pt2)
                for pt in points_to_merge1:
                    points1.remove(pt)
                merge_points_to(points_to_merge1, pt1)
                points1.remove(pt1)


class Good2(MapObj):

    PRECISION: int = 3  # px

    def run(self) -> None:
        """NOTE Quite fast in compraison with _good1."""
        self.convert_coords_to_px()
        self.round_point_coordinates(self.PRECISION)  # !important!
        self.remove_close_points(self.PRECISION)  # !important!

        # Find overlapping multipolygons
        multipolygons = self.get_children()
        mergable_multipolygon_pairs =\
            find_overlapping_multipolygons(multipolygons)

        # Find overlapping polygons
        mergable_polygon_pairs = \
            find_overlapping_polygons(mergable_multipolygon_pairs)

        self.collapse_gaps(mergable_polygon_pairs, self.PRECISION)
        self.count_points()
        self.generate_svg_code()

    def collapse_gaps(self, mergable_polygon_pairs:
                      list[tuple[Polygon, Polygon]],
                      precision: int) -> None:
        """Find mergable neighbour points between polygons.
        NOTE Alg does not merge borders fully - white triangles remain.
        """
        counter = 0
        for pg1, pg2 in mergable_polygon_pairs:
            counter += 1
            points1 = pg1.get_points()
            points2 = pg2.get_points()
            print(f'Polygon pair {counter} of {len(mergable_polygon_pairs)}'
                  + ' '*8 + '\r', end='')
            merge_cloud1: list[Point] = []
            merge_cloud2: list[Point] = []
            for pt1 in points1:
                for pt2 in points2:
                    if pt1.close_to(pt2, precision):
                        merge_cloud1.append(pt1)
                        break
            for pt2 in points2:
                for pt1 in points1:
                    if pt2.close_to(pt1, precision):
                        merge_cloud2.append(pt2)
                        break
            collapse_gap_1(merge_cloud1, merge_cloud2)


class Good3(MapObj):

    PRECISION: int = 3  # px

    def run(self) -> None:
        """NOTE Quite fast in compraison with _good1."""
        self.convert_coords_to_px()
        self.round_point_coordinates(self.PRECISION)
        self.remove_close_points(self.PRECISION)

        # Find overlapping multipolygons
        multipolygons = self.get_children()
        mergable_multipolygon_pairs =\
            find_overlapping_multipolygons(multipolygons)

        # Find overlapping polygons
        mergable_polygon_pairs = \
            find_overlapping_polygons(mergable_multipolygon_pairs)

        for points1, points2 in self.get_border_point_clouds(
                mergable_polygon_pairs, self.PRECISION):
            collapse_gap_2(points1, points2, self.PRECISION)

        self.count_points()
        self.generate_svg_code()

    def get_border_point_clouds(
            self, mergable_polygon_pairs:
            list[tuple[Polygon, Polygon]],
            precision: int) -> list[tuple[list[Point], list[Point]]]:
        """Find mergable neighbour points between polygons."""
        counter = 0
        border_point_clouds: list[tuple[list[Point], list[Point]]] = []
        for pg1, pg2 in mergable_polygon_pairs:
            counter += 1
            points1 = pg1.get_children()
            points2 = pg2.get_children()
            print(f'Polygon pair {counter} of {len(mergable_polygon_pairs)}'
                  + ' '*8 + '\r', end='')
            merge_cloud1: list[Point] = []
            merge_cloud2: list[Point] = []
            for pt1 in points1:
                for pt2 in points2:
                    if pt1.close_to(pt2, precision):
                        merge_cloud1.append(pt1)
                        break
            for pt2 in points2:
                for pt1 in points1:
                    if pt2.close_to(pt1, precision):
                        merge_cloud2.append(pt2)
                        break
            border_point_clouds.append((merge_cloud1, merge_cloud2))

        return border_point_clouds


class Good4(MapObj):

    PRECISION: int = 3  # px

    def run(self) -> None:
        """NOTE For performance
        remove duplicated points before the border collapse!
        """
        self.convert_coords_to_px()
        self.round_point_coordinates(self.PRECISION)
        self.filter_points_with_same_coords()
        self.generate_svg_code()


class Dev(MapObj):

    PRECISION: int = 1  # px

    def run(self) -> None:
        self.convert_coords_to_px()
        self.round_point_coordinates(1)
        recursive_quad_merge(self.get_points(), self.PRECISION * 2)
        self.remove_close_points(self.PRECISION)
        self.count_points()
        self.generate_svg_code()
