import os
def monthToNum(shortMonth):

    return{
            'Jan' : '01',
            'Feb' : '02',
            'Mar' : '03',
            'Apr' : '04',
            'May' : '05',
            'Jun' : '06',
            'Jul' : '07',
            'Aug' : '08',
            'Sep' : '09',
            'Oct' : '10',
            'Nov' : '11',
            'Dec' : '12'
    }[shortMonth]

def reformatDate(dates):
    finalList = []
    for item in dates:
        date = (item.split(" "))[::-1]
        for val in range(len(date)):
            if val == 1:
                month = monthToNum(date[val])
            elif val == 2:
                day = ''.join(i for i in date[val] if i.isdigit())
                if len(','.join(day)) == 1:
                    day = '0'+day
            else:
                year = date[val]
        dateFormat='{}-{}-{}'.format(year,month, day)
        finalList.append(dateFormat)
    return finalList



if __name__ == '__main__':
    fptr = open('dateformat', 'w')

    dates_count = int(input().strip())

    dates = []

    for _ in range(dates_count):
        dates_item = input()
        dates.append(dates_item)

    result = reformatDate(dates)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
