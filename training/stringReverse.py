def rev(name):
    temp=[]
    print name[4]
    for i in range(len(name),0,-1):
        print i
        temp.append(name[i-1])
        print temp
    name="".join(temp)
    return name

def revString(st):
    st=st.split(' ')
    print st
    temp=[]
    for i in range(len(st),0,-1):
        temp.append(st[i-1])
        print temp
    st=" ".join(temp)
    return st

def reverse(st):
    return " ".join(st.split(' ')[::-1])

name='vijay kumar'
newName=reverse(name)
print newName
