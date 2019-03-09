"""
Initialize two pointers left node and right node
Move forward right node by n-1 positions
Move forward both Left and righr by 1 post till (f.next == null)
Return left.val
"""

class Node(object):
    def __init__(self, val):
        self.val = val
        self.next = None

def nth_to_last_node(n, head):

    left_node = head
    right_node = head

    for i in range(n-1):

        if not right_node.next:
            raise LookupError('n -{} is out of range'.format(n))
        right_node = right_node.next

    while right_node.next:

        left_node = left_node.next
        right_node = right_node.next

    return left_node.val

a = Node(1)
b = Node(2)
c = Node(3)
d = Node(4)

a.next = b
b.next = c
c.next = d

print(nth_to_last_node(4, a))