#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import os
from typing import Self, override
import unidecode

from base.lands import Land
from base.obj import Obj
from base.point import POINTS, Point
from base.multipolygon \
    import MULTIPOLYGONS, MultiPolygon, create_multipolygon
import settings
from settings import report as r

PARENTS: dict[int, str] = dict()  # id_: name


class MapObj(Obj):
    """Parent of MultiPolygon, consists of multiple MultiPolygon objects."""

    def __init__(self, klass: type[Land]) -> None:
        super().__init__()
        os.chdir(os.path.dirname(__file__))
        self.klass = klass
        self.svg_fpath = os.path.join(
            settings.files,
            os.path.splitext(self.klass.output_name)[0] + '.svg')
        self.read_children()
        self.set_bbox()
        r.info(str(self))

    def __str__(self) -> str:
        input_name = unidecode.unidecode(self.klass.input_name)
        return f'{input_name}\n' \
            + f'{self.klass.w}x{self.klass.h}\n' \
            + f'{self.bbox}\n' \
            + f'{len(self.children)} paths\n' \
            + f'{len(POINTS)} points before\n'

    def read_children(self) -> None:
        """Read polygon coordinates:
        {
            id1: [(x11, y11), (x12, y12), ...],
            id2: [(x21, y21), (x22, y22), ...],
            ...
        }
        """
        fpath = settings.files / self.klass.input_name
        if not fpath.exists():
            r.error(f'File not found: {fpath}')
            raise SystemExit

        with open(fpath, 'r', encoding=settings.encoding) as f:
            geojson = json.load(f)
        for feature in geojson['features']:
            p = feature['properties']
            path_id = p[self.klass.name]
            if self.klass.parent is not None:
                if self.klass.parent in p and self.klass.id in p:
                    if p[self.klass.parent] in PARENTS:
                        path_id = PARENTS[p[self.klass.parent]] + '_' + path_id
                    PARENTS[p[self.klass.id]] = path_id
            else:
                if self.klass.id in p:
                    PARENTS[p[self.klass.id]] = p[self.klass.name]
            path_id = settings.to_en(path_id)

            if feature['geometry']['type'] == 'MultiPolygon':
                coordinates = feature['geometry']['coordinates']
            else:
                coordinates = [feature['geometry']['coordinates']]
            mp = create_multipolygon(path_id, coordinates)
            self.children.append(mp.path_id)

    @override
    def get_children(self) -> list[MultiPolygon]:
        return list([MULTIPOLYGONS[id_] for id_ in self.children])

    @override
    def get_points(self) -> list[Point]:
        points: list[Point] = []
        for mp in self.get_children():
            points.extend(mp.get_points())
        return points

    def convert_coords_to_px(self) -> None:
        """Convert latitude and longitude GeoJson coords
        to Land's width (w) and height (h) in pixels.
        """
        for mp in self.get_children():
            for pg in mp.get_children():
                pg.convert_coords_to_px(self.bbox, self.klass.w, self.klass.h)

    def remove_needles(self) -> None:
        for mp in self.get_children():
            for pg in mp.get_children():
                point_ids_to_remove: set[int] = set()
                points = pg.get_children()
                for i in range(len(points) - 3):
                    pt0 = points[i]
                    pt1 = points[i + 1]
                    pt2 = points[i + 2]
                    if pt0.x == pt2.x and pt0.y == pt2.y:
                        point_ids_to_remove.add(pt1.id_)
                for id_ in point_ids_to_remove:
                    pg.remove_point(id_)

    def remove_close_points(self, precision: int) -> None:
        """Remove close points (within precision)."""
        for mp in self.get_children():
            for pg in mp.get_children():
                prev_pt = None
                for pt in pg.get_children():
                    if prev_pt is not None:
                        if pt.close_to(prev_pt, precision):
                            pg.remove_point(pt.id_)
                            continue
                    prev_pt = pt

    def filter_points_with_same_coords(self) -> None:
        for mp in self.get_children():
            for pg in mp.get_children():
                points = pg.get_children()
                points = filter_points_with_same_coords(points)
                coords = [(pt.x, pt.y) for pt in points]
                pg.set_children(coords)

    def count_points(self) -> None:
        counter = 0
        for mp in self.get_children():
            for pg in mp.get_children():
                counter += len(pg.get_children())
        r.info('{} points after.\n'.format(counter))

    def __add__(self, map_obj: Self) -> Self:
        s1: str = os.path.splitext(self.svg_fpath)[0]
        s2: str = os.path.basename(
            os.path.splitext(map_obj.klass.output_name)[0])
        self.svg_fpath = s1 + '_' + s2 + '.svg'

        self.children.extend(map_obj.children)
        return self

    def generate_svg_code(self, show_ids: bool = False) -> None:
        """Create paths and place them into SVG code."""
        pad = ' ' * 4
        svg_paths: list[str] = []
        for mp in self.get_children():
            coords = ''
            for pg in mp.get_children():
                coords += 'M'  # NOTE use small letter for dx,dy
                for pt in pg.get_children():
                    # coords += ' {:.3f},{:.3f}'.format(dx, dy) # for dx,dy
                    coords += f' {pt.x} {pt.y}'
                    if show_ids:
                        svg_paths.append('<text x="{}" y="{}">{}</text>\n'
                                         .format(pt.x + 10 * pg.id_,
                                                 pt.y - 10 * pg.id_, pt.id_))
                coords += ' Z'  # NOTE use small letter for dx,dy
            svg_paths.append(f'{pad}<path d="{coords}" id="{mp.path_id}" />\n')
        # for pt in BORDER_UTMOST_POINTS:
        #     svg_paths.append(f'{pad}<circle cx="{pt.x}" cy="{pt.y}" '
        #                      'r="0.5" style="fill:black;" />\n')
        # for id_ in DISORDERED_POINTS:
        #     pt = POINTS[id_]
        #     r.debug(f'[{pt.x}, {pt.y}]')
        #     svg_paths.append(f'{pad}<circle cx="{pt.x}" cy="{pt.y}" '
        #                      'r="0.5" style="fill:red;" />\n')
        # TODO remove CSS
        svg_code: list[str] = [
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n',
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {self.klass.w} {self.klass.h}">\n',
            # pad + '<style>\n',
            # pad * 2 + 'path {fill: black; stroke: white; '
            #           'stroke-width: 0.2px}\n',
            # pad * 2 + 'path#plzensky-kraj {fill: transparent; '
            #           'stroke: black; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#karlovarsky-kraj {fill: transparent; '
            #           'stroke: red; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#pardubicky-kraj {fill: transparent; '
            #           'stroke: black; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#kralovehradecky-kraj {fill: transparent; '
            #           'stroke: red; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#stredocesky-kraj {fill: transparent; '
            #           'stroke: black; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#jihocesky-kraj {fill: transparent; '
            #           'stroke: red; stroke-width: 0.5px}\n',
            # pad * 2 + 'path#ustecky-kraj {fill: transparent; stroke: blue; '
            #           'stroke-width: 0.5px}\n',
            # pad + '</style>\n',
            *svg_paths,
            '</svg>',
        ]
        with open(self.svg_fpath, 'w', encoding=settings.encoding) as f:
            f.writelines(svg_code)


def filter_points_with_same_coords(points: list[Point]) -> list[Point]:
    filtered_points: list[Point] = []
    for pt1 in points:
        unique = True
        for pt2 in filtered_points:
            if pt1.x == pt2.x and pt1.y == pt2.y:
                unique = False
                pg = pt1.parent
                if pg is None:
                    r.warning(f'Point {pt1.id_} has no parent polygon.')
                else:
                    pg.remove_point(pt1.id_)
        if unique:
            filtered_points.append(pt1)
    r.debug('Before filtering: {}, after: {}'
            .format(len(points), len(filtered_points)))
    return filtered_points
