class newNode:
    # Construct to create a new node
    def __init__(self, key):
        self.data = key
        self.left = None
        self.right = None

# Function to pr sorted
# level order traversal
def sorted_level_order( root):

    q = []
    s = set()

    q.append(root)
    q.append(None)

    while (len(q)):
        tmp = q[0]
        q.pop(0)

        if (tmp == None):
            if (not len(s)):
                break
            for i in s:
                print(i, " ", end="")
                q.append(None)
                s = set()

        else :
            s.add(tmp.data)

            if (tmp.left != None):
                q.append(tmp.left)
            if (tmp.right != None):
                q.append(tmp.right)

# Driver Code
if __name__ == '__main__':
    root = newNode(7)
    root.left = newNode(6)
    root.right = newNode(5)
    root.left.left = newNode(4)
    root.left.right = newNode(3)
    root.right.left = newNode(2)
    root.right.right = newNode(1)
    sorted_level_order(root)