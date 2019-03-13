from collections import deque
class Node(object):
    def __init__(self, val):
        self.val = val
        self.right = None
        self.left = None

def print_level_order(tree):

    # Return None when Tree is empty
    if not tree:
        return None

    # Create deque for given nodes [insert and del from both ends]
    nodes = deque([tree])
    currentCount = 1
    nextCount = 0

    while len(nodes) != 0:
        # Remove the root from the list
        currentNode = nodes.popleft()
        currentCount -= 1
        print('', currentNode.val, end='')
        # If any node is there on left, append to the list
        if currentNode.left:
            nodes.append(currentNode.left)
            nextCount += 1

        # If any node on right, append to the list
        if currentNode.right:
            nodes.append(currentNode.right)
            nextCount += 1

        if currentCount == 0:
            print('\n')
            currentCount, nextCount = nextCount, currentCount
root = Node(1)
root.left = Node(2)
root.left.left = Node(4)
root.right = Node(3)
root.right.right = Node(5)

print_level_order(root)