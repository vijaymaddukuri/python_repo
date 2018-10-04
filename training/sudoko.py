def done_or_not(board):
    result='Finished!'
    for i in range(0,len(board[0])):
        temp=[]
        temp.append(board[0][i])
        for j in range(1,len(board)):
            temp.append(board[j][i])
        temp1=list(set(temp))
        if len(temp1)!=len(temp):
            result='Try again!'
            break
    return result


input= [[5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8], [1, 9, 8, 3, 4, 2, 5, 6, 7], [8, 5, 9, 7, 6, 1, 4, 2, 3], [4, 2, 6, 8, 5, 3, 7, 9, 1], [7, 1, 3, 9, 2, 4, 8, 5, 6], [9, 6, 1, 5, 3, 7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5], [3, 4, 5, 2, 8, 6, 1, 7, 9]]

def done_or_not(sudlist) :
    numbers = set(range(1, len(sudlist) + 1))
    if (any(set(row) != numbers for row in sudlist) or
        any(set(col) != numbers for col in zip(*sudlist))) :
        return 'Try again!'
    return 'Finished!'
print len(input)

res=check_sudoku(input)
print res
