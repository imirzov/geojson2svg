#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Remove unneeded shit from a geojson file."""

import json
from typing import Any

import settings

REMOVE = {
    '1.regions.geojson': [
        'Australie',
        'Belgie',
        'Brazilie',
        'Bulharsko',
        'Cina',
        'Dansko',
        'Estonsko',
        'Finsko',
        'Francie',
        'Chorvatsko',
        'Indie',
        'Irsko',
        'Island',
        'Italie',
        'Izrael',
        'Japonsko',
        'Jizni_Afrika',
        'Kanada',
        'Korejska_rep',
        'Kypr',
        'Lichtenstejnsko',
        'Litva',
        'Lotyssko',
        'Lucembursko',
        'Madarsko',
        'Malta',
        'Mexiko',
        'Nemecko',
        'Nerezidenti',
        'Nizozemsko',
        'Norsko',
        'Novy_Zeland',
        'Oceanie',
        'Ostatni_africke_zeme',
        'Ostatni_americke_zeme',
        'Ostatni_asijske_zeme',
        'Ostatni_evropske_zeme',
        'Polsko',
        'Portugalsko',
        'Rakousko',
        'Rumunsko',
        'Rusko',
        'Recko',
        'Saudska_Arabie',
        'Slovensko',
        'Slovinsko',
        'Spojene_arabske_emiraty',
        'Spojene_staty',
        'Srbsko_a_Cerna_Hora',
        'Spanelsko',
        'Svedsko',
        'Svycarsko',
        'Tchaj_wan',
        'Turecko',
        'Ukrajina',
        'Velka_Britanie',
        'SHAPE_Length',
        'SHAPE_Area',
    ],
    '2.districts_with_prague.geojson': [
        'FID',
        'KOD_UZOHMP',
        'KOD_RUIAN',
        'PLATIOD',
        'NEPLATIPO',
        'doziti_zeny_2015',
        'doziti_zeny_2016',
        'doziti_zeny2017',
        'doziti_zeny_2018',
        'doziti_zeny_2019',
        'doziti_muzi_2015',
        'doziti_muzi_2016',
        'doziti_muzi_2017',
        'doziti_muzi_2018',
        'doziti_muzi_2019',
        'pocet_obyv',
        'SHAPE_Length',
        'SHAPE_Area',
    ],
    '5.praha_obvody.geojson': [
        'FID',
        'KOD_UZOHMP',
        'KOD_RUIAN',
        'PLATIOD',
        'NEPLATIPO'
    ]
}


def recursively_remove_keys(data: dict[str, Any] | list[Any],
                            keys_to_remove: list[str]) -> Any:
    if isinstance(data, dict):
        # Create a new dictionary without the key to remove
        return {
            key: recursively_remove_keys(value, keys_to_remove)
            for key, value in data.items()
            if key not in keys_to_remove
        }
    else:
        # Process each item in the list recursively
        return [recursively_remove_keys(item, keys_to_remove)
                for item in data]


def main() -> None:
    for fname, list_ in REMOVE.items():
        fpath = settings.files / fname
        d = json.loads(fpath.read_text(encoding=settings.encoding))
        d = recursively_remove_keys(d, list_)

        # print(json.dumps(d, ensure_ascii=False, indent=2))
        fpath2 = str(fpath)[:-8] + '_.geojson'
        with open(fpath2, 'w', encoding=settings.encoding) as f:
            json.dump(d, f, ensure_ascii=False)
