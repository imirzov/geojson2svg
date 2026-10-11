#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""© Ihor Mirzov, 2021.
Global application's settings and case settings.
Each case corresponds to a separate geo location:
region, district - ('stredocesky-kraj', 'mlada-boleslav')
"""

import os
import re
import json
import logging
import datetime
import unidecode
import enum
from pathlib import Path

SRC_DIR = Path(__file__).parent
os.environ['PYTHONPATH'] = str(SRC_DIR)

# Server role: development or production
_environment = os.environ.get('APP_ENV', 'development').strip().lower()
if _environment not in {'development', 'production'}:
    raise ValueError(
        "APP_ENV must be either 'development' or 'production'.")
is_production = _environment == 'production'

files = Path(SRC_DIR / '..' / 'files').resolve()
backups = Path(SRC_DIR / '..' / 'backups').resolve()
cache = Path(SRC_DIR / '..' / 'cache').resolve()
config = Path(SRC_DIR / '..' / 'config').resolve()
data = Path(SRC_DIR / '..' / 'data').resolve()
img = Path(SRC_DIR / '..' / 'img').resolve()
lists = Path(SRC_DIR / '..' / 'lists').resolve()
logs = Path(SRC_DIR / '..' / 'logs').resolve()
maps = Path(SRC_DIR / '..' / 'maps').resolve()
src = Path(SRC_DIR / '..' / 'src').resolve()
stats = Path(SRC_DIR / '..' / 'stats').resolve()
temp = Path(SRC_DIR / '..' / 'temp').resolve()
tests = Path(SRC_DIR / '..' / 'tests').resolve()
www = Path(SRC_DIR / '..' / 'www').resolve()

for d in [backups, cache, data, img, lists,
          logs, maps, stats, tests, temp, www]:
    if not d.exists():
        d.mkdir(parents=True, exist_ok=True)


def time_now() -> str:
    """Last update time for HTML pages.
    2023-12-17 17:34:42
    """
    return str(datetime.datetime.now())[:19]


class Period(enum.Enum):
    """
    Archive apartments older than 30 days
    Remove easy cache files each 90 minutes (1.5 hours)
    Remove deep cache files each 30 days
    """
    timeout = 1  # timeout for requests in seconds
    request = 3  # request period in seconds
    minute = 60
    hour = 3600
    day = hour * 25
    week = day * 7
    month = day * 31
    year = day * 366

    easy_cache_outdate = minute * 90
    deep_cache_outdate = day * 10  # 1 week was not enough
    archive_after = month
    images_outdate = month
    logs_lifetime = month * 2


log_level = logging.INFO
restricted_statuses = [301, 404, 410]
thumb_size = (80, 60)
year = datetime.datetime.now().year
prev_year = year - 1
report = logging.getLogger('report')
json_db_all = '*.json'
json_db_0 = '0.json'  # announcements
json_db_1 = '1.json'  # apartments
json_db_2 = f'{year}.json'  # archive
geo = 'geo.json'
encoding = 'utf-8'
stopwords_json = config / 'stopwords.json'
headers_json = config / 'headers.json'
providers_json = config / 'providers.json'
img_extensions = ('.ico', '.mpo', '.jpg', '.jpeg', '.svg',
                  '.png', '.gif', '.webp')  # must be lowercase
too_big_file_size = 50  # MB
use_proxy = True
long_text_length = 2000
dispositions = ['1+', '2+', '3+', '4+']
number_of_images_to_save = 3
number_of_backups_to_keep = 1
min_proxy_availability_percentage = 80  # proxies below this % are removed

# Significant attributes of the announcement/apartment instances
announcement_attributes = ['date', 'images', 'urls',
                           'rooms', 'area', 'price', 'location']


def get_proxy_list() -> Path:
    fpath = config / 'proxy.list'
    if fpath.is_file():
        return fpath
    else:
        return lists / 'proxy.list'


# def get_proxy_stats() -> Path:
#     fpath = config / 'proxy.stats'
#     if fpath.is_file():
#         return fpath
#     else:
#         return lists / 'proxy.stats'


def get_download_list() -> Path:
    fpath = config / 'download.list'
    if fpath.is_file():
        return fpath
    else:
        return lists / 'download.list'


def get_locations_list() -> Path:
    fpath = config / 'locations.list'
    if fpath.is_file():
        return fpath
    else:
        return lists / 'locations.list'


# def get_stopwords_list() -> Path:
#     fpath = config / 'stopwords.list'
#     if fpath.is_file():
#         return fpath
#     else:
#         return lists / 'stopwords.list'


# List files
proxy_list = get_proxy_list()
# proxy_stats = get_proxy_stats()
download_list = get_download_list()
locations_list = get_locations_list()
# stopwords_list = get_stopwords_list()
# areas_list = logs / 'areas.list'
# urls = 'urls.list'


def get_http_headers(ext: str = '.html') -> dict[str, str]:
    with open(headers_json, 'r', encoding=encoding) as f:
        data = json.load(f)
        return data.get(ext, dict())


def to_en(s: str) -> str:
    """Utility for internationalization - i18n.
    Convert a string to EN. Removes special characters
    leaving only lowercase EN letters and hyphen.
    """
    s = unidecode.unidecode(s)
    s = s.lower()
    s = re.sub(r'\s', '-', s)
    return s
