color = ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow']
newList=[]
for (i,x) in enumerate(color):
    if i not in (0,4,5):
        newList.append(x)

print newList