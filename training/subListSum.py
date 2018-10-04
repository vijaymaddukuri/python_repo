def sublists(lst):
    sublst = []
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            sub=lst[i:j]
            sublst.append(sub)
    return sublst

def sum1(lst):
    value=0
    for i in lst:
        value=value+i
    return value

l1 = [2, 3, -5,1, 2, -3, 10, 20]
finalLst=[]
subLst = sublists(l1)
for j in subLst:
    add=sum1(j)
    if add == 0:
        finalLst.append(j)
print finalLst


