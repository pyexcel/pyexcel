import os
from textwrap import dedent

import pyexcel as pe

from nose.tools import eq_


def test_write_texttable():
    content = [[1, 2]]
    test_file = "test.texttable"
    expected = dedent(
        """
    pyexcel_sheet1:
    +---+---+
    | 1 | 2 |
    +---+---+""",
    ).strip("\n")
    pe.save_as(array=content, dest_file_name=test_file)
    with open(test_file, "r", encoding="utf-8") as f:
        written = f.read()
        eq_(written, expected)
    os.unlink(test_file)


def test_write_texttable_book():
    content = {"Sheet": [[1, 2]]}
    test_file = "test.texttable"
    expected = dedent(
        """
    Sheet:
    +---+---+
    | 1 | 2 |
    +---+---+""",
    ).strip("\n")
    pe.save_book_as(bookdict=content, dest_file_name=test_file)
    with open(test_file, "r", encoding="utf-8") as f:
        written = f.read()
        eq_(written, expected)
    os.unlink(test_file)
