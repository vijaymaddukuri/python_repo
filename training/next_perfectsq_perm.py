# There are some perfect squares with a particular property. For example the number n = 256 is a perfect square,
# its square root is 16. If we change the position of the digits of n, we may obtain another perfect square625
# (square root = 25).
# With these three digits 2,5 and 6 we can get two perfect squares: [256,625]
def next_perfectsq_perm(lower_limit, k):
    lst=[]
    fList=[]
    temp=lower_limit
    for i in range(k):
        temp=int(temp**0.5)
        next=(temp+1)**2
        temp=next
    new=str(next)
    print new
    new1=str(new[::-1])
    for i in range(len(new)):
        index=len(new)-i
        lst1 = new[index:]
        lst2 = new[:index]
        final = lst1 + lst2
        lst.append(int(final))
    for i in range(len(new1)):
        index=len(new1)-i
        lst1 = new1[index:]
        lst2 = new1[:index]
        final = lst1 + lst2
        lst.append(int(final))
    print lst
    for item in lst:
        if int(item**0.5)*int(item**0.5) == item:
            fList.append(item)
    return sorted(fList)[-1]

print(next_perfectsq_perm(100,5))