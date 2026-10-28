#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base.point import Point, merge_points_to
from base.polygon import Polygon, find_overlapping_polygons
from base.multipolygon import find_overlapping_multipolygons
from base.mapobj import MapObj
from services.filters import RemoveSamePoints, RemoveNeedles
from services.log import r
from services.transform import Round, Coords2Px
from core.utils import recursive_quad_merge, collapse_gap_1, collapse_gap_2


class Good0(MapObj):

    def run(self) -> None:
        Coords2Px(self).apply()
        Round(self).apply(precision=1)
        for mp in self.get_children():
            for polygon in mp.get_children():
                RemoveNeedles(polygon.get_points()).apply()
        r.info(f'Point count: {len(self.get_points())}')


class Good1(MapObj):

    PRECISION: int = 3  # px

    def run(self) -> None:
        Coords2Px(self).apply()

        # Find overlapping multipolygons
        multipolygons = self.get_children()
        mergable_multipolygon_pairs =\
            find_overlapping_multipolygons(multipolygons)

        # Find overlapping polygons
        mergable_polygon_pairs: list[tuple[Polygon, Polygon]] = []
        for mp1, mp2 in mergable_multipolygon_pairs:
            polygons = mp1.get_children() + mp2.get_children()
            list_ = find_overlapping_polygons(polygons)
            mergable_polygon_pairs.extend(list_)

        self.collapse_gaps(mergable_polygon_pairs, self.PRECISION)
        self.remove_close_points(self.PRECISION)
        Round(self).apply(precision=1)
        for mp in self.get_children():
            for polygon in mp.get_children():
                RemoveNeedles(polygon.get_points()).apply()
        r.info(f'Point count: {len(self.get_points())}')

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
            r.info(f'Polygon pair {counter} of {len(mergable_polygon_pairs)}'
                   + ' ' * 8 + '\r')

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
        Coords2Px(self).apply()
        Round(self).apply(precision=self.PRECISION)  # !important!
        self.remove_close_points(self.PRECISION)  # !important!

        # Find overlapping multipolygons
        multipolygons = self.get_children()
        mergable_multipolygon_pairs =\
            find_overlapping_multipolygons(multipolygons)

        # Find overlapping polygons
        mergable_polygon_pairs: list[tuple[Polygon, Polygon]] = []
        for mp1, mp2 in mergable_multipolygon_pairs:
            polygons = mp1.get_children() + mp2.get_children()
            list_ = find_overlapping_polygons(polygons)
            mergable_polygon_pairs.extend(list_)

        self.collapse_gaps(mergable_polygon_pairs, self.PRECISION)
        r.info(f'Point count: {len(self.get_points())}')

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
            r.info(f'Polygon pair {counter} of {len(mergable_polygon_pairs)}'
                   + ' '*8 + '\r')
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
        Coords2Px(self).apply()
        Round(self).apply(precision=self.PRECISION)
        self.remove_close_points(self.PRECISION)

        # Find overlapping multipolygons
        multipolygons = self.get_children()
        mergable_multipolygon_pairs =\
            find_overlapping_multipolygons(multipolygons)

        # Find overlapping polygons
        mergable_polygon_pairs: list[tuple[Polygon, Polygon]] = []
        for mp1, mp2 in mergable_multipolygon_pairs:
            polygons = mp1.get_children() + mp2.get_children()
            list_ = find_overlapping_polygons(polygons)
            mergable_polygon_pairs.extend(list_)

        for points1, points2 in self.get_border_point_clouds(
                mergable_polygon_pairs, self.PRECISION):
            collapse_gap_2(points1, points2, self.PRECISION)

        r.info(f'Point count: {len(self.get_points())}')

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
            r.info(f'Polygon pair {counter} of {len(mergable_polygon_pairs)}'
                   + ' '*8 + '\r')
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
        Coords2Px(self).apply()
        Round(self).apply(precision=self.PRECISION)
        RemoveSamePoints(self.get_points()).apply()


class Dev(MapObj):

    PRECISION: int = 1  # px

    def run(self) -> None:
        Coords2Px(self).apply()
        Round(self).apply(precision=self.PRECISION)
        recursive_quad_merge(self.get_points(), self.PRECISION * 2)
        self.remove_close_points(self.PRECISION)
        r.info(f'Point count: {len(self.get_points())}')
