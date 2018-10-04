
n = int(input())
dp = [-1 for i in range(n+1)]
def fib(n, dp):
   if n<=1:
       dp[n] = n
   if dp[n] != -1:
       return dp[n]
   dp[n] = fib(n-1, dp) + fib(n-2, dp)
   return dp[n]
print(fib(n, dp))
#def fib(n):
#    if n<=1:
#        return n
#    return fib(n-1) + fib(n-2)
#print(fib(n))