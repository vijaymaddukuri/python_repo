def sort(itemList):
    maxPos=0
    for i in range(len(itemList)-1,0,-1):
        for j in range(i):
            if itemList[j]>itemList[j+1]:
                maxPos=j
        temp=itemList[i]
        itemList[i]=itemList[maxPos]
        itemList[maxPos]=temp
    return itemList

newList=sort([1,3,2,4,5,1])
print(newList)


