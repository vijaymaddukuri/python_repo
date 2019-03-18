def median(itemList):
    length=len(itemList)
    if length==0:
        return itemList[0]
    if length%2==1:
        return (itemList[(int((length+1)/2))-1])
    else:
        return float(sum(itemList[int((length/2))-1:int((length/2))+1]))/2.0

result=median([1,2,3,1,1])
print(result)

