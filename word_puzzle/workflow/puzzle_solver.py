import argparse
import logging as logger
import os.path
import sys

from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

from lib.trie_tree import TrieTree
from lib.word_search import Boggle
from lib.data_logging import data_logging


def load_dictionary(tree, filepath):
    """
    Loads a dictionary file into Boggle object's word list
    :param: tree: prefix tree object
    :param name: Path to the dictionary file
    :return: None
    """
    try:
        with open(filepath) as f:
            for line in f:
                word = line.rstrip().upper()
                tree.insert_word(word)
    except IOError:
        raise Exception('Please enter a valid filename.')


def main(size, filepath):
    boggle = Boggle(size=int(size))
    tree = TrieTree()
    load_dictionary(tree, filepath)
    found = set()
    boggle.find_words(tree, found)
    for word in sorted(found):
        logger.info(word)
    logger.info(boggle)


if __name__ == '__main__':
    default_dict_path = os.path.join(parent_dir, 'conf', 'words.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--size", type=int, default=4,
                        action='store', help="Board size")
    parser.add_argument('-p', "--filepath", default=default_dict_path,
                        action='store', help="Path of words.txt file")

    args = parser.parse_args()
    data_logging()
    main(args.size, args.filepath)
