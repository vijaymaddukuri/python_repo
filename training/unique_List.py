def unique_in_order(iterable):
    itemList=[]
    for i in range(len(iterable)):
        if i==0:
            itemList.append(iterable[0])
        else:
            if itemList[-1] != iterable[i]:
                itemList.append(iterable[i])
    return itemList



def unique_in_order1(iterable):
    result = []
    prev = None
    for char in iterable[0:]:
        if char != prev:
            result.append(char)
            prev = char
    return result

item=unique_in_order('AABBCCcXX')
print(item)
