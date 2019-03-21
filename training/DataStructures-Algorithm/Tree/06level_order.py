class Node:
    def __init__(self, key, left=None, right=None):
        self.val = key
        self.left = left
        self.right = right

class Tree:
    def __init__(self, root):
        self.root = root
        self.levels = []

    def print_level_order(self):
        list = [self.root]
        while len(list) > 0:
            level = ([n.val for n in list])
            list = [n.left for n in list if n.left] + [n.right for n in list if n.right]
            self.levels.append(level)
        return self.levels

nodes = (Node(1, Node(2, Node(3)), Node(4, Node(5), Node(6))))
t = Tree(nodes)
levels = t.print_level_order()
for l in levels:
    print(l)
