#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Self

from base import get_nested_list_depth
from base.bbox import BBox


class Obj(ABC):
    COORDINATES_LIST_DEPTH = 0

    def __init__(self, coordinates: Any) -> None:
        super().__init__()
        self.id_ = 0
        self.coordinates = coordinates
        self.children: list[Any] = list()
        self.bbox = BBox()

    def set_bbox(self) -> None:
        for pt in self.get_points():
            self.bbox += pt.bbox

    @abstractmethod
    def get_children(self) -> list[Any]:
        ...

    @abstractmethod
    def get_points(self) -> list[Any]:
        ...

    def remove_point(self, id_: int) -> None:
        assert id_ in self.children
        self.children.remove(id_)

    def check_coords(self) -> bool:
        return get_nested_list_depth(self.coordinates) \
            == self.COORDINATES_LIST_DEPTH

    def is_overlapping_with(self, obj: Self) -> bool:

        def f(obj1: Obj, obj2: Obj) -> bool:
            # Conditions:
            c1 = False
            c2 = False

            if obj1.bbox.xmin <= obj2.bbox.xmin \
                    and obj2.bbox.xmin <= obj1.bbox.xmax:
                c1 = True
            if obj1.bbox.xmin <= obj2.bbox.xmax \
                    and obj2.bbox.xmax <= obj1.bbox.xmax:
                c1 = True

            if obj1.bbox.ymin <= obj2.bbox.ymin \
                    and obj2.bbox.ymin <= obj1.bbox.ymax:
                c2 = True
            if obj1.bbox.ymin <= obj2.bbox.ymax \
                    and obj2.bbox.ymax <= obj1.bbox.ymax:
                c2 = True

            if c1 and c2:
                return True
            return False

        return f(self, obj) or f(obj, self)

    # def convert_coords_to_px(self) -> None:
    #     """Convert latitude and longitude GeoJson coords
    #     to Land's width (w) and height (h) in pixels.
    #     """
    #     for ch in self.get_children():
    #         ch.convert_coords_to_px()

    @abstractmethod
    def get_svg_code(self) -> str:
        """Return the SVG code for this object."""
        ...

    @abstractmethod
    def get_svg_style(self) -> str:
        """Return the SVG style for this object."""
        ...
