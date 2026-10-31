#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from string import Template
import settings

from model.mapobj import MapObj

pad = ' ' * 4


class Svg:
    svg_code: str = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'viewBox="$viewbox">\n'
        '<style>\n'
        '$style'
        '</style>\n'
        '$features'
        '</svg>'
    )

    """
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

    # for pt in BORDER_UTMOST_POINTS:
    #     svg_paths.append(f'{pad}<circle cx="{pt.x}" cy="{pt.y}" '
    #                      'r="0.5" style="fill:black;" />\n')
    # for id_ in DISORDERED_POINTS:
    #     pt = POINTS[id_]
    #     svg_paths.append(f'{pad}<circle cx="{pt.x}" cy="{pt.y}" '
    #                      'r="0.5" style="fill:red;" />\n')
    """

    def __init__(self, mo: MapObj) -> None:
        self.mo = mo
        self.w = mo.klass.w
        self.h = mo.klass.h
        self.fpath = mo.svg_fpath
        self.t = Template(self.svg_code)

    def run(self, show_ids: bool = False) -> None:
        """
        svg_paths: list[str] = []
        for feature in self.mo.get_children():
            coords = ''
            for ch in feature.get_children():
                coords += 'M'  # NOTE use small letter for dx,dy
                for pt in ch.get_points():
                    # coords += f' {dx:.3f},{dy:.3f}'  # NOTE for dx,dy
                    coords += f' {pt.x} {pt.y}'

                    if show_ids:
                        svg_paths.append(
                            '<text x="{}" y="{}">{}</text>\n'
                            .format(pt.x + 10 * polygon.id_,
                                    pt.y - 10 * polygon.id_, pt.id_))

                coords += ' Z'  # NOTE use small letter for dx,dy
            path_id = feature.properties.get('name', '')
            svg_paths.append(f'{pad}<path d="{coords}" id="{path_id}" />\n')
        paths = ''.join(svg_paths)
        """

        features_code = ''
        features_style = ''
        for feature in self.mo.get_children():
            for ch in feature.get_children():
                features_code += ch.get_svg_code()
                style = ch.get_svg_style()
                if style not in features_style:
                    features_style += style
        svg_code = self.t.substitute(
            viewbox=self.mo.bbox.get_viewbox(),
            style=features_style, features=features_code)
        with open(self.fpath, 'w', encoding=settings.encoding) as f:
            f.writelines(svg_code)
