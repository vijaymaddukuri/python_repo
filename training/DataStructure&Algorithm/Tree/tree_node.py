"""
A Tree node contains following parts.
1. Data
2. Pointer to left child
3. Pointer to right child
"""

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key
"""
create a simple tree with 4 nodes
    tree
      ----
       1    <-- root
     /   \
    2     3
   /
  4
"""
root = Node(1)

root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)

print(root.left.left.value)
print(root.right.value)

