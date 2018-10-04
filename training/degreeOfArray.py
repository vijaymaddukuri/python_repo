# Max Sequential repeated count
def degree(arr):
    num=arr[0]
    finalNum=num
    maxCount=0
    count=1
    for item in arr[1:]:
        if num == item:
            count+=1
        else:
            if count > maxCount:
                maxCount=count
                finalNum=num
            count = 1
        num=item
    if count > maxCount:
        maxCount = count
        finalNum = num

    return finalNum, maxCount
lst=[1,2,2,1]
print(degree(lst))








