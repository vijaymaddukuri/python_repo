def subtraction(A, B):
    fRes={}
    for i in range(len(A)):
        res=[]
        for j in range(len(A[0])):
            sub=A[i][j]-B[i][j]
            res.append(sub)
        fRes[i] = res
    return fRes.values()

def trasnpose(A):
    res = [[A[j][i] for j in range(len(A))]for i in range(len(A[0]))]
    return res

def multiple(A, B):
    C = [[0 for j in range(len(B[0]))]for i in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j]+=A[i][k]*B[k][j]
    return C

def addition(A, B):
    result=[]
    for i in range(len(A)):
        res=[]
        for j in range(len(A[0])):
            add = A[i][j]+B[i][j]
            res.append(add)
        result.append(res)
    return result


X = [[12,7,3],
    [4 ,5,6],
    [7 ,8,9]]
# 3x4 matrix
Y = [[5,8,1,2],
    [6,7,3,0],
    [4,5,9,1]]

print(subtraction(X, Y))
print(trasnpose(X))
print(multiple(X,Y))
print(addition(X, Y))