# Simple, durable tables.

from os import path
import json


class SimpleTable:

    def __init__(self, filename: str):
        """Create a table that will be made durable by writing to parm filename."""

        self.filename = filename            # JSON file that the table will be persisted to.
        self.rows = []                      # List of rows in the table.

        # Read any previous contents of the file into memory.
        if path.exists(self.filename):
            f = open(self.filename, 'r')
            whole_text = (f.read())
            self.rows = json.loads(whole_text)
            f.close()

    def insert(self, row: list):
        """Insert the parm row into the table."""
        self.rows.append(row)

    def commit(self):
        """Write the table to durable storage."""
        f = open(self.filename, 'w')
        f.writelines(json.dumps(self.rows))
        f.close()
