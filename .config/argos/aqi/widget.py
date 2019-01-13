#!/usr/bin/env python3
# Get air quality

import requests  # pip install --user requests[socks]
import sys
import os
import re
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from constants import places, proxies
from helpers import (
    argos_fontset, reqs_headers,
    api_by_location, coloring, show_palette
)

# Unicodes (r'[^\x00-\x7F]'+)
# ... excluding Chinese
air_symbol = '🜁'
dot = '⏺'
bullet = '▶'
thin_sp = ' '  # U+2009

icon_printed = False
exception_raising = True
time_stamp = '* Executed: ' \
    + datetime.now().strftime('%m-%d %H:%M') \
    + argos_fontset + ' ' + 'size=8'

reqs = requests.Session()
reqs.headers.update(reqs_headers)


def debug_info(msg: str, critical=True, exception=None) -> str:
    global exception_raising
    if exception:
        args = list(exception.args)
        args[0] = msg + ' ' + args[0]
        exception.args = tuple(args)
        raise exception from None
    elif exception is None and exception_raising:
        raise Exception(msg)

    msg = '# ' + msg
    if 'ARGOS_VERSION' in os.environ:
        msg += f"{argos_fontset}"
        global icon_printed
        if not icon_printed:
            msg = f' {air_symbol} \n---\n' \
                + time_stamp + '\n---\n' \
                + msg
            icon_printed = True
    print(msg)
    if critical:
        sys.exit()


def get_data(url, type, always_raise=False, **kwargs):
    try:
        req = reqs.get(url, timeout=5, **kwargs)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        if type == 'text':
            return req.text
        elif type == 'json':
            return req.json()
        else:
            raise ValueError('Data type not specified.')
    except ValueError as e:
        raise e from None
    except Exception as e:
        e = e if always_raise else None
        url = "/".join(filter(
            lambda x: x == '' or x[0] != '?',
            url.split('/')
        )).replace('http://', '').replace('https://', '')
        debug_info(f"Fetch failed: {url}", exception=e)


# Primary pollutant crawled from <pm25.in>
def crawl_pollutant(city, station=None) -> str:
    if city is None:
        raise Exception('Must specify city for pollutant-crawling.')

    html = get_data(
        'http://www.pm25.in/' + city,
        type='text'
    )
    soup = BeautifulSoup(html, 'html.parser')

    if station is not None:
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
            station = None  # Fall back to city average

    if station is None:  # City average
        primary = soup.find(attrs={"class": "primary_pollutant"}) \
            .p.text.strip() \
            .replace(' ', '') \
            .replace('首要污染物：', '') \
            .replace('\n', '')

    dominent = ''
    if primary == '':
        raise
    if 'PM2.5' in primary:
        dominent += 'pm25 '
    if 'PM10' in primary:
        dominent += 'pm10 '
    if '臭氧' in primary:
        dominent += 'o3 '

    return dominent.strip() + '\''


def aqi_json_by_location(loc: str, city=None, station=None) -> dict:
    try:
        aqi_json = get_data(
            api_by_location(loc), type='json', always_raise=True
        )
    except:  # noqa: E722
        aqi_json = get_data(
            api_by_location(loc), type='json', proxies=proxies
        )

    if aqi_json['status'] != 'ok':
        debug_info(
            "API problematic,"
            f" status: {aqi_json['status']},"
            f" returns: {aqi_json['data']}"
        )
        return {}
    elif aqi_json['data']['aqi'] == '-':
        debug_info(
            "Server side issue,"
            f" returns: {aqi_json['data']}"
        )

    aqi_json = aqi_json['data']
    for key in {'idx', 'attributions', 'debug'}:
        if key in aqi_json:
            del aqi_json[key]

    try:
        aqi_json['dominentpol'] = crawl_pollutant(city, station)
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
        ).replace('25', f'{thin_sp}2.5')
    except KeyError:
        debug_info('AQI by location failed.')
        return None

    details = [
        f"<span color='{color}'> {bullet} </span>"
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
            f"{air_symbol} <span color='{color}'>{dot}</span>"
            f" {aqi_json['aqi']}",
            '---',
            sep='\n'
        )
        global icon_printed
        icon_printed = True

    print(*details, '---', sep='\n')


if __name__ == '__main__':
    successes = []
    for idx, place in enumerate(places):
        if 'city' in place:
            if place['city'] != place['location']:
                places.insert(idx + 1, {
                    'location': place['city'],
                    'city': place['city'],
                    'backup': True
                })  # generates city average for backup

        location = place['location']
        del place['location']  # location as required arg

        entry_gen = lambda: aqi_detailed(  # noqa: E731
            location, **place,
            default=(sum(successes) == 0)
        )

        try:
            if 'backup' in place and successes[-1] == 1:
                raise Exception('redundant')
            entry_gen()
            successes.append(1)
        except Exception as e:  # noqa: E722
            if e.args == ('redundant',):
                successes.append(1)
            elif 'ARGOS_VERSION' not in os.environ:
                debug_info('# Debug:', exception=e)  # For debugging
            elif idx < len(places) - 1:
                successes.append(0)
            else:  # Last resort
                exception_raising = False
                entry_gen()

    # Display colors
    show_palette()
    print(time_stamp)
