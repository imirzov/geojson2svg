#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from geojson2svg.common import MapObj


class Good4(MapObj):

    PRECISION: int = 3  # px

    def run(self) -> None:
        """NOTE For performance
        remove duplicated points before the border collapse!
        """
        self.convert_coords_to_px()
        self.round_point_coordinates(self.PRECISION)
        self.filter_points_with_same_coords()
        self.generate_svg_code()
