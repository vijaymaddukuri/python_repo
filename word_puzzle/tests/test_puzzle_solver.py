from lib.trie_tree import TrieTree
from lib.word_search import Boggle
from unittest.mock import patch
from workflow.puzzle_solver import load_dictionary, main

import io
import unittest
import mock


class FakeFileWrapper:
    def __init__(self, text):
        self.text = text

    def open(self):
        return io.StringIO(self.text)


class FileOpen:
    def __init__(self, file_access):
        self.file_access = file_access
        with self.file_access.open():
            pass

    def get_item(self):
        return "file"


class FileTest(unittest.TestCase):
    def setUp(self):
        self.filename = FileOpen(FakeFileWrapper("file"))
        self.boggle = Boggle()
        self.dictionary = ['dog', 'cat', 'foo', 'bar']
        self.tree = TrieTree()
        for word in self.dictionary:
            self.tree.insert_word(word)

    @mock.patch("workflow.puzzle_solver.open", create=True)
    def test_save_data_to_file(self, mock_open):
        mock_open.side_effect = [
            mock.mock_open(read_data="Data1").return_value,
            mock.mock_open(read_data="Data2").return_value
        ]
        load_dictionary(self.tree, self.filename)

    @patch('workflow.puzzle_solver.load_dictionary')
    def test_main_function(self, dict_mock):
        main(4, dict_mock)
