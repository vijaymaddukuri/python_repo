#  Find length of Longest Common Subsequence and sub array string
#  Find length of longest subsequence of one string which is substring of another string
#Algorithm:

# If the last character matches
#  LCS[i][j] = L[i-1][j-1] + 1

# If the last character not matches

# LCS[i][j] = max(L[i-1][j], L[j-1][j])


def lcs(arr1, arr2):
    sub_seq_arr=''
    # Dynamically assign the arr1 and arr2 based on the length
    if len(arr1) > len(arr2):
        arr1, arr2 = arr2, arr1
    m = len(arr1)
    n = len(arr2)

    # declaring the array for storing the dp values
    L = [[None] * (n + 1) for i in range(m + 1)]

    """Following steps build L[m+1][n+1] in bottom up fashion
     Note: L[i][j] contains length of LCS of arr1[0..i-1]
     and arr2[0..j-1]"""
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif arr1[i-1] == arr2[j-1]:
                if arr1[i-1] not in sub_seq_arr:
                    sub_seq_arr = sub_seq_arr + arr1[i-1]

                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])


    # Find length of longest subsequence of one string which is substring of another string
    ans = 0
    for i in range(1, m):
        ans = max(ans, L[i][n])
    print(ans)

    # Longest Common Subsequence and sub array
    print(L[m][n], sub_seq_arr)

    # L[m][n] contains the length of LCS of arr1[0..n-1] & arr2[0..m-1],  sub_seq_arr will contain the LCS
    return L[m][n], sub_seq_arr

a2 = "ABCD"
a1 = "BACDBDCD"

print("Length of LCS is ", lcs(a1, a2))