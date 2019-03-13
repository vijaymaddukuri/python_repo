a = [1, 2, 3, 4, 8, 10]


def linear_search(arr, n):
    for i in range(len(arr)):
        if arr[i] == n:
            return i
    return -1

print(linear_search(a, 11))