def armstrongNumber(num):
    sum = 0
    temp = num

    while temp > 0:
        print(temp)
        digit = temp % 10
        print(digit)
        print(digit ** 3)
        sum += digit ** 3
        temp //= 10
        print(temp)
        print(sum)

    if num == sum:
        print(num, "is an Armstrong number")
    else:
        print(num, "is not an Armstrong number")

armstrongNumber(153)