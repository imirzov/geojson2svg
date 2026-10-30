#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Point transformers: perform various operations on points."""

from abc import ABC

from model.mapobj import MapObj


class Transform(ABC):
    """Abstract base class for point transformers."""

    def __init__(self, mo: MapObj) -> None:
        """Initialize the transformer."""
        super().__init__()
        self.mo = mo
        self.points = mo.get_points()


class Round(Transform):
    """Rounds each point's coordinates according to the given precision."""

    def apply(self, precision: int) -> None:
        for pt in self.points:
            pt.round(precision)


class Smooth(Transform):
    """Averages each point with its 2 neighbors."""

    def apply(self) -> None:
        for i in range(len(self.points) - 2):
            pt0 = self.points[i]
            pt1 = self.points[i + 1]
            pt2 = self.points[i + 2]
            pt1.x = (pt0.x + pt2.x) / 2
            pt1.y = (pt0.y + pt2.y) / 2


class Coords2Px(Transform):
    """Converts coordinates to pixel values based on a given scale."""

    def __init__(self, mo: MapObj) -> None:
        super().__init__(mo)
        self.bbox = mo.bbox
        assert self.bbox.dx
        assert self.bbox.dy
        self.w = mo.klass.w
        self.h = mo.klass.h

    def apply(self) -> None:
        """Convert latitude and longitude GeoJson coords
        to Land's width (w) and height (h) in pixels.
        """
        for pt in self.mo.get_points():
            pt.x = (pt.x - self.bbox.xmin) / self.bbox.dx * self.w
            pt.y = (self.bbox.ymax - pt.y) / self.bbox.dy * self.h
