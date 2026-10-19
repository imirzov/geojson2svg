#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from geojson2svg.model.bbox import BBox
from geojson2svg.model.point import Point, merge_points_to
from settings import report as r


def get_bbox(points: list[Point]) -> BBox:
    """Calculate bounding box: min and max X and Y coordinates."""
    bbox = BBox(xmin=1e+9, xmax=-1e+9, ymin=1e+9, ymax=-1e+9)
    for pt in points:
        bbox.xmin = min(pt.x, bbox.xmin)
        bbox.xmax = max(pt.x, bbox.xmax)
        bbox.ymin = min(pt.y, bbox.ymin)
        bbox.ymax = max(pt.y, bbox.ymax)
    return bbox


def recursive_quad_merge(points: list[Point], precision: int) -> None:
    bbox = get_bbox(points)
    center_x = (bbox.xmax + bbox.xmin) / 2
    center_y = (bbox.ymax + bbox.ymin) / 2
    quater1: list[Point] = []
    quater2: list[Point] = []
    quater3: list[Point] = []
    quater4: list[Point] = []
    for pt in points:
        if pt.x > center_x and pt.y > center_y:
            quater1.append(pt)
        elif pt.x < center_x and pt.y > center_y:
            quater2.append(pt)
        elif pt.x < center_x and pt.y < center_y:
            quater3.append(pt)
        elif pt.x > center_x and pt.y < center_y:
            quater4.append(pt)

    for q in [quater1, quater2, quater3, quater4]:
        if len(q) >= 2:
            if bbox.dx > precision and bbox.dy > precision * 2:
                recursive_quad_merge(q, precision)
            else:
                for pt in q[1:]:
                    if not pt.merged:
                        pt.x = q[0].x
                        pt.y = q[0].y
                        pt.merged = True
                q[0].merged = True


def get_closest_point(pt: Point, points: list[Point]) -> Point:
    """Return the closest point to pt from the list of points."""
    return min(points, key=lambda p: (pt.x-p.x)**2 + (pt.y-p.y)**2)


def collapse_gap_1(point_line_1: list[Point],
                   point_line_2: list[Point]) -> None:
    """Move points
    to the coordinates of their nearest points in the other point line"""
    while set(point_line_1) != set(point_line_2):
        # Move each point in the first line to its nearest point in the second
        for pt in point_line_1:
            closest = get_closest_point(pt, point_line_2)
            pt.x = closest.x
            pt.y = closest.y
        # Do the same for the second line, using the updated first line
        for pt in point_line_2:
            closest = get_closest_point(pt, point_line_1)
            pt.x = closest.x
            pt.y = closest.y


def collapse_gap_2(points1: list[Point], points2: list[Point],
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
            merge_points_to(points_to_merge, pt1)

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
