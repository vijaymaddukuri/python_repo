"""
Shallow copy: A reference of object is copied in other object. It means any change made to a copy of object do reflect
in the original object

Shallow copy: i=10 and j=10 will have the same id, because value is same,
 within the same scope. The id will exist if it have same references.

Deep copy: A copy of object is copied into another object. It means changes made to a copy of object
do not reflect in the original object

Creates a copy of the object and the elements of the object.
"""

# importing copy module
import copy

# Deep Copy
# initializing list 1
li1 = [1, 2, [3, 5], 4]

# using deepcopy to deep copy
li2 = copy.deepcopy(li1)

# original elements of list
print("The original elements before deep copying")
for i in range(0, len(li1)):
    print(li1[i], end=" ")

print("\r")

# adding and element to new list
li2[2][0] = 7

# Change is reflected in l2
print("The new list of elements after deep copying ")
for i in range(0, len(li1)):
    print(li2[i], end=" ")

print("\r")

# Change is NOT reflected in original list
# as it is a deep copy
print("The original elements after deep copying")
for i in range(0, len(li1)):
    print(li1[i], end=" ")


# Shallow copy
print('\n')
# initializing list 1
li1 = [1, 2, [3, 5], 4]

# using copy to shallow copy
li2 = copy.copy(li1)

# original elements of list
print("The original elements before shallow copying")
for i in range(0, len(li1)):
    print(li1[i], end=" ")

print("\r")

# adding and element to new list
li2[2][0] = 7

# checking if change is reflected
print("The original elements after shallow copying")
for i in range(0, len(li1)):
    print(li1[i], end=" ")
