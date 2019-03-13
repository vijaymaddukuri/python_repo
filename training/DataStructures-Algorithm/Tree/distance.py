"""
Given a root of a tree, and an integer k. Print all the nodes which are at k distance from root.
For example, in the below tree, 4, 5 & 8 are at distance 2 from root.
"""

class Node:
    # Constructor to create a new node
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def printKDistant(root, k):
    if root is None:
        return
    if k == 0:
        print(root.data)
    else:
        printKDistant(root.left, k - 1)
        printKDistant(root.right, k - 1)


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.left = Node(8)

printKDistant(root, 2)