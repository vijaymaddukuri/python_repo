import numpy as np

number = [8, 9, 9, 1, 6, 9, 5, 7, 3, 9, 7, 3, 4, 8, 3, 5, 8, 4, 8, 7, 5, 7, 3, 6, 1, 2, 7, 4, 7, 7, 8, 4, 3, 4, 2, 2, 2, 7, 3, 5, 6, 1, 1, 3, 2, 1, 1, 7, 7, 1, 4, 4, 5, 6, 1, 2, 7, 4, 5, 8, 1, 4, 8, 6, 2, 4, 3, 7, 3, 6, 2, 3, 3, 3, 2, 4, 6, 8, 9, 3, 9, 3, 1, 8, 6, 6, 3, 3, 9, 4, 6, 4, 9, 6, 7, 1, 2, 8, 7, 8, 1, 4]
price = [195, 225, 150, 150, 90, 60, 75, 255, 270, 225, 135, 195, 30, 15, 210, 105, 15, 30, 180, 60, 165, 60, 45, 225, 180, 90, 30, 210, 150, 15, 270, 60, 210, 180, 60, 225, 150, 150, 120, 195, 75, 240, 60, 45, 30, 180, 240, 285, 135, 165, 180, 240, 60, 105, 165, 240, 120, 45, 120, 165, 285, 225, 90, 105, 225, 45, 45, 45, 75, 180, 90, 240, 30, 30, 60, 135, 180, 15, 255, 180, 270, 135, 105, 135, 210, 180, 135, 195, 225, 75, 225, 15, 240, 60, 15, 180, 255, 90, 15, 150, 230, 150]
# print(sum(price)/102)

price_num = np.array(price)
expensive = price_num[price_num>139.01]
# print(expensive.size)
input_list = [[11, 12, 13, 14],
              [21, 22, 23, 24],
              [31, 32, 33, 34]]
array_name = np.array(input_list)
print(array_name[ : , 0])
print(array_name[0])
print(array_name[ : , -1])
print(array_name[-1])


array_multipleof5 = np.arange(5,51,5)

print(array_multipleof5)

# Given a single integer n, create an (n x n) 2D array with 1 on the border and 0 on the inside.
print(help(np.ones))
n = 2
x = np.ones((n,n), dtype=int)
print("Original array:")
print(x)
print("1 on the border and 0 inside in the array")
x[1:-1,1:-1] = 0
print(x)
"""
"The learning objectives of this section are:\n",
"\n",
"* Manipulate arrays\n",
"    * Reshape arrays\n",
"    * Stack arrays\n",
"* Perform operations on arrays\n",
"    * Perform basic mathematical operations\n",
"    * Apply built-in functions \n",
"    * Apply your own functions \n",
"    * Apply basic linear algebra operations \n"
"""

array1 = np.array([10,20,30,40,50])
array2 = np.arange(5)


a = np.array([1, 2, 3])
b = np.array([2, 3, 4])

print(np.hstack((a,b)))
print(np.vstack((a,b)))

array1 = np.arange(12).reshape(3,4)
print("+++++++++++")
print(array1)
array2 = np.arange(20).reshape(5,4)
print(np.arange(12).reshape(3,4))
print(np.arange(20).reshape(5,4))
print(np.vstack((array1,array2)))


theta = (np.linspace(0, np.pi, 5))
print(np.sin(theta))
