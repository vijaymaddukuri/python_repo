def timeConversion(time):
    if time[-2:] == "AM" and int(time[0:2]) < 12:
        convTime = time[:-2]
    elif time[-2:] == "AM" and int(time[0:2])==12:
        convTime = '00' + time[2:8]
    elif time[-2:] == "PM" and int(time[0:2])==12:
        convTime = time[:-2]
    else:
        convTime = str(int(time[:2]) + 12) + time[2:8]
    return convTime

convTime = timeConversion('12:40:22AM')
print(convTime)