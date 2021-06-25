"""
Description
Merge the three arrays provided to you to form a one 4x4 array.

[Hint: Check the function np.transpose() in the 'Manipulating Arrays' notebook provided.]



Input:

Array 1: 3*3

[[7, 13, 14]

[18, 10, 17]

[11, 12, 19]]



Array 2: 1-D array

[16, 6, 1]



Array 3: 1*4 array

[[5, 8, 4, 3]]



Output:

[[7 13 14 5]

[18 10 17 8]

[11 12 19 4]

[16 6 1 3]]
"""
# Import NumPy
import numpy as np
# print(help(np.transpose))
# print(help(np.append))


list_1 =[[7, 13, 14],

         [18, 10, 17],

         [11, 12, 19]]


list_2 = [16, 6, 1]

list_3 = [[5, 8, 4, 3]]

array_1 = np.array(list_1)

# array_2 = np.array(list_2)



array_1 = (np.append(array_1, list_2))
arr1_arr2 = array_1.reshape(4,3)
arr3 = np.array(list_3).transpose()

result = np.hstack((arr1_arr2, arr3))
print(result)



