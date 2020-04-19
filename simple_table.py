# Simple, durable tables.

from os import path


class SimpleTable:

    def __init__(self, filename: str):
        """Create a table that will be made durable by writing to parm filename."""

        self.filename = filename
        self.new_rows = []          # List of rows added to the table in this session.
        self.rows = []              # Union of old and new rows, ie. all of the rows in the table.

        # Read any previous contents of the file into memory.
        if path.exists(self.filename):
            f = open(self.filename, 'r')
            whole_text = (f.read())
            for each_line in whole_text.split():
                self.rows.append(each_line)
            f.close()

    def insert(self, row: str):
        """Insert the parm row into the table."""
        self.new_rows.append(row)
        self.rows.append(row)

    def commit(self):
        """Write the table to durable storage."""
        if path.exists(self.filename):
            f = open(self.filename, 'a')
        else:
            f = open(self.filename, 'w')

        while len(self.new_rows) > 0:
            this_addition = self.new_rows.pop(0)
            f.write(str(this_addition) + '\n')
        f.close()
