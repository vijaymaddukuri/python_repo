from lib.trie_tree import TrieTree

import unittest


class TestPrefixTree(unittest.TestCase):
    def setUp(self):
        self.dictionary = ['dog', 'cat', 'foo', 'bar']
        self.tree = TrieTree()
        for word in self.dictionary:
            self.tree.insert_word(word)

    def test_add(self):
        # checking if dog is inserted or not.
        tmp = self.tree
        inserted_word = 'dog'
        word_found = True
        for letter in inserted_word:
            try:
                tmp = tmp.children[letter]
            except KeyError as e:
                word_found = False

        self.assertTrue(word_found)
        self.assertTrue(tmp.stop)

        # This word should not be in prefix tree.
        inserted_word = 'dogy'
        tmp = self.tree
        word_found = True
        for letter in inserted_word:
            try:
                tmp = tmp.children[letter]
            except KeyError as e:
                word_found = False
        self.assertFalse(word_found)

    def test_find_letter(self):
        res = self.tree.search_char('d')
        self.assertIsNotNone(res)

        res = self.tree.search_char('a')
        self.assertIsNone(res)
