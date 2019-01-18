def plusMinus(arr):
    positive = (len((list(filter(lambda x: x>0, arr))))/len(arr))
    negative = (len((list(filter(lambda x: x < 0, arr)))) / len(arr))
    zero = (len((list(filter(lambda x: x == 0, arr)))) / len(arr))
    return  format(positive,".6f"), format(negative,".6f"), format(zero,".6f")

arr = [-4,3,-9,0,4,1]
print(plusMinus(arr))
