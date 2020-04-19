# Script to test the SimpleTable class.

from simple_table import SimpleTable
from os import path, remove
import unittest


class TestSimpleTable(unittest.TestCase):

    def test_insert_and_commit(self):
        """Test row inserts and saving to file for simple, single column rows."""
        filename = 'table_scratch_simple.json'

        # At start of test, ensure the file doesn't exist.
        if path.exists(filename):
            remove(filename)

        first_table = SimpleTable(filename)
        self.assertEqual(first_table.rows, [])

        first_table.insert(['Tom'])
        self.assertEqual(first_table.rows, [['Tom']])

        first_table.insert(['Dick'])
        first_table.insert(['Harry'])
        self.assertEqual(first_table.rows, [['Tom'], ['Dick'], ['Harry']])

        first_table.commit()
        self.assertEqual(first_table.rows, [['Tom'], ['Dick'], ['Harry']])

        first_table.insert(['Barry'])
        self.assertEqual(first_table.rows, [['Tom'], ['Dick'], ['Harry'], ['Barry']])

        first_table.commit()
        second_table = SimpleTable(filename)
        self.assertEqual(second_table.rows, [['Tom'], ['Dick'], ['Harry'], ['Barry']])

        second_table.insert(['Larry'])
        self.assertEqual(second_table.rows, [['Tom'], ['Dick'], ['Harry'], ['Barry'], ['Larry']])

        second_table.commit()
        third_table = SimpleTable(filename)
        self.assertEqual(third_table.rows, [['Tom'], ['Dick'], ['Harry'], ['Barry'], ['Larry']])

    def test_complex_rows(self):
        """Test rows with many columns of many different types."""
        filename = 'table_scratch_complex.json'

        # At start of test, ensure the file doesn't exist.
        if path.exists(filename):
            remove(filename)

        first_table = SimpleTable(filename)

        row1 = [123, 'Some text', 'more text', 1.234]      # List containing a mix of types.
        first_table.insert(row1)
        row2 = [456, 'other text', 'yet more', 1.678]
        first_table.insert(row2)
        first_table.commit()

        second_table = SimpleTable(filename)
        self.assertEqual(row1, second_table.rows[0])
        self.assertEqual(row2, second_table.rows[1])


if __name__ == '__main__':
    unittest.main()
