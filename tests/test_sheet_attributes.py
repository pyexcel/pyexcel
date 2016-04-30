#since v0.2.2
from textwrap import dedent
from unittest import TestCase
from pyexcel.sheets import Sheet


class TestAttributes(TestCase):
    def test_sheet_content(self):
        array = [[1,2]]
        sheet = Sheet(array)
        expected = dedent("""
        +---+---+
        | 1 | 2 |
        +---+---+""").strip('\n')
        self.assertEqual(sheet.content, expected)
        