n=[1,2,3,4,5,6,7]
k=3

def rotateArray(n, k):
    new=n[k:]+n[:k]
    return new
newArray=rotateArray(n,k)
print(newArray)