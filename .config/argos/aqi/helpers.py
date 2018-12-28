#!/usr/bin/env python3
# AQI widget helper

from constants import (
    token, colors, argos_fontset
)


def api_by_location(loc: str) -> dict:
    api_dict = {
        'url': 'http://api.waqi.info/feed/' + loc + '/',
        'token': token
    }
    return api_dict['url'] + '?token=' + api_dict['token']


def coloring(aqi: int) -> str:
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
