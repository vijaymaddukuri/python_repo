def fib(n, dp):
    if n<=1:
        dp[n]=n
    if dp[n] != -1:
        return dp[n]
    dp[n] = fib(n-1, dp) + fib(n-2, dp)
    if dp[n]==dp[-1]:
        return dp
    return dp[n]
n = 6
dp = [-1 for i in range(n+1)]
print(fib(n, dp))
