def array_diff(a, b):
    newList=[]
    for i in a[0:]:
        if i not in b:
            newList.append(i)
    return newList

newList=array_diff([], [1,2])
print(newList)