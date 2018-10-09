a = [2, 5, 8, 12, 23, 38, 56, 72, 91]


def binary_search(arr, n):
    first = 0
    last = len(arr)-1
    found = False
    while(first<last and not found):
        mid = (first+last)//2
        if arr[mid]==n:
            found = True
        else:
            if arr[mid] > n:
                last = mid - 1
            else:
                first=mid+1
    return found

print(binary_search(a, 1))