def maxDigit(digit, sum):
    if digit*9<sum or sum==0:
        print("invalid sum")
        return
    num_str = ""
    while sum>9:
        num_str += '9'
        sum = sum - 9
    if sum:
        num_str += str(sum)
    while len(num_str) != digit:
        num_str += '0'
    print(num_str)
digit = 4
sum=1
maxDigit(digit, sum)