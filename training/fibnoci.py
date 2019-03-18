def fib(n):
    if n <= 0:
        return "Please enter a positive integer"
    a, b, count = 0, 1, 0
    while count<n:            # First iteration:
        yield a            # yield 0 to start with and then
        a, b = b, a + b   # a will now be 1, and b will also be 1, (0 + 1)
        # temp = a+b
        # a = b
        # b =temp
        count+=1

lst=[]
for item in fib(12):
    lst.append(item)
print(lst)