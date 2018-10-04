#Given a list of integers and a target number, write a function that returns a boolean indicating if its
# possible to sum two integers from the list to reach the target number


def find(arr,target):
    for i in range(1,len(arr)):
        for j in range(1,len(arr)):
            sum=arr[i-1]+arr[j]
            if sum==target:
                return True
    return False

print(find([1,3,5,1,7],14))
