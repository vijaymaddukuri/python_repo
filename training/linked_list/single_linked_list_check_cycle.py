class Node(object):

    def __init__(self, val):
        self.val = val
        self.next = None


def check_cycle(node):

    marker1 = node
    marker2 = node

    while marker2 != None and marker2.next != None:
        marker1 = marker1.next
        marker2 = marker2.next.next

        if marker1 == marker2:
            return True
    return False

a = Node(1)
b = Node(2)
c = Node(1)

a.next = b
b.next = c
c.next = a

print(check_cycle(a))