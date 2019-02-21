# Driver program to test the above functions
# Let us create the following BST
#      50
#    /      \
#   30     70
#   / \    / \
#  20 40  60 80

class Node:
    def __init__(self, key):
        self.right=None
        self.left=None
        self.val=key

def insert(root, node):
    if root is None:
        root = node
    if root.val == node.val:
        return root
    else:
        print("root",root.val)
        print("node", node.val)
        if root.val < node.val and root.val != node.val:
            if root.right is None:
                root.right= node
            else:
                insert(root.right, node)
        else:
            if root.left is None:
                root.left=node
            else:
                insert(root.left, node)

def inorder(root):
    # L - V -R
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)

def pre_order_print(root):
    # V - L - R
    if not root:
        return
    print(root.val)
    pre_order_print(root.left)
    pre_order_print(root.right)

def post_order_print(root):
    # L - R - V
    if not root:
        return
    pre_order_print(root.left)
    pre_order_print(root.right)
    print(root.val)

r = Node(50)
insert(r, Node(30))
insert(r, Node(50))
insert(r, Node(60))
insert(r, Node(50))


print('pre-order')
pre_order_print(r)
print('in-order')
inorder(r)
print('post-order')
post_order_print(r)