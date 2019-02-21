def getScore(s):
    dp = [[0 for i in range(len(s))] for i in range(len(s))]

    def LPS(s):
        for i in range(len(s)):
            dp[i][i] = 1

        for sl in range(2, len(s) + 1):
            for i in range(0, len(s) - sl + 1):
                j = i + sl - 1
                if s[i] == s[j] and sl == 2:
                    dp[i][j] = 2
                elif s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

        return dp[0][len(s) - 1]

    LPS(s)
    maximum_product = 0

    for i in range(len(dp) - 1):
        value = dp[0][i] * dp[i + 1][len(dp) - 1]
        maximum_product = max(maximum_product, value)

    return maximum_product


# Driver program to test above functions
seq = "acdapmpomp"
print(getScore(seq))
