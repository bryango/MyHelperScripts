#!/usr/bin/env python3
# AQI Widget: User Settings

places = [
    { 'city': 'beijing',
      'location': 'beijing/haidianwanliu',
      'station': '海淀区万柳' },
    { 'location': 'beijing/us-embassy'}
]  # `location` required, other keys optional

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}  # only when direct connection fails

mainfont = 'Anka/Coder Condensed'
