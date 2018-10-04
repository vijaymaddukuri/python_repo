def divisors(integer):
    divisor = []
    count=0
    for i in range(2, integer, 1):
        if integer % i == 0:
            divisor.append(i)
            count = 1
    if count == 0:
            divisor = str(integer)+" "+'is prime'
    return divisor

a=divisors(13)
print a
