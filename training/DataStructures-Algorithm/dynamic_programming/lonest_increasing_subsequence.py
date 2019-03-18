def longest_incr_subsequence(arr):
    dp = [1 for i in range(len(arr))]

    for i in range(1, len(arr)):
        for j in range(0, i):
            if arr[j] < arr[i]:
                dp[i] = max(1+dp[j], dp[i])
    return max(dp)

print(longest_incr_subsequence([10, 22, 9, 33, 21, 50, 41, 60]))