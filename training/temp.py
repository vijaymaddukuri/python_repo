def len_subsequnce(arr1, arr2):
    sub_seq_arr = ''
    if arr1 > arr2:
        arr1, arr2 = arr2, arr1
    m = len(arr1)
    n = len(arr2)

    L = [[None]*(n+1) for i in range(m+1)]

    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j]=0
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
    print('length of longest subsequence of one string which is substring of another string is',ans)

    # Longest Common Subsequence and sub array
    print(L[m][n], sub_seq_arr)

    # L[m][n] contains the length of LCS of arr1[0..n-1] & arr2[0..m-1],  sub_seq_arr will contain the LCS
    return L[m][n], sub_seq_arr

a2 = "ABCD"
a1 = "BACDBDCD"

print("Length of LCS is ", len_subsequnce(a1, a2))