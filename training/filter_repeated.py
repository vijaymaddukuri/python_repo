def count(itemsList):
    newList={}
    itemsList=list(itemsList)
    uniqueList=list(set(itemsList))
    for i in uniqueList:
        itemCount = itemsList.count(i)
        newList[i]=itemCount
    return newList

def unique1(itemsList):
    return [i for i in list(set(itemsList)) if itemsList.count(i)==1]
a=''
n=count(a)
print n
