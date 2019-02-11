class Node:
    def __init__(self, key, left=None, right=None):
        self.left = left
        self.right = right
        self.val = key

class Tree:
    def __init__(self, root):
        self.root = root

    def levelOrder(self):
        list = [self.root]
        while len(list) > 0:
            print([n.val for n in list])
            list = [n.left for n in list if n.left] + [n.right for n in list if n.right]

bst = Tree(Node(1, Node(2, Node(4), Node(5)), Node(3, Node(6), Node(7))))

bst.levelOrder()