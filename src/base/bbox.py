#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations


class BBox:

    def __init__(self,
                 xmin: float = 0, xmax: float = 0,
                 ymin: float = 0, ymax: float = 0) -> None:
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.dx = xmax - xmin
        self.dy = ymax - ymin

    def __add__(self, other: BBox) -> BBox:
        return BBox(
            xmin=min(self.xmin, other.xmin),
            xmax=max(self.xmax, other.xmax),
            ymin=min(self.ymin, other.ymin),
            ymax=max(self.ymax, other.ymax)
        )

    def __str__(self) -> str:
        return f'BBox(xmin={self.xmin}, xmax={self.xmax}, ' \
                    f'ymin={self.ymin}, ymax={self.ymax})'
