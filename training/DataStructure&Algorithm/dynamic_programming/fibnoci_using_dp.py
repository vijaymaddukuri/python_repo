# def fib(n, dp):
#     if n<=1:
#         dp[n]=n
#     if dp[n] != -1:
#         return dp[n]
#     dp[n] = fib(n-1, dp) + fib(n-2, dp)
#     return dp[n]
# n = 6
# dp = [-1 for i in range(n+1)]
# print("initial values of dp=",dp, "\t Object reference id of dp=",id(dp))
# fib(n, dp)
# print("After execution values of dp=",dp, "\t Object reference id of dp=",id(dp))
# print(dp[:-1])
# def fib(n, computed = {0: 0, 1: 1}):
#     if n not in computed:
#         computed[n] = fib(n-1, computed) + fib(n-2, computed)
#     return computed[n]
#
# a=fib(500)
#
# print(a)

def fibonacci(n, cache = [0, 1]):
    if len(cache) <= n:
        cache.append(fibonacci(n - 1) + fibonacci(n - 2))

    return cache[n]

print(fibonacci(500))