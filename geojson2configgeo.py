#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate config/geo.json from geojson maps."""

import json
from typing import Any, Union

import settings
from settings import report as r
from tools.geojson.geojson2svg.lands import (Region, District,
                                             City, CityPart)

GeoItem = Union[type[Region], type[District], type[City], type[CityPart]]


class Feature:

    def __init__(self, id_: int, name: str, parent: int | None) -> None:
        self.id_ = int(id_)
        self.name = name
        if parent is None:
            parent = -1
        self.parent = int(parent)

    def __str__(self) -> str:
        return f'{self.id_} {self.name} {self.parent}'


def extract_features(klass: GeoItem) -> list[Feature]:
    features: list[Feature] = []
    fpath = settings.files / klass.output_name
    with open(fpath, 'r', encoding=settings.encoding) as f:
        geojson = json.load(f)
    for feature in geojson['features']:
        p = feature['properties']
        parent = None
        if klass.parent in p:
            parent = p[klass.parent]
        f = Feature(p[klass.id], p[klass.name], parent)
        features.append(f)
    r.info(len(features))
    return features


def get_parent_by_id(features: list[Feature], parent_id: int) \
        -> Feature | None:
    for f in features:
        if f.id_ == parent_id:
            return f
    r.error(parent_id)


def main() -> None:
    config_geo_json: dict[str, Any] = dict()
    region_features = extract_features(Region)
    district_features = extract_features(District)
    city_features = extract_features(City)
    city_part_features = extract_features(CityPart)
    for f1 in region_features:
        config_geo_json[f1.name] = dict()

    for f2 in district_features:
        f1 = get_parent_by_id(region_features, f2.parent)
        if f1 is None:
            continue
        config_geo_json[f1.name][f2.name] = dict()

    for f3 in city_features:
        f2 = get_parent_by_id(district_features, f3.parent)
        if f2 is None:
            continue
        f1 = get_parent_by_id(region_features, f2.parent)
        if f1 is None:
            continue
        config_geo_json[f1.name][f2.name][f3.name] = []

    for f4 in city_part_features:
        f3 = get_parent_by_id(city_features, f4.parent)
        if f3 is None:
            continue
        f2 = get_parent_by_id(district_features, f3.parent)
        if f2 is None:
            continue
        f1 = get_parent_by_id(region_features, f2.parent)
        if f1 is None:
            continue

        # Brno-Jundrov -> Jundrov etc.
        exclude = ['Brno-střed', 'Brno-jih', 'Brno-sever']
        city_part_name: str = f4.name
        if city_part_name not in exclude:
            if city_part_name.startswith(f3.name + '-'):
                city_part_name = city_part_name[len(f3.name) + 1:]
        config_geo_json[f1.name][f2.name][f3.name].append(city_part_name)

    # Sort everything
    # level 1 - regions
    config_geo_json = dict(sorted(config_geo_json.items()))
    for k2, v2 in config_geo_json.items():
        # level 2 - districts
        config_geo_json[k2] = dict(sorted(v2.items()))
        for k3, v3 in config_geo_json[k2].items():
            # level 3 - cities
            config_geo_json[k2][k3] = dict(sorted(v3.items()))
            for k4, v4 in config_geo_json[k2][k3].items():
                # level 4 - city parts
                config_geo_json[k2][k3][k4] = sorted(v4)

    # Convert district from dict to list
    for f1 in region_features:
        d1 = config_geo_json[f1.name]
        for f2 in district_features:
            if f2.name in d1:
                d = config_geo_json[f1.name][f2.name]
                loc: list[Union[str, dict[str, list[str]]]] = []
                for city, city_parts_list in d.items():
                    if not city_parts_list:
                        loc.append(city)
                    else:
                        loc.append(dict({city: city_parts_list}))
                config_geo_json[f1.name][f2.name] = loc

    fpath = settings.logs / settings.geo
    with open(fpath, 'w', encoding=settings.encoding) as f:
        json.dump(config_geo_json, f, ensure_ascii=False, indent=4)
