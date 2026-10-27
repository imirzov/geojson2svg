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


from base.lands import State1
from core import Good1 as MapObj
from services.log import initialize_logging


"""
import pandas as pd
import geopandas as gpd
import settings
def dictricts_with_prague() -> None:
    # Merge districts with Prague.

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
"""


if __name__ == '__main__':
    initialize_logging()
    MapObj(State1).run()
    # MapObj(Districts).run()
    # MapObj(PrahaObvody).run()
    # dictricts_with_prague()
    # MapObj(Cities).run()
    # MapObj(CityParts).run()
    # MapObj(PrahaCasti).run()
    # MapObj(PrahaUzemi).run()
    pass
