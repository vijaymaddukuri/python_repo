def deadAntCount(ants):
    e=[]
    d=ants.replace("ant", "")
    for c in 'ant':
        temp= d.count(c)
        e.append(temp)
    return max(e)


count=deadAntCount("ant a ant anatttt")
print count