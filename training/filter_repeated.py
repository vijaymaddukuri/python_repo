def count(itemsList):
    newList={}
    itemsList=list(itemsList)
    uniqueList=list(set(itemsList))
    for i in uniqueList:
        itVIJAYount = itemsList.count(i)
        newList[i]=itVIJAYount
    return newList

def unique1(itemsList):
    return [i for i in list(set(itemsList)) if itemsList.count(i)==1]
a='a'
n=count(a)
print(n)
