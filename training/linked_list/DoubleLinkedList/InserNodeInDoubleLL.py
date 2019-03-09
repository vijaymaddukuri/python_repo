"""
Inserting a Node Into a Sorted Doubly Linked List
Given a reference to the head of a doubly-linked list and an integer, data,
create a new DoublyLinkedListNode object having data value data and
insert it into a sorted linked list while maintaining the sort.
"""

class DoublyLinkedListNode:
    def __init__(self, node_data):
        self.data = node_data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_node(self, node_data):
        node = DoublyLinkedListNode(node_data)

        if not self.head:
            self.head = node
        else:
            self.tail.next = node
            node.prev = self.tail


        self.tail = node

def print_doubly_linked_list(node, sep, fptr):
    while node:
        fptr.write(str(node.data))

        node = node.next

        if node:
            fptr.write(sep)

def sortedInsert(head, data):
    node = DoublyLinkedListNode(data)
    if (head == None):
        return node
    elif (data < head.data):
        node.next = head
        head.prev = node
        return node
    else:
        node = sortedInsert(head.next, data)
        head.next = node
        node.prev = head
        return head