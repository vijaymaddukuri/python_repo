def stringCount(strList):
    newList=[]
    for str in strList:
        if len(str) >= 2:
            if str[0] == str[-1]:
                newList.append(str)
    return newList

strList=['vijay','121','141']
new=stringCount(strList)
print new
