# Find the smallest positive integer value that cannot be represented as sum of any subset of a given array

# Examples:
#
# Input:  arr[] = {1, 3, 6, 10, 11, 15};
# Output: 2
#
# Input:  arr[] = {1, 1, 1, 1};
# Output: 5
#
# Input:  arr[] = {1, 1, 3, 4};
# Output: 10
#
# Input:  arr[] = {1, 2, 5, 10, 20, 40};
# Output: 4
#
# Input:  arr[] = {1, 2, 3, 4, 5, 6};
# Output: 22

def findSmallest(arr):
    small=1
    n = len(arr)
    for i in range(0,n):
        if arr[i] <= small:
            small = small + arr[i]
    return small

print(findSmallest([1, 3, 6, 10, 11, 15]))
print(findSmallest([1, 2, 5, 10, 20, 40]))
print(findSmallest([1, 2, 3, 4, 5, 6]))
