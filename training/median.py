def median(itemList):
    length=len(itemList)
    if length==0:
        return itemList[0]
    if length%2==1:
        return itemList[((length+1)/2)-1]
    else:
        return float(sum(itemList[(length/2)-1:(length/2)+1]))/2.0

result=median([1,2,3,1])
print(result)

