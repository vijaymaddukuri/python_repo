
def productArr(arr):

    newArr=[]
    for i in arr:
        temp=i
        mul=1
        for j in arr:
            if j!=temp:
                mul=mul*j
        newArr.append(mul)
    return newArr

out=  productArr([0,1,2,3,4])
print(out)