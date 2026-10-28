#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Definitions of various land-related classes and test cases."""

from pathlib import Path

from settings import files


state = files / 'state'
regions = files / 'regions'
districts = files / 'districts'
districts_with_prague = districts / 'districts_with_prague'
cities = files / 'cities'
city_parts = cities / 'city_parts'
praha = cities / 'praha'
tests = files / 'tests'


class Land:
    fpath = Path('')
    w = 2000
    h = 1155
    id = 'kod'
    name = 'name'
    parent = None


class State1(Land):
    fpath = state / '1.geojson'


class Region1(Land):
    fpath = regions / '1.geojson'


class Region2(Land):
    fpath = regions / '2.geojson'


class Region2_(Land):
    fpath = regions / '2_.geojson'


class Region3(Land):
    fpath = regions / '3.geojson'


class Region4(Land):
    fpath = regions / '4.geojson'


class Jihocesky(Land):
    fpath = regions / 'jihocesky.geojson'


class Jihomoravsky(Land):
    fpath = regions / 'jihomoravsky.geojson'


class Karlovarsky(Land):
    fpath = regions / 'karlovarsky.geojson'


class Kralovehradecky(Land):
    fpath = regions / 'kralovehradecky.geojson'


class Liberecky(Land):
    fpath = regions / 'liberecky.geojson'


class Moravskoslezsky(Land):
    fpath = regions / 'moravskoslezsky.geojson'


class Olomoucky(Land):
    fpath = regions / 'olomoucky.geojson'


class Pardubicky(Land):
    fpath = regions / 'pardubicky.geojson'


class Plzensky(Land):
    fpath = regions / 'plzensky.geojson'


class Praha(Land):
    fpath = regions / 'praha.geojson'


class Stredocesky(Land):
    fpath = regions / 'stredocesky.geojson'


class Ustecky(Land):
    fpath = regions / 'ustecky.geojson'


class Vysocina(Land):
    fpath = regions / 'vysocina.geojson'


class Zlinsky(Land):
    fpath = regions / 'zlinsky.geojson'


class District1(Land):
    fpath = districts / '1.geojson'
    parent = 'vusc'


class District2(Land):
    fpath = districts / '2.json'
    parent = 'vusc'


class District3(Land):
    fpath = districts / '3.geojson'
    parent = 'vusc'


class District4(Land):
    fpath = districts / '4.geojson'
    parent = 'vusc'


class DistrictPrague1(Land):
    fpath = districts_with_prague / '1.geojson'


class DistrictPrague2(Land):
    fpath = districts_with_prague / '2.geojson'


class DistrictPrague2_(Land):
    fpath = districts_with_prague / '2_.geojson'


class DistrictPrague3(Land):
    fpath = districts_with_prague / '3.geojson'


class City1(Land):
    fpath = cities / '1.geojson'
    parent = 'okres'


class City2(Land):
    fpath = cities / '2.geojson'
    parent = 'okres'


class City3(Land):
    fpath = cities / '3.geojson'
    parent = 'okres'


class City4(Land):
    fpath = cities / '4.geojson'
    parent = 'okres'


class City5(Land):
    fpath = cities / '5.geojson'
    parent = 'okres'


class CityParts1(Land):
    fpath = city_parts / '1.geojson'
    parent = 'obec'


class CityParts2(Land):
    fpath = city_parts / '2.geojson'
    parent = 'obec'


class Prague(Land):
    w = 2000
    h = 1522


class PrahaObvody(Prague):
    fpath = praha / '5.praha_obvody.geojson'


class PrahaObvody_(Prague):
    fpath = praha / '5.praha_obvody_.geojson'


class PrahaCasti(Prague):
    fpath = praha / '6.praha_casti.geojson'
    name = 'NAZEV_MC'


class PrahaUzemi(Prague):
    fpath = praha / '7.praha_uzemi.geojson'
    name = 'NAZ_KU_P'


class Test1(Land):
    fpath = tests / '1.geojson'
    w = 1000
    h = 1000


class Test2(Land):
    fpath = tests / '2.geojson'
    w = 1000
    h = 1000


class Test3(Land):
    fpath = tests / '3.geojson'
    w = 1000
    h = 1000


class Test4(Land):
    fpath = files / 'tests' / '4.geojson'
    w = 1000
    h = 1000
