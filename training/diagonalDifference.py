
def diagonalDifference(arr):
    diff = 0
    arr_len = len(arr)
    print(arr_len)
    for idx in range(arr_len):
        diff += arr[idx][idx]
        diff -= arr[idx][arr_len - idx - 1]

    return abs(diff)

print(diagonalDifference([[1,2,3],[4,5,6],[9,8,9]]))

