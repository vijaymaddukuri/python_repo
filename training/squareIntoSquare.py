def decompose(x):
    a=[]
    c=[]
    b=0
    for i in range(1,x+1):
        a.append(i*i)
    for i in range(len(a)):
        b=0
        for j in range(1,i):
            b= b+a[i]+a[j]
            if b==x*x:
                c.append(a[i])
    return c

n=5
l=decompose(n)
print(l)


