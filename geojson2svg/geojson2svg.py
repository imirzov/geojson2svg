#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg import common
from geojson2svg.utils import recursive_quad_merge

PRECISION: int = 1  # px


class MapObj(common.MapObj):

    def run(self) -> None:
        self.convert_coords_to_px()
        self.round_point_coordinates(1)
        recursive_quad_merge(self.get_points(), PRECISION * 2)
        self.remove_close_points(PRECISION)
        self.count_points()
        self.generate_svg_code()
