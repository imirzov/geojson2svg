#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Create maps and combined maps from geojsons
good0 - 11s - THE BEST, BUT OLD CODE (take updates from newer modules)
good1 - too slow, can not process cities
good2 - too slow, can not process cities
good3 - too slow, can not process cities
good4 - 47s, broken cities and city parts
.     - 29 s, broken cities and city parts
"""

import pandas as pd
import geopandas as gpd

import settings
from tools.geojson.geojson2svg.geojson2svg_good4 import MapObj
from tools.geojson.geojson2svg.lands \
    import Districts, PrahaObvody, DistrictsWithPrague


def dictricts_with_prague() -> None:
    """Merge districts with Prague."""

    fpath = settings.files / Districts.input_name
    gdf = gpd.read_file(fpath)  # type: ignore
    gdf = gdf.to_crs('epsg:4326')

    fpath = settings.files / PrahaObvody.input_name
    gdf2 = gpd.read_file(fpath)  # type: ignore
    gdf2 = gdf2.to_crs('epsg:4326')

    j = pd.concat([gdf2, gdf], ignore_index=True)

    s = j.to_json(to_wgs84=True)  # type: ignore
    fpath = settings.files / DistrictsWithPrague.input_name
    with open(fpath, 'w') as f:
        f.writelines(s)

    mo = MapObj(DistrictsWithPrague)
    mo.run()


def main() -> None:
    # MapObj(Regions).run()
    # MapObj(Districts).run()
    # MapObj(PrahaObvody).run()
    # dictricts_with_prague()
    # MapObj(Cities).run()
    # MapObj(CityParts).run()
    # MapObj(PrahaCasti).run()
    # MapObj(PrahaUzemi).run()
    pass
