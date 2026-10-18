#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg.common import Point, Polygon, MapObj, \
    find_overlapping_multipolygons, find_overlapping_polygons
from geojson2svg.utils import collapse_gap_1


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
