#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg import common
from geojson2svg.common import Point, Polygon, MultiPolygon

PRECISION: int = 3  # px


class MapObj(common.MapObj):

    def run(self) -> None:
        self.convert_coords_to_px()
        self.collapse_border_gaps()
        self.remove_close_points(PRECISION)
        self.round_point_coordinates(1)
        self.remove_needles()
        self.count_points()
        self.generate_svg_code()

    def collapse_border_gaps(self) -> None:
        """Merge neighbour points of different multipolygons to avoid gaps
        between paths. If polygons are crossed by X and Y, then search for
        close points. Otherwise - do not waste time.
        TODO This alg is too slow - can not process 3.cities.geojson.
        """
        # Find overlapping multipolygons
        mergable_multipolygon_pairs: \
            list[tuple[MultiPolygon, MultiPolygon]] = []
        for i in range(len(self.get_children()) - 1):
            mp1 = self.get_children()[i]
            for j in range(i + 1, len(self.get_children())):
                mp2 = self.get_children()[j]
                if common.is_overlapping_with(mp1, mp2):
                    mergable_multipolygon_pairs.append((mp1, mp2))

        # Find overlapping polygons
        mergable_polygon_pairs: \
            list[tuple[Polygon, Polygon]] = []
        for mp1, mp2 in mergable_multipolygon_pairs:
            for pg1 in mp1.get_children():
                for pg2 in mp2.get_children():
                    if common.is_overlapping_with(pg1, pg2):
                        mergable_polygon_pairs.append((pg1, pg2))

        # Find neighbour points
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
                    if pt1.close_to(pt2, PRECISION):
                        points_to_merge2.append(pt2)
                for pt in points_to_merge2:
                    points2.remove(pt)
                common.merge_points_to(points_to_merge2, pt1)

                # Merge points on 1st polygon
                for pt2 in points1[1:]:
                    if pt1.close_to(pt2, PRECISION):
                        points_to_merge1.append(pt2)
                for pt in points_to_merge1:
                    points1.remove(pt)
                common.merge_points_to(points_to_merge1, pt1)
                points1.remove(pt1)
