#!/usr/bin/env python3
# AQI widget helper

import os
from constants import mainfont

try:
    token = os.environ['TOKEN_AQICN']
except KeyError:
    token = 'demo'

colors = {
    50: '#009966',
    100: '#ffde33',
    150: '#ff9933',
    200: '#cc0033',
    300: '#660099',  # '#a804fb', brighter alt
    350: '#7e0023',  # '#8c4219', brighter alt
}

argos_fontset = " | font='%s'" % mainfont
# f-string breaks pyls, no idea why!
# ... Github: palantir/python-language-server#424

reqs_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/70.0.3538.110 Safari/537.36'
}


def api_by_location(loc: str) -> dict:
    api_dict = {
        'url': 'http://api.waqi.info/feed/' + loc + '/',
        'token': token
    }
    return api_dict['url'] + '?token=' + api_dict['token']


def coloring(aqi: int) -> str:
    try:
        int(aqi)
    except ValueError:
        return '#cccccc'

    aqi = min(aqi, 350)
    level = aqi // 50
    ceiling = 50 * (level + 1 * int(aqi % 50 != 0))
    while True:
        try:
            return colors[ceiling]
        except KeyError:
            ceiling += 50


def show_palette() -> str:
    for key, value in colors.items():
        if key == 350:
            key = '300+'
        print(
            f"<span background='{value}' color='white' weight='900'>"
            f"  ≤ {key}  </span> ",
            end=' '
        )
    print(f"{argos_fontset} size=8")
