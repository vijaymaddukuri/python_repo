def kanp_sack(wt, val, limit):
    dp = [[0 for _ in range(limit+1)] for _ in range(len(wt)+1)]

    for i in range(len(wt)+1):
        for j in range(limit+1):
            if i == 0 and j == 0:
                dp[i][j] = 0

            elif j < wt[i-1]:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(val[i-1]+dp[i-1][j-wt[i-1]], dp[i-1][j])

    return dp[len(wt)][limit]

val = [60, 100, 120]
wt = [10, 20, 30]
limit = 50
n = len(val)
print(kanp_sack(wt, val, limit))

