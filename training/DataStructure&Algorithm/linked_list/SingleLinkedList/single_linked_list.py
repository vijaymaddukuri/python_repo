class Node(object):
    def __init__(self, val):
        self.val = val
        self.nextnode = None

a = Node(1)
b = Node(2)
c = Node(3)

a.nextnode = b
b.nextnode = c

print(a.nextnode.val)
