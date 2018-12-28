#!/usr/bin/env python3
# AQI Constants

import os

# USER PREFERENCE #####
city = 'beijing'
station = '海淀区万柳'
location = f"{city}/haidianwanliu"
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
mainfont = 'Anka/Coder Condensed'


# PRESETS #####
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
argos_fontset = f" | font='{mainfont}'"
reqs_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/70.0.3538.110 Safari/537.36'
}
