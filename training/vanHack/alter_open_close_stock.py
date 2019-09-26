#!/bin/python3
import sys
import os
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import URLError
import json
from datetime import date, timedelta, datetime
import requests

# Complete the function below.
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def openAndClosePrices(firstDate, lastDate, weekDay):
    global days
    main_day = days.index(weekDay.lower())
    date_object_1 = datetime.strptime(firstDate, '%d-%B-%Y')
    timestamp_1 = datetime.timestamp(date_object_1)

    date_object_2 = datetime.strptime(lastDate, '%d-%B-%Y')
    timestamp_2 = datetime.timestamp(date_object_2)
    r = requests.get('https://jsonmock.hackerrank.com/api/stocks')
    data = r.json()
    if 'data' in data:
        data = data['data']
    for one in data:
        test_date = (one['date'])
        datetimeObj = datetime.strptime(one['date'], '%d-%B-%Y')
        day = date.weekday(datetimeObj)
        timestamp_3 = datetime.timestamp(datetimeObj)
        if day != main_day:
            continue
        if timestamp_3 > timestamp_1 and timestamp_3 < timestamp_2:
            print(one['date'], one['open'], one['close'])



openAndClosePrices(_firstDate, _lastDate, _weekDay)