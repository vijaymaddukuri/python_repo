def filterList(nList):
    temp=[]
    for i in nList:
        if i not in temp:
            temp.append(i)
    return  temp

unfilterdList=['vijay','vijay','vicky','vj','vj']

newList = filterList(unfilterdList)
print newList
