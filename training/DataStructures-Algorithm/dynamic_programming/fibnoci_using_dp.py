def fibnoci(n):
    dp = [-1 for i in range(n+1)]
    print("initial values of dp=", dp, "\t Object reference id of dp=", id(dp))
    def gen_fib_series(n, dp):
        if n <= 1:
            dp[n] = n
        if dp[n] != -1:
            return dp[n]
        dp[n] = gen_fib_series(n - 1, dp) + gen_fib_series(n - 2, dp)
        return dp[n]
    gen_fib_series(n, dp)
    print("After execution values of dp=", dp, "\t Object reference id of dp=", id(dp))
    _ = dp.pop()
    return (dp)
print(fibnoci(5))