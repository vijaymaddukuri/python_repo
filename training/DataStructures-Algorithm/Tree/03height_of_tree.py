def height(root):
    add = 0
    if root.left:
        add = 1 + height(root.left)
    if root.right:
        add = 1 + height(root.right)

    return add


# A binary tree node
class Node:
    # Constructor to create new node
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


# Iterative method to find height of Binary Tree
def treeHeight(root):
    # Base Case
    if root is None:
        return 0

    # Create a empty queue for level order traversal
    q = []

    # Enqueue Root and Initialize Height
    q.append(root)
    height = 0

    while (True):

        # n(queue size) indicates number of nodes
        # at current level
        n = len(q)
        if n == 0:
            return height

        height += 1

        # Dequeue all nodes of current level and Enqueue
        # all nodes of next level
        while (n > 0):
            node = q[0]
            q.pop(0)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)

            n -= 1


# Driver program to test above function
# Let us create binary tree shown in above diagram
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

print("Height of tree is", treeHeight(root))