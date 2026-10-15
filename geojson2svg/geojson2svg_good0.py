#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg import common


class MapObj(common.MapObj):

    def run(self) -> None:
        self.convert_coords_to_px()
        self.round_point_coordinates(1)
        self.remove_needles()
        self.count_points()
        self.generate_svg_code()
