import unittest
from training.Collections_10.implementing_collections.sorted_set import SortedSet

class TestContainerProtocol(unittest.TestCase):
    def setUp(self):
        self.s = SortedSet([1,3,4,2])

    def test_positive(self):
        self.assertTrue(3 in self.s)

    def test_negative(self):
        self.assertFalse(5 in self.s)

    def test_positive_not_contained(self):
        self.assertTrue(5 not in self.s)

    def test_negative_not_contained(self):
        self.assertFalse(4 not in self.s)

if __name__ == '__main__':
    unittest.main()