#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg import common
from geojson2svg.common import Point, get_bbox

PRECISION: int = 1  # px


def recursive_quad_merge(points: list[Point]) -> None:
    xmin, xmax, ymin, ymax = get_bbox(points)
    center_x = (xmax + xmin) / 2
    center_y = (ymax + ymin) / 2
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
            if (xmax - xmin) > PRECISION * 2 and (ymax - ymin) > PRECISION * 2:
                recursive_quad_merge(q)
            else:
                for pt in q[1:]:
                    if not pt.merged:
                        pt.x = q[0].x
                        pt.y = q[0].y
                        pt.merged = True
                q[0].merged = True


class MapObj(common.MapObj):

    def run(self) -> None:
        self.convert_coords_to_px()
        self.round_point_coordinates(1)
        recursive_quad_merge(self.get_points())
        self.remove_close_points(PRECISION)
        self.count_points()
        self.generate_svg_code()

    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for mp in self.get_children():
            for pg in mp.get_children():
                points.extend(pg.get_children())
        return points
