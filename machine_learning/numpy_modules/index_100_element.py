"""
Index of the 100th Element
Consider an (11,12) shape array. What is the index (x,y) of the 100th element? Note: For counting the elements, go row-wise.
For example, in the array:

[[1, 5, 9],
 [3, 0, 2]]
the 5th element would be '0'.
"""

import numpy as np

array1 = np.array(range(1, 11*12+1))
print(np.unravel_index(99, (11,12)))