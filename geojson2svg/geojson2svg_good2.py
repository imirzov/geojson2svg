#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg import common
from geojson2svg.common import Point, Polygon, MultiPolygon


def collapse_border_gaps(points1: list[Point],
                         points2: list[Point]) -> None:
    l1 = 0
    l2 = 1
    while l1 != l2:
        if not points1 or not points2:
            break
        for pt in points1:
            pts = sorted(points2, key=lambda p: (pt.x-p.x)**2 + (pt.y-p.y)**2)
            pt.x = pts[0].x
            pt.y = pts[0].y
        for pt in points2:
            pts = sorted(points1, key=lambda p: (pt.x-p.x)**2 + (pt.y-p.y)**2)
            pt.x = pts[0].x
            pt.y = pts[0].y
        l1 = len(set([p.x for p in points1] + [p.y for p in points1]))
        l2 = len(set([p.x for p in points2] + [p.y for p in points2]))


class MapObj(common.MapObj):

    PRECISION: int = 3  # px

    def run(self) -> None:
        """NOTE Quite fast in compraison with _good1."""
        self.convert_coords_to_px()
        self.round_point_coordinates(self.PRECISION)  # !important!
        self.remove_close_points(self.PRECISION)  # !important!
        self.collapse_border_gaps(self.PRECISION)
        self.count_points()
        self.generate_svg_code()

    def collapse_border_gaps(self, precision: int) -> None:
        """Find mergable neighbour points betwee multipolygons.
        TODO The same problem as in _good1 alg. Additionally
        this alg does not merge borders fully - white triangles remain.
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
            collapse_border_gaps(merge_cloud1, merge_cloud2)
