import unittest
from training.Collections_10.implementing_collections.sorted_set import SortedSet

class TestIterableProtocol(unittest.TestCase):
    def setUp(self):
        self.s = SortedSet([1,2,3])

    def test_iter(self):
        i = iter(self.s)
        self.assertEqual(next(i), 1)
        self.assertEqual(next(i), 2)
        self.assertEqual(next(i), 3)
        self.assertRaises(StopIteration, lambda: next(i))

    def test_for_loop(self):
        index = 0
        expected = [1, 2, 3]
        for item in self.s:
            self.assertEqual(item, expected[index])
            index+=1

if __name__ == '__main__':
    unittest.main()