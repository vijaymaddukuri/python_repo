"""
In given interval find the max possible squareroots for one number
Example: 10, 20

16, 4, 2

Total count is 3

"""

def is_square(num):
    item = 0
    while item*item < num:
        item=item+1
        if item*item == num:
            return True, item
    return False, 0

def solution(A, B):
    square_dict = {}
    for i in range(A, B):
        res, num =  is_square(i)
        if res:
            square_dict[i] = [num]
            while num>1:
                res, num = is_square(num)
                if res:
                    square_dict[i].append(num)
    print(square_dict)
    return len((max(square_dict.values(), key=len)))
solution(10, 20)