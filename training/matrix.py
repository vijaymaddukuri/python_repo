# 3x3 matrix
X = [[12,7,3],
    [4 ,5,6],
    [7 ,8,9]]
# 3x4 matrix
Y = [[5,8,1,2],
    [6,7,3,0],
    [4,5,9,1]]
# result is 3x4
def transpose(X):
    result = [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
    return result

def subtract(a,b):
    result={}
    for i in range(len(a)):
        res=[]
        for j in range(len(a[0])):
            sub=a[i][j]-b[i][j]
            res.append(sub)
        result[i]=res
    return result.values()


def multiple(A,B):
    C = [[0 for col in range(len(B[0]))] for row in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j]+=A[i][k]*B[k][j]
    return C

c=multiple(X,Y)
print c