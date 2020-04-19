# Script to test the last_n_items function.

from last_items import last_n_items
import unittest


class TestLastNItems(unittest.TestCase):

    def test_last_n_items(self):
        self.assertEqual(last_n_items([], 10), [])
        self.assertEqual(last_n_items([1, 2, 3, 4], 10), [4, 3, 2, 1])
        self.assertEqual(last_n_items([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 3), [13, 12, 11])
        self.assertEqual(last_n_items([1, 1, 3, 3, 7, 5], 10), [5, 7, 3, 3, 1, 1])


if __name__ == '__main__':
    unittest.main()
