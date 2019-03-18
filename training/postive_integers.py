def pre_fizz(n):
    newList=[]
    for i in range(n):
        if i >= 0:
            newList.append(i+1)
    return newList

def itemList(n):
    return [i+1 for i in range(n) if i>=0]

new = itemList(3)
print(new)