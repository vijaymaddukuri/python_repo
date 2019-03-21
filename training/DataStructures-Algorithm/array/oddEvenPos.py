"""
Rearrange array such that even index elements are smaller and odd index elements are greater
"""
def rearrange(arr, n):
    for i in range(n - 1):
        if (i % 2 == 0 and arr[i] > arr[i + 1]):
            temp = arr[i]
            arr[i] = arr[i + 1]
            arr[i + 1] = temp

        if (i % 2 != 0 and arr[i] < arr[i + 1]):
            temp = arr[i]
            arr[i] = arr[i + 1]
            arr[i + 1] = temp
    return arr

print(rearrange([1,2,3,4], 4))