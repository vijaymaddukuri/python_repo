def fact(n):
    fac=1
    for i in range(1,n+1):
        fac=i*fac
    return fac
f=fact(5)
print f