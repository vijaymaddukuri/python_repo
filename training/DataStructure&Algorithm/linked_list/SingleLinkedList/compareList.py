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


def compare_lists(headA, headB):
    while True:
        # both nodes are None
        if (not headA) and (not headB): return 1
        # only one node is None or node data differs
        if (bool(headA) != bool(headB)) or (headA.data != headB.data): return 0
        headA = headA.next
        headB = headB.next