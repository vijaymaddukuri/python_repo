# Check the array is circular or not
# Check if every index i has an index j such that sum of elements in both directions are equal

def check(a, n):
    # check for odd
    if n % 2 == 1:
        return False

    # check if the opposite element is same
    # as a[i]
    for i in range(n // 2):
        if a[i] != a[i + (n // 2)]:
            return False

    return True

# [1,4,1,4]