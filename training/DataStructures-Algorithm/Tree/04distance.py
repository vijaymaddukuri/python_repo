"""
Given a root of a tree, and an integer k. Print all the nodes which are at k distance from root.
For example, in the below tree, 4, 5 & 8 are at distance 2 from root.
"""

class Node:
    # Constructor to create a new node
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def printKDistant(root, k):
    if root is None:
        return
    if k == 0:
        print(root.data)
    else:
        printKDistant(root.left, k - 1)
        printKDistant(root.right, k - 1)


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.left = Node(8)

printKDistant(root, 2)


# Node of binary tree
# Function to add a new node
class newNode:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None


# Function to prnodes of given level
def printKDistant(root, klevel):
    q = []
    level = 1
    flag = False
    q.append(root)

    # extra None is appended to keep track
    # of all the nodes to be appended
    # before level is incremented by 1
    q.append(None)
    while (len(q)):
        temp = q[0]

        # prwhen level is equal to k
        if (level == klevel and temp != None):
            flag = True
            print(temp.data, end=" ")

        q.pop(0)
        if (temp == None):
            if (len(q)):
                q.append(None)
            level += 1

            # break the loop if level exceeds
            # the given level number
            if (level > klevel):
                break
        else:
            if (temp.left):
                q.append(temp.left)

            if (temp.right):
                q.append(temp.right)
    print()

    return flag


# Driver Code
if __name__ == '__main__':
    root = newNode(20)
    root.left = newNode(10)
    root.right = newNode(30)
    root.left.left = newNode(5)
    root.left.right = newNode(15)
    root.left.right.left = newNode(12)
    root.right.left = newNode(25)
    root.right.right = newNode(40)

    print("data at level 1 : ", end="")
    ret = printKDistant(root, 1)
    if (ret == False):
        print("Number exceeds total",
              "number of levels")

    print("data at level 2 : ", end="")
    ret = printKDistant(root, 2)
    if (ret == False):
        print("Number exceeds total",
              "number of levels")

    print("data at level 3 : ", end="")
    ret = printKDistant(root, 3)
    if (ret == False):
        print("Number exceeds total",
              "number of levels")

    print("data at level 6 : ", end="")
    ret = printKDistant(root, 6)
    if (ret == False):
        print("Number exceeds total number of levels")