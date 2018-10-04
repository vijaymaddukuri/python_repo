#n = 5; decomp(12) -> "2^10 * 3^5 * 5^2 * 7 * 11"

def decomp(n):
    mul=1
    for i in range(1,n+1):
        mul*=i
    primeList=[]
    finalLst=''
    for num in range(2, n+1):
        if all(num % i != 0 for i in range(2, num)):
            primeList.append(num)
    for item in primeList:
        count=0
        while mul%item==0:
            count+=1
            mul=long(mul)/item
        if count == 0:
            break
        if count > 1 :
            finalLst=str(finalLst) + str(item) + '^' + str(count) + ' * '
        else:
            finalLst=str(finalLst) + str(item) + ' * '

    return finalLst.rstrip(' *')

def decomp2(n):
    is_prime = lambda n: n == 2 or n % 2 and all(n % d for d in range(3, int(n ** .5) + 1, 2))
    order = lambda n, k: n and n // k + order(n // k, k)
    decomp = lambda n: ' * '.join(
        str(p) if n < 2 * p else '%d^%d' % (p, order(n, p)) for p in range(2, n + 1) if is_prime(p))
print(decomp(5))
