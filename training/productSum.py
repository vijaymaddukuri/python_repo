def prod2sum(a, b, c, d):
    product=(a*a+b*b)*(c*c+d*d)
    newPair=[]
    square=[]
    for i in range(product+1,0,-1):
        for j in range(i+1):
            if j*j==i:
                square.append(j)
    for i in range(len(square)):
        for j in range(len(square)):
            if square[i]*square[i]+square[j]*square[j]==product:
                temp=[square[i],square[j]]
                temp=sorted(temp)
                if temp not in newPair:
                    newPair.append(sorted(temp))
    return newPair

def prod2sum1(a, b, c, d):
    product = (a * a + b * b) * (c * c + d * d)
    print product
    l1 = sorted([abs(a*c+b*d),abs(a*d-b*c)])
    print l1
    l2 = sorted([abs(a*c-b*d),abs(a*d+b*c)])
    print l2
    if l1==l2:
        return [l1]
    else:
        return sorted([l1,l2])
s=prod2sum1(1,2,3,4)
print s