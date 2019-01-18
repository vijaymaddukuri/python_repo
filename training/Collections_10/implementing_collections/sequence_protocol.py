import unittest
from training.Collections_10.implementing_collections.sorted_set import SortedSet

class TestSequenceProtocol(unittest.TestCase):
    def setUp(self):
        self.s = SortedSet([1,4,2])

    def test_check_index_zero_value(self):
        self.assertEqual(self.s[0], 1)

    def test_check_last_index_value(self):
        self.assertEqual(self.s[2], 4)

    def test_outofrange_index(self):
        with self.assertRaises(IndexError):
            self.s[6]

    def test_negative_index(self):
        self.assertEqual(self.s[-1], 4)

    def test_outofrange_negative_index(self):
        with self.assertRaises(IndexError):
            self.s[-5]

    def test_slice_from_start(self):
        self.assertEqual(self.s[:3], SortedSet([1,2,3]))

    def test_slice_from_end(self):
        self.assertEqual(self.s[3:], SortedSet([1,2,3]))

    def test_slice_from_middle(self):
        self.assertEqual(self.s[1:3], SortedSet([1,2,3]))

    def test_slice_full(self):
        self.assertEqual(self.s[:], self.s)

    def test_slice_empty(self):
        self.assertEqual(self.s[10:], SortedSet())

if __name__ == '__main__':
    unittest.main()
