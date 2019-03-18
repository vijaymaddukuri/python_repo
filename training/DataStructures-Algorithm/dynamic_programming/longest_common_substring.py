def longest_common_substring(arr1, arr2):
    substring = 0
    if len(arr1) > len(arr2):
        arr1, arr2 = arr2, arr1
    m = len(arr1)
    n = len(arr2)

    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if arr1[i-1] == arr2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
                substring = max(substring, dp[i][j])
            else:
                dp[i][j] = 0
    return substring

a = ['a', 'b', 'c', 'd', 'a', 'f']
b = ['g', 'b', 'c', 'd', 'f']
print(longest_common_substring(a,b))
