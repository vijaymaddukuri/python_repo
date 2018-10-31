"""
If we use normal function the life span of that returned value will exist, its waste of memory.

Interpreted to end the span of function after getting value is lamada
"""
def add(x,y):
    return x+y

print("add(4,5)", (lambda x, y: x+y) (4,5))


zero = lambda fn: lambda val: val
one = lambda fn: lambda val: fn(val)
two = lambda fn: lambda val: fn(fn(val))

toInt = lambda callFn: callFn(lambda Count: Count + 1) (0)
print(toInt(one))
print(toInt(two))

succ = lambda nTimesFncall: lambda fn: lambda val: nTimesFncall(fn)

fact = lambda  n: 1 if n<=1 else n * fact(n-1)
print(fact(4))