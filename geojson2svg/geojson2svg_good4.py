#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from settings import report as r
from geojson2svg import common
from geojson2svg.common import Point, Polygon, MultiPolygon


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


def swap_points(_id1: int, _id2: int) -> None:
    pt1 = common.POINTS[_id1]
    pt2 = common.POINTS[_id2]
    pt1.id_ = _id2
    pt2.id_ = _id1
    common.POINTS[_id1] = pt2
    common.POINTS[_id2] = pt1


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


class MapObj(common.MapObj):

    PRECISION: int = 3  # px
    BORDER_UTMOST_POINTS: list[Point] = []

    def run(self) -> None:
        """NOTE For performance remove duplicated points before
        the border collapse!
        """
        self.convert_coords_to_px()
        self.round_point_coordinates(self.PRECISION)
        self.filter_points_with_same_coords()
        self.generate_svg_code()

    def smooth_filter(self) -> None:
        for mp in self.get_children():
            for pg in mp.get_children():
                points = pg.get_children()
                for i in range(len(points) - 2):
                    pt0 = points[i]
                    pt1 = points[i + 1]
                    pt2 = points[i + 2]
                    pt1.x = (pt0.x + pt2.x) / 2
                    pt1.y = (pt0.y + pt2.y) / 2

    def get_border_points(self, precision: int) \
            -> list[tuple[list[Point], list[Point]]]:
        """Find mergable neighbour points between multipolygons."""

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
                self.BORDER_UTMOST_POINTS.extend([border_points1[0],
                                                  border_points1[-1]])
            if len(border_points2) >= 2:
                border_points2[0].utmost = True
                border_points2[-1].utmost = True
                self.BORDER_UTMOST_POINTS.extend([border_points2[0],
                                                  border_points2[-1]])

        return border_points_list
