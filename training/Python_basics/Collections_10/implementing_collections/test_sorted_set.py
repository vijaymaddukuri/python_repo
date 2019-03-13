import unittest

from training.Python_basics.Collections_10.implementing_collections.sorted_set import SortedSet

class TestConstruction(unittest.TestCase):
    def test_empty(self):
        s= SortedSet([])

    def test_from_sequence(self):
        s= SortedSet([7, 8, 3, 10])

    def test_with_duplicate(self):
        s= SortedSet([8,8,8])

    def test_from_iterables(self):
        def gen6842():
            yield 6
            yield 8
            yield 4
            yield 2
        g=gen6842()
        s= SortedSet(g)

    def test_default_empty(self):
        s = SortedSet()

if __name__ == '__main__':
    unittest.main()
