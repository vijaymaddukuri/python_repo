def miniMaxSum(arr):
    arr= sorted(arr)
    print(sum(arr[0:4]), sum(((arr[::-1]))[0:4]))

miniMaxSum([1,2,3,4,5])