#!/usr/bin/env python3
# Get air quality

import requests  # pip install --user requests[socks]
import sys
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from constants import (
    city, station, location, proxies,
    argos_fontset, reqs_headers
)
from helpers import (
    api_by_location, coloring, show_palette
)


icon_printed = False

reqs = requests.Session()
reqs.headers.update(reqs_headers)


def debug_info(msg: str, critical=True) -> str:
    if 'ARGOS_VERSION' in os.environ:
        msg += f"{argos_fontset}"
        global icon_printed
        if not icon_printed:
            msg = ' 🜁 ? \n---\n' + msg
            icon_printed = True
    else:
        msg = 'Note: ' + msg
    print(msg)
    if critical:
        sys.exit()


def get_data(url, **kwargs):
    req = reqs.get(url, timeout=5, **kwargs)
    req.raise_for_status()
    req.encoding = req.apparent_encoding
    return req


def aqi_json_by_location(loc: str, city=None, station=None) -> dict:
    try:
        aqi_data = get_data(api_by_location(loc))
    except:  # noqa: E722
        try:
            aqi_data = get_data(api_by_location(loc), proxies=proxies)
        except:  # noqa: E722
            debug_info('Fetch failed. Reloading...')
            return {}

    try:
        aqi_json = aqi_data.json()
    except:  # noqa: E722
        debug_info('Fetch failed. Reloading...')
        return {}

    if aqi_json['status'] != 'ok' or not isinstance(
        aqi_json['data']['aqi'], int
    ):
        debug_info(
            "API problematic,"
            f" status: {aqi_json['status']},"
            f" returns: {aqi_json['data']}"
        )
        return {}

    aqi_json = aqi_json['data']
    for key in {'idx', 'attributions', 'debug'}:
        if key in aqi_json:
            del aqi_json[key]

    # Primary pollutant crawled from <pm25.in>
    try:
        if any(map(
            lambda x: x is None,
            [city, station]
        )):  # Feature triggered ONLY when [city, station] supplied
            raise

        html = get_data(
            'http://www.pm25.in/' + city
        ).text
        soup = BeautifulSoup(html, 'html.parser')
        df_list = pd.read_html(str(
            soup.find(attrs={"id": "detail-data"})
        ))

        if len(df_list) != 1:
            debug_info('Crawler confused, need to fix.')
        else:
            df = df_list[0]

        index = pd.Index(df['监测点']).get_loc(station)
        primary = df['首要污染物'].loc[index]
        if primary == '_':  # Station not available
            primary = soup.find(attrs={"class": "primary_pollutant"}) \
                .p.text.strip() \
                .replace(' ', '') \
                .replace('首要污染物：', '') \
                .replace('\n', '')  # City average

        dominent = ''
        if primary == '':
            raise
        if 'PM2.5' in primary:
            dominent += 'pm25 '
        if 'PM10' in primary:
            dominent += 'pm10 '
        if '臭氧' in primary:
            dominent += 'o3 '
        aqi_json['dominentpol'] = dominent.strip() + '\''
    except:  # noqa: E722
        pass

    return aqi_json


def aqi_detailed(loc: str, city=None, station=None, default=False) -> None:
    aqi_json = aqi_json_by_location(loc, city=city, station=station)

    try:  # String formatting
        color = coloring(aqi_json['aqi'])
        human_loc = aqi_json['city']['name'] \
            .replace('(', '/ ') \
            .replace(')', '')
        gps = list(map(
            lambda x: float(f'{x:.2f}'),
            aqi_json['city']['geo']
        ))
        time = re.sub(
            r'([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})'
            r' ([0-9]{2}:[0-9]{2})(:[0-9]{2})',
            r"<span weight='900'>\2</span> \1",
            aqi_json['time']['s']
        )
        pollutant = re.sub(
            r'([a-zA-Z])([0-9]+)',
            r'\1<small>\2</small>',
            aqi_json['dominentpol'].upper()
        ).replace('25', ' 2.5')  # NOTE: thin space (U+2009) before '2.5'
    except KeyError:
        debug_info('AQI by location failed.')
        return None

    details = [
        f"<span color='{color}'> ▶ </span>"
        " <span weight='bold'>AQI:</span>"
        " <span weight='bold' background='grey'>"
        f" {aqi_json['aqi']} / {pollutant}"
        " </span>"
        f"{argos_fontset} size=18"
        f" href='{aqi_json['city']['url']}'",
        '---',
        f"> {time}\\n"
        f"  - [UTC{aqi_json['time']['tz']}]\\n"
        f"> <span weight='900'>{human_loc}</span>\\n"
        f"  - {gps}"
        f"{argos_fontset} size=10"
    ]

    if default:
        print(
            f"🜁 <span color='{color}'>⏺</span>"
            f" {aqi_json['aqi']}",
            '---',
            sep='\n'
        )
        global icon_printed
        icon_printed = True

    print(*details, '---', sep='\n')


if __name__ == '__main__':
    aqi_detailed(location, city=city, station=station, default=True)
    aqi_detailed('beijing/us-embassy')

    # Display colors
    show_palette()
