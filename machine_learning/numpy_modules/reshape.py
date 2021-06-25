import numpy as np

array1 = [[1, 5],
          [3, 7],
          [4, 9]]
np_array = np.array(array1)
print(np_array)
print(np.reshape(np_array, -1))
"""
Consider the array provided below: 

[[1, 2, 3, 4, 5]
 [6, 7, 8, 9, 10]
 [11, 12, 13, 14, 15]
 [16, 17, 18, 19, 20]]
Now, you are expected to generate the following array out of it:

[[1, 3]
 [5, 7]
 [9, 11]
 [13, 15]
 [17, 19]]
Which code will give you the correct output?
"""
array2 = [[1, 2, 3, 4, 5],
          [6, 7, 8, 9, 10],
          [11, 12, 13, 14, 15],
          [16, 17, 18, 19, 20]]
array_1 = np.array(array2)
print(array_1[array_1%2 != 0].reshape(5, 2))

print(array_1[array_1%2 != 0])

p = [[1, 5],
     [3, 7],
     [4, 9]]

print(np.reshape(p, (1, -1)))

