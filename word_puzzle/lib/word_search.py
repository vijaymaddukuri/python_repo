from random import choice


class Boggle(object):
    """
    Traverse to all the cells to search for possible words in the Trie tree
    """
    def __init__(self, board=None, size=15):
        """
        Boggle board class constructor to initialize the board
        :param size: Size of the board
        :param board: The points corresponding to word lengths
        :return: None
        """
        self.size = size
        if board is None:
            self.board = []
            for i in range(0, self.size):
                self.board.append([])
                for j in range(0, self.size):
                    self.board[i].append(Boggle.random_letter())
        else:
            self.board = board

    @staticmethod
    def random_letter():
        """
        Generate random letters between A-Z
        :return: Return the character
        """
        return chr(choice(range(65, 91)))

    def find_words(self, tree, found):
        """
        Search for all the words in the dictionary
        :param tree: prefix tree object
        :param found: word to search
        :return: None
        """
        for r in range(0, self.size):
            for c in range(0, self.size):
                self.dfs(tree, found, r, c)

    def dfs(self, tree, found, row, col, path=None, node=None, word=None):
        """
        Depth first search, to find the possible word from the give position
        :param tree: Trie tree object
        :param found: word found in the dictionary
        :param row: row id
        :param col: column id
        :param path: List of matrix co-ordinates
        :param node: Trie tree node
        :param word: Currently constructed word
        :return: None
        """
        letter = self.board[row][col]
        if node is None or path is None or word is None:
            node = tree.search_char(letter)
            path = [(row, col)]
            word = letter
        else:
            node = node.search_char(letter)
            path.append((row, col))
            word = word + letter
        if node is None:
            return
        elif node.stop:
            found.add(word)
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r >= 0 and r < self.size
                    and c >= 0 and c < self.size
                    and not (r == row and c == col)
                    and (r, c) not in path):
                    self.dfs(tree, found, r, c, path[:], node, word[:])

    def __repr__(self):
        """
        Prints the Boggle board

        :return: A string representation of the board
        """
        return "Boggle(size={0}, board={1})".format(self.size, self.board)
