def rotateListByPos(lst, pos):
    index= len(lst) - pos
    lst1=lst[index:]
    lst2=lst[:index]
    final=lst1+lst2
    print(final)

a= [3, 0, 1, 4, 2, 3]
p=3
final=rotateListByPos(a,p)
