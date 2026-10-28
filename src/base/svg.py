#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from string import Template
import settings

from base.mapobj import MapObj

pad = ' ' * 4


class Svg:
    svg_code: str = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'viewBox="0 0 $w $h">\n'
        '$style\n'
        '$paths\n'
        '</svg>'
    )
    style: str = (
        pad + '<style>\n' +
        pad * 2 + 'path {fill: black; stroke: white; '
                  'stroke-width: 0.2px}\n' +
        pad + '</style>\n'
    )

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
    #           'stroke-width: 0.5px}\n'

    def __init__(self, map_obj: MapObj) -> None:
        self.map_obj = map_obj
        self.w = map_obj.klass.w
        self.h = map_obj.klass.h
        self.fpath = map_obj.svg_fpath
        self.t = Template(self.svg_code)

    def run(self, show_ids: bool = False) -> None:
        """Create paths and place them into SVG code."""
        svg_paths: list[str] = []
        for mp in self.map_obj.get_children():
            coords = ''
            for polygon in mp.get_children():
                coords += 'M'  # NOTE use small letter for dx,dy
                for pt in polygon.get_children():
                    # coords += ' {:.3f},{:.3f}'.format(dx, dy) # for dx,dy
                    coords += f' {pt.x} {pt.y}'
                    if show_ids:
                        svg_paths.append(
                            '<text x="{}" y="{}">{}</text>\n'
                            .format(pt.x + 10 * polygon.id_,
                                    pt.y - 10 * polygon.id_, pt.id_))
                coords += ' Z'  # NOTE use small letter for dx,dy
            svg_paths.append('{}<path d="{}" id="{}" />\n'
                             .format(pad, coords, mp.path_id))
        # for pt in BORDER_UTMOST_POINTS:
        #     svg_paths.append(f'{pad}<circle cx="{pt.x}" cy="{pt.y}" '
        #                      'r="0.5" style="fill:black;" />\n')
        # for id_ in DISORDERED_POINTS:
        #     pt = POINTS[id_]
        #     svg_paths.append(f'{pad}<circle cx="{pt.x}" cy="{pt.y}" '
        #                      'r="0.5" style="fill:red;" />\n')
        paths = ''.join(svg_paths)
        svg_code = self.t.substitute(w=self.w, h=self.h,
                                     paths=paths, style=self.style)
        with open(self.fpath, 'w', encoding=settings.encoding) as f:
            f.writelines(svg_code)
