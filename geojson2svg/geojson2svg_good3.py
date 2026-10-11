#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from settings import report as r
from tools.geojson.geojson2svg import common
from tools.geojson.geojson2svg.common \
    import Point, Polygon, MultiPolygon

PRECISION: int = 3  # px


def collapse_border_gaps(points1: list[Point],
                         points2: list[Point],
                         precision: int) -> None:
    points = points1 + points2
    r.debug(f'Total {len(points)} points: {len(points1)} + {len(points2)}')
    for i in range(len(points)-1):
        pt1 = points[i]
        if pt1.x == 750 and pt1.y == 546:
            r.debug(f'{pt1.id_} points1')
        points_to_merge: list[Point] = []
        for j in range(i+1, len(points)):
            pt2 = points[j]
            if pt1.close_to(pt2, precision):
                points_to_merge.append(pt2)
        if points_to_merge:
            common.merge_points_to(points_to_merge, pt1)

    # If there is no pair point with the same coords
    pair_counter = 0
    not_pair_counter = 0
    removed_points1: list[Point] = []
    for pt1 in points1:
        if pt1.x == 750 and pt1.y == 546:
            r.debug(f'{pt1.id_} still points1')
        has_pair = False
        for pt2 in points2:
            if pt1.x == pt2.x and pt1.y == pt2.y:
                has_pair = True
                pair_counter += 1
                break
        if not has_pair:
            not_pair_counter += 1
            pg = pt1.parent
            removed_points1.append(pt1)
            if pg is None:
                r.warning(f'Point {pt1.id_} has no parent polygon.')
            else:
                r.debug(f'Point {pt1.id_} from {pg.id_} has no pair.')
                pg.remove_point(pt1.id_)
    for pt in removed_points1:
        points1.remove(pt)

    removed_points2: list[Point] = []
    for pt1 in points2:
        if pt1.x == 750 and pt1.y == 546:
            r.debug(f'{pt1.id_} still points2')
        has_pair = False
        for pt2 in points1:
            if pt1.x == pt2.x and pt1.y == pt2.y:
                has_pair = True
                pair_counter += 1
                break
        if not has_pair:
            not_pair_counter += 1
            pg = pt1.parent
            removed_points2.append(pt1)
            if pg is None:
                r.warning(f'Point {pt1.id_} has no parent polygon.')
            else:
                r.debug(f'Point {pt1.id_} from {pg.id_} has no pair.')
                pg.remove_point(pt1.id_)
    for pt in removed_points2:
        points2.remove(pt)

    if len(points1) != len(points2):
        msg = f'len(points1) = {len(points1)}, len(points2) = {len(points2)}'
        r.warning(msg)


class MapObj(common.MapObj):

    def run(self) -> None:
        """NOTE Quite fast in compraison with _good1."""
        self.convert_coords_to_px()
        self.round_point_coordinates(PRECISION)
        self.remove_close_points(PRECISION)
        for points1, points2 in self.get_border_point_clouds(PRECISION):
            collapse_border_gaps(points1, points2, PRECISION)
        self.count_points()
        self.generate_svg_code()

    def get_border_point_clouds(self, precision: int = PRECISION) \
            -> list[tuple[list[Point], list[Point]]]:
        """Find mergable neighbour points between multipolygons.
        TODO The same problem as in alg _good1 and _good2.
        """

        # Find overlapping multipolygons
        mergable_multipolygon_pairs: \
            list[tuple[MultiPolygon, MultiPolygon]] = []
        for i in range(len(self.get_children())-1):
            mp1 = self.get_children()[i]
            for j in range(i+1, len(self.get_children())):
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
