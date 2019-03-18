"""
We define the following:

A palindrome is a sequence of characters which reads the same forward and backwards.
For example: madam and dad are palindromes, but eva and sam are not.
A subsequence is a group of characters chosen from a list while maintaining their order.
For instance, the subsequences of abc are [a,b,c,ab,ac,bc,abc]
The score of string s is the maximum product of two non-overlapping palindromic subsequences of s that we_ll
refer to as a and b. In other words, score(s) = max(length(a) x length(b)).
There may be multiple ways to choose a and b, but there can't be any overlap between the two subsequences. For example:

Index 0123456
    s attract
Palindromic subsequences are [a,t,r,c,t,aa,tt,ata,ara,ttt,trt,tat,tct,atta]. Many of these subsequences overlap,
however (e.g. atta and tct) The maximum score is obtained using the subsequence atta, |atta| = 4 and |c| or |t| = 1, 4 x 1 = 4.

Function Description

Complete the function getScore in the editor below. The function must return an integer denoting the maximum possible score of s.

getScore has the following parameter(s):
s: a string to process

Constraints
1 < |s| <= 3000
s[i] is of ascii[a-z]
Sample Case 0
Sample Input 0
acdapmpomp
Sample Output 0
15
Explanation 0
Given s = "acdapmpomp", we can choose a = "aca" and b= "pmpmp" to get a maximal product of score = 3 x 5 = 15.
"""

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
                    print(i, j)
                    print(dp[i][j])
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

        return dp[0][len(s) - 1]

    longest_subsequence_pal = LPS(s)
    print('Longest Palindromic Subsequence -', longest_subsequence_pal)

    maximum_product = 0

    for i in range(len(dp) - 1):
        value = dp[0][i] * dp[i + 1][len(dp) - 1]
        maximum_product = max(maximum_product, value)

    return maximum_product

print(getScore('acdapmpomp'))
