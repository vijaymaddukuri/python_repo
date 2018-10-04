def squareRoot(item):
    if item < 0:
        raise ValueError
    if item==1:
        return 1
    low=0
    high=1+(item/2)
    while low+1<high:
        mid=low+(high-low)/2
        square=mid**2
        if square==item:
            return mid
        elif square<item:
            low=mid
        else:
            high=mid
    return low

print(squareRoot(8))