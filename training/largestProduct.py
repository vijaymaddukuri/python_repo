#Given a list of integers, find the largest product you could make from 3 integers in the list
def largestProduct(arr):
    high=max(arr[0],arr[1])
    low=min(arr[0],arr[1])
    high_prod2=arr[0]*arr[1]
    low_prod2=arr[0]*arr[1]
    high_prod3=arr[0]*arr[1]*arr[2]
    for item in arr[2:]:
        high_prod3=max(high_prod3,high_prod2*item,low_prod2*item)
        high_prod2=max(high_prod2,high*item,low*item)
        low_prod2=min(low_prod2,high*item,low*item)
        high=max(high,item)
        low=min(low,item)
    return high_prod3


print(largestProduct([99,-82,82,40,75,-24,39, -82, 5, 30, -25, -94, 93, -23, 48, 50, 49,-81,41,63]))