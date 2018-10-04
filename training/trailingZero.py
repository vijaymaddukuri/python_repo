def zeros(n):
    fact=1
    count=0
    for i in range(1,n+1,1):
        fact=fact*i
    fact=str(fact)
    count=len(fact) - len(fact.rstrip('0'))
    return count

def Trailing_Zeroes(x):
    fives = 0
    for number in range(2, x+1):
        while number > 0:
            if number % 5 == 0:
                fives += 1

                number = number/5

            else:
                break
    return fives


def zeros_in_factorial(n):

    if n < 5:
        return 0
    count = 0
    i = 5
    while n//i >= 1:
        count += n // i
        i *= 5
    return count
f=zeros_in_factorial(100000000000)
print f