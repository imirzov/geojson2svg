#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tools.geojson.geojson2svg import common

PRECISION: int = 2  # px


class MapObj(common.MapObj):

    def run(self) -> None:
        self.convert_coords_to_px()
        self.round_point_coordinates(1)
        self.remove_needles()
        self.count_points()
        self.generate_svg_code()
