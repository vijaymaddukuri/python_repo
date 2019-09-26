"""
STOCK OPEN and CLOSE PRICES
Write a program to retrieve and report various stock information of given days

Query for the stock info using one of the following URLS:

https://jsonmock.hackerrank.com/api/stocks:
This query returns all available stock information.
The response is paginated so you may need to query https://jsonmock.hackerrank.com/api/stocks/?page=pageNumber,
where pageNumber is an integer that describes the page number to view (e.g., 1, 2, etc.).

https://jsonmock.hackerrank.com/api/stocks/?key=value:
This query returns all results where the searched key has exact matching value.
The response is paginated, so you may need to query
https://jsonmock.hackerrank.com/api/stocks/?key=value&page=pageNumber,
where pageNumber is an integer that describes the page number to view (e.g., 1, 2, etc.).

https://jsonmock.hackerrank.com/api/stocks/search?key=value:
This query returns all the results where the searched key has values that contains value as a substring.
The response is paginated,
so you may need to query https://jsonmock.hackerrank.com/api/stocks/search?key=value&page=pageNumber,
where pageNumber is an integer that describes the page number to view (e.g., 1, 2, etc.).


Sample Json Output:

{"page":1,"per_page":500,"total":2500,"total_pages":5,
"data":[{"date":"5-January-2000","open":5265.09,"high":5464.35,"low":5184.48,"close":5357},
{"date":"6-January-2000","open":5424.21,"high":5489.86,"low":5391.33,"close":5421.53}
}

Function Description:

For the above data, print the stock information (day, Open-Bal, Close-Bal), which is available on specified day

Sample program Input:

26-March-2001
15-August-2001
Wednesday

Expected program output:

For the above date range, print the stock information (day Open-Bal Close-Bal), which is available on Wednesday

Output Example:
11-April-2001 3476.41 3325.46
18-April-2001 3311.2 3438.75
25-April-2001 3586.94 3600.83
2-May-2001 3565.53 3538.42
9-May-2001 3580.37 3586.58
23-May-2001 3640.8 3674.54
30-May-2001 3745.57 3662.04
6-June-2001 3473.32 3457.31
13-June-2001 3499.32 3501.61
20-June-2001 3410.1 3406.05
27-June-2001 3407.68 3411.64
11-July-2001 3328.37 3376.21
18-July-2001 3434.94 3383.41
8-August-2001 3317.51 3302.32
"""

import requests
import json
import datetime

def whichDay(fullDate):
    fullDate = fullDate.split('-')
    day = int(fullDate[0])
    month = int(monthToNum(fullDate[1]))
    year = int(fullDate[2])
    dayofweek = datetime.date(year, month, day).strftime("%A")
    return dayofweek

def monthToNum(shortMonth):

    return{
            'January' : '01',
            'February' : '02',
            'March' : '03',
            'April' : '04',
            'May' : '05',
            'June' : '06',
            'July' : '07',
            'August' : '08',
            'Septempber' : '09',
            'October' : '10',
            'Novmber' : '11',
            'December' : '12'
    }[shortMonth]

def split_date(date):
    date = date.split('-')
    return date[0], date[1], date[2]

def openAndClosePrices(firstDate, lastDate, weekDay):
    fday, fMonth, fYear   = split_date(firstDate)
    lday, lMonth, lYear = split_date(lastDate)
    i =0
    firstYear = int(fYear)
    lastYear = int(lYear)
    url = {}
    output = {}
    total_pages = 0

    while True:
        url[i] = "https://jsonmock.hackerrank.com/api/stocks/search?date={}".format(firstYear)
        output[i] = json.loads(requests.get(url[i]).text)
        total_pages = total_pages + output[i]["total_pages"]
        i += 1
        if firstYear == lastYear:
            break
        else:
            firstYear+=1

    counter = 0

    for p in range(total_pages):
        count = len((output[p]["data"]))
        for i in range(count):
            start = (output[p]["data"][i]['date'])
            sday, sMonth, sYear = split_date(start)
            if counter == 0:
                if sday>=fday and sMonth==fMonth and fYear == sYear:
                    counter = 1
            if counter == 1:
                if whichDay(start) ==  weekDay:
                    print('{} {} {}'.format(start, output[p]["data"][i]['open'], output[p]["data"][i]['close']))
                if int(sday)>=int(lday) and sMonth==lMonth and lYear == sYear:
                    return


result = openAndClosePrices("1-January-2000", "22-February-2000", "Monday")
