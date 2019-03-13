class Node:
    def __init__(self, key):
        self.left=None
        self.right=None
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

def search_in_bst(root, node):
    if root == None:
        return None
    if node == None:
        return None
    if root.val == node:
        return root
    else:
        if root.val < node and root.val != node:
            return search_in_bst(root.right, node)
        else:
            return search_in_bst(root.left, node)

r = Node(5)


insert(r, Node(3))
insert(r, Node(6))

a = (search_in_bst(r, 1))
if a:
    print(a.val)
else:
    print("Not found")

b= (search_in_bst(r, 3))
if b:
    print(b.val)
else:
    print("Not found")

