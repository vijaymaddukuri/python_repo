
class TrieTree(object):
    """
    Constructing TRIE for the give word
    """

    def __init__(self, letter=None):
        self.letter = letter
        self.children = {}
        self.stop = False

    def insert_word(self, word):
        """
        Adding the word to Trie tree and marking the last
        character of the word.
        :param word: Word to be inserted
        :return: Returning the trie tree object
        """
        if len(word):
            letter = word[0]
            word = word[1:]
            if letter not in self.children:
                self.children[letter] = TrieTree(letter)
            return self.children[letter].insert_word(word)
        else:
            self.stop = True
            return self

    def search_char(self, letter):
        """
        Find the letter in the children of trie tree
        :param letter: letter to be find
        :return: Trie tree object if found, else None
        """
        if letter not in self.children:
            return None
        return self.children[letter]

    def __repr__(self):
        return "PrefixTree(letter={0}, stop={1})".\
            format(self.letter, self.stop)
