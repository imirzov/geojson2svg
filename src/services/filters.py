#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Point filters: perform various operations on points."""

from abc import ABC

from base.point import Point
from base.polygon import Polygon
from services.log import r


class Filter(ABC):
    """Abstract base class for point filters."""

    def __init__(self, points: list[Point]) -> None:
        """Initialize the filter."""
        super().__init__()
        self.points = points


class RemoveNeedles(Filter):
    """Needle is 3 points where first and third have the same
    coordinates. So 2nd and 3rd point have to be removed."""

    def apply(self) -> None:
        points_to_remove: set[Point] = set()
        for i in range(len(self.points) - 3):
            pt0 = self.points[i]
            pt1 = self.points[i + 1]
            pt2 = self.points[i + 2]
            if pt0.x == pt2.x and pt0.y == pt2.y:
                points_to_remove.add(pt1)
                points_to_remove.add(pt2)
        for pt in points_to_remove:
            pg: Polygon = pt.parent
            pg.remove_point(pt.id_)


class RemoveSamePoints(Filter):
    """Filter out points with the same coordinates."""

    def apply(self) -> None:
        filtered_points: list[Point] = []
        for pt1 in self.points:
            unique = True
            for pt2 in filtered_points:
                if pt1.x == pt2.x and pt1.y == pt2.y:
                    unique = False
                    pg: Polygon | None = pt1.parent
                    if pg is None:
                        r.warning(f'Point {pt1.id_} has no parent polygon.')
                    else:
                        pg.remove_point(pt1.id_)
            if unique:
                filtered_points.append(pt1)
        r.debug('Before filtering: {}, after: {}'
                .format(len(self.points), len(filtered_points)))


class Round(Filter):
    """Rounds each point's coordinates according to the given precision."""

    def apply(self, precision: int) -> None:
        for pt in self.points:
            pt.round(precision)


class Smooth(Filter):
    """Averages each point with its 2 neighbors."""

    def apply(self) -> None:
        for i in range(len(self.points) - 2):
            pt0 = self.points[i]
            pt1 = self.points[i + 1]
            pt2 = self.points[i + 2]
            pt1.x = (pt0.x + pt2.x) / 2
            pt1.y = (pt0.y + pt2.y) / 2
