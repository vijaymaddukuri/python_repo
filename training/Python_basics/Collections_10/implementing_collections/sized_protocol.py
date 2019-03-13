import unittest

from training.Python_basics.Collections_10.implementing_collections.sorted_set import SortedSet


class TestSizedProtocol(unittest.TestCase):
    def setUp(self):
        s = SortedSet([1,4,2])

    def test_positive_len(self):
        self.s = SortedSet([2])
        self.assertEqual(len(self.s), 1)

    def test_with_duplicate(self):
        self.s = SortedSet([5,5,5])
        self.assertEqual(len(self.s), 1)

if __name__ == '__main__':
    unittest.main()