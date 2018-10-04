def sublists(lst):
    sublst = [[]]
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            sub=lst[i:j]
            sublst.append(sub)
    return sublst

# driver code
l1 = [1, 2, 3, 4]
print(sublists(l1))

