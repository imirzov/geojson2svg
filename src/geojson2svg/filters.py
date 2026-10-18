#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Point filters."""

from abc import ABC

from geojson2svg.common import Point


class Filter(ABC):
    """Abstract base class for point filters."""

    def __init__(self, points: list[Point]) -> None:
        """Initialize the filter."""
        super().__init__()
        self.points = points


class Smooth(Filter):
    """Averages each point with its neighbors."""

    def apply(self) -> None:
        for i in range(len(self.points) - 2):
            pt0 = self.points[i]
            pt1 = self.points[i + 1]
            pt2 = self.points[i + 2]
            pt1.x = (pt0.x + pt2.x) / 2
            pt1.y = (pt0.y + pt2.y) / 2


class Round(Filter):
    """Rounds each point's coordinates according to the given precision."""

    def apply(self, precision: int) -> None:
        for pt in self.points:
            pt.round(precision)


class RemoveNeedles(Filter):
    """Removes points that form sharp angles (needles)."""

    # def apply(self, angle_threshold: float) -> None:
    #     for mp in self.get_children():
    #         for pg in mp.get_children():
    #             point_ids_to_remove: set[int] = set()
    #             points = pg.get_children()
    #             for i in range(len(points) - 3):
    #                 pt0 = points[i]
    #                 pt1 = points[i + 1]
    #                 pt2 = points[i + 2]
    #                 if pt0.x == pt2.x and pt0.y == pt2.y:
    #                     point_ids_to_remove.add(pt1.id_)
    #             for id_ in point_ids_to_remove:
    #                 pg.remove_point(id_)

    pass
