def filterUniqueList(arr):
    newList=[]
    for item in arr:
        if item not in newList:
            newList.append(item)
    return newList


print(filterUniqueList([1,1,2,2,3,4,5]))
