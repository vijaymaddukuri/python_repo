def perimeter(n):
    a,b=1,1
    fib=[]
    fib.append(a)
    for i in range(n):
        a,b=b,a+b
        fib.append(a)
    sum=0
    for i in fib:
        sum=sum+i
    return 4*sum
p=perimeter(5)
print p