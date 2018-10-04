# You are given  queries. Each query is of the form two integers described below:
# 1, x -  : Insert x in your data structure.
# 2, y  : Delete one occurence of y from your data structure, if present.
# 3, z  : Check if any integer is present whose frequency is exactly . If yes, print 1 else 0.
# Logic:
# In dict1 place the item as key and count as value
# In dict2 place the count in key and item repeated count in value section

def solve(queries):
    result = []
    dict1 = {}
    dict2= {}
    for (operand, value) in queries:
        if operand == 1:
            # Increment the value (x) count in the first dict
            dict1[value] = dict1.get(value, 0) + 1
            # Assign the value count to count variable
            count=dict1[value]
            # If the X count is there in the dict2, reduce the count in dict2 
            if count-1 in dict2:
                dict2[count - 1] -= 1
                # If X count is zero in dict2, del the key from dict
                if dict2[count - 1] == 0:
                    del dict2[count - 1]
                # Increment the X count 
                dict2[count] = dict2.get(count,0)+1
            else:
                dict2[count] = dict2.get(count, 0) + 1

        elif operand == 2:
            if value in dict1:
                dict1[value] -= 1
                count = dict1[value]
                if count == 0:
                    del dict1[value]
                dict2[count + 1] -= 1
                if dict2[count + 1] == 0:
                    del dict2[count + 1]
                dict2[count] = dict2.get(count, 0) + 1
        elif operand == 3:
            if value in dict2:
                if dict2[value]>=1:
                    result.append(1)
                else:
                    result.append(0)
            else:
                result.append(0)
    return result

print solve([(1,89),
(3,15),
(1,12),
(1,47),
(1,23),
(1,66)])