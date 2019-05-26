from lib.word_search import Boggle
from lib.trie_tree import TrieTree
from mock import patch

import unittest


class TestPrefixTree(unittest.TestCase):
    def setUp(self):
        self.boggle = Boggle()
        self.dictionary = ['dog', 'cat', 'foo', 'bar']
        self.tree = TrieTree()
        for word in self.dictionary:
            self.tree.insert_word(word)

    @patch('lib.word_search.choice')
    def test_random_letter_positive(self, choice_mock):
        choice_mock.return_value = 65
        res = self.boggle.random_letter()
        self.assertEqual(res, "A")

    @patch('lib.word_search.choice')
    def test_random_letter_negative(self, choice_mock):
        choice_mock.return_value = 66
        res = self.boggle.random_letter()
        self.assertNotEqual(res, "A")

    def test_find_search(self):
        self.boggle.find_words(self.tree, set())
