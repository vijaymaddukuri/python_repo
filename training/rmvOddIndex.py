def oddIndex(name):
    lenName=len(name)
    newName=[]
    for n in range(lenName):
        if n%2==0:
            newName.append(name[n])
    newName=''.join(newName)
    return newName

name='vijay'
new=oddIndex(name)
print(new)
