"""
If the difference between the  grade and the next multiple of  5 is less than 3, round  up to the next multiple of 5.
If the value of grade is less than 38, no rounding occurs as the result will still be a failing grade.

Input:
73
67
38
33

Output:
75
67
40
33
"""

def solve(grades):
    result = []
    for i in grades:
        if i >= 38:
            if i % 5 >= 3:
                i += (5 - i % 5)
        result.append(i)
    return result

print(solve([73, 67, 38, 33]))




