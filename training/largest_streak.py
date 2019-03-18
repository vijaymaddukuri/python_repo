def largest_streak(arr):
    arr= set(arr)
    maxCount=0
    for i in arr:
        temp=i+1
        count=1
        while temp in arr:
            count+=1
            temp+=1
        if count>maxCount:
            maxCount=count
    return maxCount

l=[1,3,4,5,8, 15]
print(largest_streak(l))


