class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def lenOfList(self):
        currentNode = self.head
        count = 0
        while currentNode is not None:
            count+=1
            currentNode = currentNode.next
        return count

    def insertEnd(self, newNode):
        if self.head is None:
            self.head = newNode
        else:
            lastNode = self.head
            while True:
                if lastNode.next is None:
                    break
                lastNode =lastNode.next
            lastNode.next = newNode

    def insertHead(self, newNode):
        if self.head is None:
            self.head = newNode
            return
        tempNode = self.head
        self.head = newNode
        self.head.next = tempNode
        del tempNode

    def insertAt(self, newNode, position):
        if position < 0 or position > self.lenOfList():
            print('Invalid position')
            return
        if position is 0:
            self.insertHead(newNode)
            return
        if self.head is None:
            self.head = newNode
            return
        currentNode = self.head
        count = 0
        prevNode = None
        while True:

            if count == position:
                prevNode.next = newNode
                newNode.next = currentNode
                break
            prevNode = currentNode
            currentNode = currentNode.next
            count +=1

    def deleteEnd(self):
        prevNode = None
        lastNode = self.head
        while lastNode.next is not None:
            prevNode = lastNode
            lastNode = lastNode.next
        prevNode.next = None

    def deleteAt(self, position):
        if position < 0 or position > self.lenOfList():
            print("Out of range position")
            return
        currentNode = self.head
        count = 0
        prevNode = None
        while True:
            if position == count:
                prevNode.next = currentNode.next
                currentNode.next = None
            prevNode = currentNode
            currentNode= currentNode.next


    def printLinkedList(self):
        if self.head is None:
            print("List is empty")
            return
        currentNode = self.head
        while True:
            if currentNode is None:
                break
            print(currentNode.data)
            currentNode=currentNode.next


node1 = Node('vijay')
node2 = Node('vicky')
node3 = Node("Maddukuri")
linkedList = LinkedList()
linkedList.insertEnd(node1)
linkedList.insertEnd(node2)
linkedList.insertHead(node3)
node4 = Node('Kumar')
linkedList.insertAt(node4, 2)
linkedList.deleteEnd()
linkedList.printLinkedList()