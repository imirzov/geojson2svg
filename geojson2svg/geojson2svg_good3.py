#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg.common import Point, Polygon, MapObj, \
    find_overlapping_multipolygons, find_overlapping_polygons
from geojson2svg.utils import collapse_gap_2


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
