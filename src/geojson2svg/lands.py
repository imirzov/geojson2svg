#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Land:
    input_name = ''
    output_name = ''
    w = 2000
    h = 1155
    id = 'kod'
    name = 'nazev'
    parent = None


class State(Land):
    url = 'https://hub.arcgis.com/datasets/' \
        + '92ee7c45a4f64262bac5217da8061233_0/explore'
    input_name = 'ArcČR_Stat.geojson'
    output_name = '0.state.geojson'


class Region(Land):
    url = 'https://hub.arcgis.com/datasets/' \
        + '77e01a68c02c43009020014020b925bf_0/explore'
    input_name = 'ArcČR_Kraj.geojson'
    output_name = '1.regions.geojson'


class Regions(Land):
    input_name = '1.regions.geojson'
    output_name = '1.regions_.geojson'


class District(Land):
    url = 'https://hub.arcgis.com/datasets/' \
        + '660bf23e44704b77a77f5a769a81fcd9_0/explore'
    input_name = 'ArcČR_Okres.geojson'
    output_name = '2.districts.geojson'
    parent = 'vusc'


class Districts(Land):
    input_name = '2.districts.geojson'
    output_name = '2.districts_.geojson'
    parent = 'vusc'


class DistrictsWithPrague(Land):
    input_name = '2.districts_with_prague.geojson'
    output_name = '2.districts_with_prague_.geojson'


class City(Land):
    url = 'https://hub.arcgis.com/datasets/' \
        + '20ab475cd72d483a83b1a94fd88c57a0_0/explore'  # NOTE URL 404
    input_name = 'ArcČR_Obec.geojson'
    output_name = '3.cities.geojson'
    parent = 'okres'


class Cities(Land):
    input_name = '3.cities.geojson'
    output_name = '3.cities_.geojson'
    parent = 'okres'


class CityPart(Land):
    url = 'https://hub.arcgis.com/datasets/' \
        + 'b62364eee2f74f41af32e1930f3048c0_0/explore'
    input_name = 'ArcČR_Městská_část.geojson'
    output_name = '4.city_parts.geojson'
    parent = 'obec'


class CityParts(Land):
    input_name = '4.city_parts.geojson'
    output_name = '4.city_parts_.geojson'
    parent = 'obec'


class Prague(Land):
    w = 2000
    h = 1522


class PrahaObvody(Prague):
    input_name = '5.praha_obvody.geojson'
    output_name = '5.praha_obvody_.geojson'


class PrahaCasti(Prague):
    input_name = '6.praha_casti.geojson'
    output_name = '6.praha_casti_.geojson'
    name = 'NAZEV_MC'


class PrahaUzemi(Prague):
    input_name = '7.praha_uzemi.geojson'
    output_name = '7.praha_uzemi_.geojson'
    name = 'NAZ_KU_P'
