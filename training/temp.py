def sort(lst):
    for i in range(len(lst)-1,0,-1):
        for j in range(i):
            temp=lst[j]
            lst[j]=lst[j+1]
            lst[j + 1]=temp
    return lst

newList=sort(['is2', 'Thi1s', 'T4est', '3a'])
print newList

