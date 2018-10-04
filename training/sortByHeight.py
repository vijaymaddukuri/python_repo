def sortByHeight(itemList):
    newList=[]

    for k in itemList:
        if k != -1:
            newList.append(k)
    for i in range(len(newList)-1,0,-1):
        for j in range(i):
            if newList[j]>newList[j+1]:
                temp=newList[j]
                newList[j]=newList[j+1]
                newList[j + 1]=temp
    sortedList=[]
    temp=0
    for i in range(len(itemList)):
        if itemList[i] == -1:
            sortedList.append(itemList[i])
        else:
            sortedList.append(newList[temp])
            temp += 1
    return sortedList

new=sortByHeight([-1,-1,-1])
print new