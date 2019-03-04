def nba_extrap(ppg, mpg):
    pointPerMin=ppg/float(mpg)
    print(pointPerMin)
    ppg=48*pointPerMin
    return round(ppg,2)

avg=nba_extrap(12,20)
print(avg)