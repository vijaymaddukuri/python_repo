"""
For example, in the above tree root to leaf paths exist with following sums.

21 –> 10 – 8 – 3
23 –> 10 – 8 – 5
14 –> 10 – 2 – 2

So the returned value should be true only for numbers 21, 23 and 14.
For any other number, returned value should be false.
"""


class Node:
    # Constructor to create a new node
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def hasPathSum(node, s):
    # Return true if we run out of tree and s = 0
    if node is None:
        return (s == 0)

    else:
        ans = 0

        # Otherwise check both subtrees
        subSum = s - node.data

        # If we reach a leaf node and sum becomes 0, then
        # return True
        if (subSum == 0 and node.left == None and node.right == None):
            return True

        if node.left is not None:
            ans = ans or hasPathSum(node.left, subSum)
        if node.right is not None:
            ans = ans or hasPathSum(node.right, subSum)

        return ans

        # Driver program to test above functions


s = 21
root = Node(10)
root.left = Node(8)
root.right = Node(2)
root.left.right = Node(5)
root.left.left = Node(3)
root.right.left = Node(2)

if hasPathSum(root, s):
    print("There is a root-to-leaf path with sum %d" % (s))
else:
    print("There is no root-to-leaf path with sum %d" % (s))