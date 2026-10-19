#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Self

from geojson2svg.model.bbox import BBox


class Obj(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.id_ = 0
        self.children: list[int | str] = list()
        self.bbox = BBox()

    def set_bbox(self) -> None:
        for ch in self.get_children():
            self.bbox += ch.bbox

    @abstractmethod
    def get_children(self) -> list[Any]:
        ...

    @abstractmethod
    def get_points(self) -> list[Any]:
        ...

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
