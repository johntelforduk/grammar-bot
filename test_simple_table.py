# Script to test the SimpleTable class.

from simple_table import SimpleTable
from os import path, remove

import unittest


class TestSimpleTable(unittest.TestCase):

    def test_insert(self):
        filename = 'table_scratch.txt'

        # At start of test, ensure the file doesn't exist.
        if path.exists(filename):
            remove(filename)

        first_table = SimpleTable(filename)
        self.assertEqual(first_table.rows, [])

        first_table.insert('Tom')
        self.assertEqual(first_table.rows, ['Tom'])

        first_table.insert('Dick')
        first_table.insert('Harry')
        self.assertEqual(first_table.rows, ['Tom', 'Dick', 'Harry'])

        first_table.commit()
        self.assertEqual(first_table.rows, ['Tom', 'Dick', 'Harry'])

        first_table.insert('Barry')
        self.assertEqual(first_table.rows, ['Tom', 'Dick', 'Harry', 'Barry'])

        first_table.commit()
        second_table = SimpleTable(filename)
        self.assertEqual(second_table.rows, ['Tom', 'Dick', 'Harry', 'Barry'])

        second_table.insert('Larry')
        self.assertEqual(second_table.rows, ['Tom', 'Dick', 'Harry', 'Barry', 'Larry'])

        second_table.commit()
        third_table = SimpleTable(filename)
        self.assertEqual(third_table.rows, ['Tom', 'Dick', 'Harry', 'Barry', 'Larry'])


if __name__ == '__main__':
    unittest.main()
