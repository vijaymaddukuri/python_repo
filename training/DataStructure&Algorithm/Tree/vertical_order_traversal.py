"""
Vertical Order Traversal:
For root horizontal distance - hd = 0
For Left Child hd = hd - 1
For right child hd = hd + 1

Start printing values from least hd:

Example:

Vertical Order

-3 -2 -1 0 1
l   d  b a c
       h e i

"""

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

from collections import deque
from collections import defaultdict

class Solution(object):
    def verticalOrder(self, root):
        """
        :type root: TreeTreeNode
        :rtype: List[List[int]]
        """
        vPosToVals = defaultdict(list)

        leftMost  = 0   # the known minimum vertical position
        rightMost = -1  # the known maximum vertical position

        queue = deque() # each item is a pair (node, verticalPosition)
        if root:
            queue.append( (root,0) )
            leftMost = 0
            rightMost = 0

        while queue:
            node, vPos = queue.popleft()
            vPosToVals[vPos].append( node.val )

            if node.left:
                queue.append( (node.left, vPos-1) )
                leftMost = min(leftMost, vPos-1)
            if node.right:
                queue.append( (node.right, vPos+1) )
                rightMost = max(rightMost, vPos+1)

        ret = []
        for pos in range(leftMost, rightMost+1):
            ret.append( vPosToVals[pos] )

        return ret

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.left = TreeNode(6)
root.right.right = TreeNode(7)
root.right.left.right = TreeNode(8)
root.right.right.left = TreeNode(10)
root.right.right.right = TreeNode(9)
root.right.right.left.right = TreeNode(11)
root.right.right.left.right.right = TreeNode(12)
print("Vertical order traversal is ")
obj= Solution()
print(obj.verticalOrder(root))

import collections

# Binary tree node
class Node:
    # Constructor to create a new node
    def __init__(self, info):
        self.info = info
        self.left = self.right = None



# function to print vertical order traversal of binary tree
def verticalTraverse(root):
    # Base case
    if root is None:
        return

    # Create empty queue for level order traversal 
    queue = []
    levelOrder = []

    # create a map to store nodes info at a particular
    # horizontal distance 
    m = {}

    # map to store horizontal distance of nodes 
    hd_node = {}

    # enqueue root 
    queue.append(root)
    levelOrder.append(root.info)
    # store the horizontal distance of root as 0 
    hd_node[root] = 0

    m[0] = [root.info]

    # loop will run while queue is not empty 
    while len(queue) > 0:

        # dequeue node from queue 
        temp = queue.pop(0)

        if temp.left:
            # Enqueue left child 
            queue.append(temp.left)
            levelOrder.append(temp.left.info)

            # Store the horizontal distance of left node 
            # hd(left child) = hd(parent) -1 
            hd_node[temp.left] = hd_node[temp] - 1
            hd = hd_node[temp.left]

            if m.get(hd) is None:
                m[hd] = []

            m[hd].append(temp.left.info)

        if temp.right:
            # Enqueue right child 
            queue.append(temp.right)
            levelOrder.append(temp.right.info)

            # store the horizontal distance of right child 
            # hd(right child) = hd(parent) + 1 
            hd_node[temp.right] = hd_node[temp] + 1
            hd = hd_node[temp.right]

            if m.get(hd) is None:
                m[hd] = []

            m[hd].append(temp.right.info)

    # Sort the map according to horizontal distance
    sorted_m = collections.OrderedDict(sorted(m.items()))

    # Traverse the sorted map and print nodes at each horizontal distance
    for i in sorted_m.values():
        for j in i:
            print(j, " ", end="")
        print()

# Driver program to check above function


"""
Constructed binary tree is  
            1 
        / \ 
        2     3 
    / \ / \ 
    4     5 6     7 
            \ / \ 
            8 10 9 
                \ 
                11 
                    \  
                    12 

"""


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.left = Node(6)
root.right.right = Node(7)
root.right.left.right = Node(8)
root.right.right.left = Node(10)
root.right.right.right = Node(9)
root.right.right.left.right = Node(11)
root.right.right.left.right.right = Node(12)
print("Vertical order traversal is ")
verticalTraverse(root)


root = Node(1)
root.right = Node(2)
root.right.right = Node(5)
root.right.right.left = Node(3)
root.right.right.right = Node(6)
root.right.right.left.right = Node(4)
print("Vertical order traversal is ")
verticalTraverse(root)
