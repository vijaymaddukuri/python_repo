"""

Count of index pairs with equal elements in an array


Given an array of n elements. The task is to count the total number of indices (i, j)
such that arr[i] = arr[j] and i != j

Input : arr[] = {1, 1, 2}
Output : 1
As arr[0] = arr[1], the pair of indices is (0, 1)

Input : arr[] = {1, 1, 1}
Output : 3
As arr[0] = arr[1], the pair of indices is (0, 1),
(0, 2) and (1, 2)

Input : arr[] = {1, 2, 3}
Output : 0

"""
def solution(A):
    arrDict = {}
    for i in A:
        arrDict[i] = arrDict.get(i, 0) + 1
    print(arrDict)
    fCount = 0
    for item in arrDict:
        count = arrDict[item]
        fCount += (count * (count-1))//2
    return fCount

A = [1,1,2,1]

print(solution(A))

