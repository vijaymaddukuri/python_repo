"""
A left rotation operation on an array of size  n shifts each of the array's elements 1 unit to the left.
For example, if 4 left rotations are performed on array [1,2,3,4,5] , then the array would become [5 1 2 3 4].


"""
def leftRotation(arr, n):
    return (arr[n:]+arr[:n])

res = (leftRotation([1,2,3,4,5], 4))
print(' '.join(str(s) for s in (res)))