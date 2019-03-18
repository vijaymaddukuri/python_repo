def sort(itemList):
    swaps=0
    preSwap=-1
    for i in range(len(itemList)-1,0,-1):
        if preSwap!=swaps:
            preSwap=swaps
            for j in range(i):
                if itemList[j]>itemList[j+1]:
                    temp=itemList[j]
                    itemList[j]=itemList[j+1]
                    itemList[j + 1]=temp
                    swaps+=1
        else:
            return itemList,swaps
    return itemList,swaps

newList=sort(['is2', 'Thi1s', 'T4est', '3a'])
# newList=sort(['b1',2,5,3,'a1'])
l=sort([2,5,3,'a1'])
print(newList)

