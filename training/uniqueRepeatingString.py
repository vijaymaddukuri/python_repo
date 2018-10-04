def unique_in_order1(iterable):
    result = ""
    new=[]
    i=0
    prev = None
    for char in iterable[0:]:
        i+=1
        if char == prev:
            match = 1
            result=result+char
        else:
            match=-1
        prev = char
        if len(iterable) == i:
            match=-1
        if match ==-1 and result!="":
            new.append(result)
            result = ""
    return max(new,key=len)

name="vviijjaaaayydddddaadddddddddddddddddddddddddddddd"

result=unique_in_order1(name)
print result+result[0]

