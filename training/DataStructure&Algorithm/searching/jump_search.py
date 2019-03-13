import math


arr = [ 0, 1, 1, 2, 3, 5, 8, 13, 21,
    34, 55, 89, 144, 233, 377, 610 ]
ser = 55
l = len(arr)

def jump_search(arr, ser, n):
    """
    :param arr: Array
    :param ser: Searching integer
    :param l: length of an array
    :return: Boolean True or False
    """
    jumptostep = math.sqrt(n)

    prev = 0
    # Finding the block where element is
    while arr[int(min(jumptostep, n)-1)] < ser:
        prev = jumptostep
        jumptostep += math.sqrt(n)
        if prev >= n:
            return -1

    # Doing a linear search for x in
    while arr[int(prev)] < ser:
        prev+=1
        if prev == min(jumptostep,n):
            return -1

    if arr[int(prev)] == ser:
        return prev

    return -1


print(jump_search(arr, 1, l))