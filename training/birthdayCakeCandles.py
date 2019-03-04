def birthdayCakeCandles(ar):
    sArr = sorted(ar)
    count = sArr.count(sArr[-1])
    return count


print(birthdayCakeCandles([1,4,4,1,4]))
