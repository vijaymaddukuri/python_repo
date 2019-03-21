"""
Level Order Traversal + Vertical Order Traversal

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

Level order:
abcddefglhijk

Topview
Take element from vertical order, if multple items are present take the element which appears first in level order
ldbac
"""

import collections

# Binary tree node
class Node:
    # Constructor to create a new node
    def __init__(self, info):
        self.info = info
        self.left = self.right = None



# function to print vertical order traversal of binary tree
def TopView(root):
    # Base case
    if root is None:
        return

    # Create empty queue for level order traversal 
    queue = []

    # create a map to store nodes data at a particular
    # horizontal distance 
    m = {}

    # map to store horizontal distance of nodes 
    hd_node = {}

    # enqueue root 
    queue.append(root)
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

            # store the horizontal distance of right child 
            # hd(right child) = hd(parent) + 1 
            hd_node[temp.right] = hd_node[temp] + 1
            hd = hd_node[temp.right]

            if m.get(hd) is None:
                m[hd] = []

            m[hd].append(temp.right.info)

    # Sort the map according to horizontal distance
    print(sorted(m.items()))
    sorted_m = collections.OrderedDict(sorted(m.items()))
    print(sorted_m)

    # Traverse the sorted map and print nodes at each horizontal distance
    for i in sorted_m.values():
        print(i[0], end=" ")


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
TopView(root)


root = Node(1)
root.right = Node(2)
root.right.right = Node(5)
root.right.right.left = Node(3)
root.right.right.right = Node(6)
root.right.right.left.right = Node(4)
print("Vertical order traversal is ")
TopView(root)
