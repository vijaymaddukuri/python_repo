from math import sqrt, floor
from collections import Counter

def fac(n):  
    step = lambda x: 1 + (x<<2) - ((x>>1)<<1)  
    maxq = long(floor(sqrt(n))) 
    d = 1
    q = n % 2 == 0 and 2 or 3 
    while q <= maxq and n % q != 0:
        q = step(d)
        d += 1
    return q <= maxq and [q] + fac(n//q) or [n]

def decomp(n):
    res = []
    for k, v in sorted(Counter([z for y in map(fac, [x for x in range(2, n+1)]) for z in y]).items()):
        if v != 1: res.append(str(k) + "^"+ str(v))
        else: res.append(str(k))
    return " * ".join(res)