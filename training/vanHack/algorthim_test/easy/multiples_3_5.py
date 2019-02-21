"""
Factors product of 3, 5

If 1, 10 is the input, output should come as 4.

We have to try all permutations and combinations for factor of 3 and 5
1 (3^0*5^0),
3 (3^1*5^1),
5 (3^0*5^1),
9 (3^2*5^0)

If input is 1, output should be 1
3^0 * 5^0= 1
Inf input is 3, output should be 1
3^1*5^0
"""

def factors(snum, lnum, fact):
    lst =[]
    i = 0
    for j in range(snum, lnum):
        temp = pow(fact, i)
        i+=1
        if temp <= lnum:
            lst.append(temp)
        else:
            break
    return lst

def getIdealNums(l, r):
    count = 0
    if l == r:
        return 1
    if l <= 0 and r <=0:
        return 0
    fact3 = factors(l, r, 3)
    fact5 = factors(l, r, 5)
    for i in fact5:
        for j in fact3:
            if i * j >= l and i * j <= r:
                count+=1
            if i * j > r:
                break
    return count

print(getIdealNums(1, 10))



