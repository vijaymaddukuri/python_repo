"""
Given pointers to the head nodes of  2 linked lists that merge together at some point,
find the Node where the two lists merge. It is guaranteed that the two head Nodes will be different,
and neither will be NULL.
"""

class SinglyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_node(self, node_data):
        node = SinglyLinkedListNode(node_data)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node


        self.tail = node

def print_singly_linked_list(node, sep, fptr):
    while node:
        fptr.write(str(node.data))

        node = node.next

        if node:
            fptr.write(sep)

def findMergeNode(headA, headB):
    h1, h2 = headA, headB
    while h1 != h2:
        h1, h2 = h1.next or headA, h2.next or headB
    return h1.data