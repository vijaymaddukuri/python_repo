class Node:
    def __init__(self, key, left=None, right=None):
        self.val = key
        self.left = left
        self.right = right


def compare_tree(root1, root2):
    if root1 == None and root2 == None:
        return True
    if root1 == None or root2 == None:
        return False
    return root1.val == root2.val and \
           compare_tree(root1.left, root2.left) and \
           compare_tree(root1.right, root2.right)

r1 = (Node(1, Node(2), Node(3, Node(4))))
r2 = (Node(1, Node(2), Node(3, Node(5, Node(6)))))


print(compare_tree(r1, r2))