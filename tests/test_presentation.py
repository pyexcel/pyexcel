from textwrap import dedent
from unittest import TestCase

import pyexcel as pe


class TestPresentation(TestCase):
    def test_normal_usage(self):
        content = [[1, 2, 3], [4, 588, 6], [7, 8, 999]]
        s = pe.Sheet(content)
        content = dedent(
            """
           pyexcel sheet:
           +---+-----+-----+
           | 1 | 2   | 3   |
           +---+-----+-----+
           | 4 | 588 | 6   |
           +---+-----+-----+
           | 7 | 8   | 999 |
           +---+-----+-----+"""
        ).strip("\n")
        self.assertEqual(str(s), content)

    def test_irregular_usage(self):
        """textable doesn't like empty string """
        content = [[1, 2, 3], [4, 588, 6], [7, 8]]  # one empty string
        s = pe.Sheet(content)
        content = dedent(
            """
           pyexcel sheet:
           +---+-----+---+
           | 1 | 2   | 3 |
           +---+-----+---+
           | 4 | 588 | 6 |
           +---+-----+---+
           | 7 | 8   |   |
           +---+-----+---+"""
        ).strip("\n")
        self.assertEqual(str(s), content)

    def test_column_series(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        s = pe.Sheet(content, name_columns_by_row=0)
        print(s)
        content = dedent(
            """
           pyexcel sheet:
           +----------+----------+----------+
           | Column 1 | Column 2 | Column 3 |
           +==========+==========+==========+
           | 1        | 2        | 3        |
           +----------+----------+----------+
           | 4        | 5        | 6        |
           +----------+----------+----------+
           | 7        | 8        | 9        |
           +----------+----------+----------+"""
        ).strip("\n")
        self.assertEqual(str(s), content)

    def test_data_frame(self):
        content = [
            ["", "Column 1", "Column 2", "Column 3"],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9],
        ]
        s = pe.Sheet(content, name_rows_by_column=0, name_columns_by_row=0)
        print(str(s))
        content = dedent(
            """
            pyexcel sheet:
            +-------+----------+----------+----------+
            |       | Column 1 | Column 2 | Column 3 |
            +=======+==========+==========+==========+
            | Row 1 | 1        | 2        | 3        |
            +-------+----------+----------+----------+
            | Row 2 | 4        | 5        | 6        |
            +-------+----------+----------+----------+
            | Row 3 | 7        | 8        | 9        |
            +-------+----------+----------+----------+"""
        ).strip("\n")
        self.assertEqual(str(s), content)

    def test_row_series(self):
        content = [["Row 1", 1, 2, 3], ["Row 2", 4, 5, 6], ["Row 3", 7, 8, 9]]
        s = pe.Sheet(content, name_rows_by_column=0)
        content = dedent(
            """
            pyexcel sheet:
            +-------+---+---+---+
            | Row 1 | 1 | 2 | 3 |
            +-------+---+---+---+
            | Row 2 | 4 | 5 | 6 |
            +-------+---+---+---+
            | Row 3 | 7 | 8 | 9 |
            +-------+---+---+---+"""
        ).strip("\n")
        self.assertEqual(str(s), content)

    def test_book_presentation(self):
        data = {
            "Sheet 1": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
            "Sheet 2": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]],
            "Sheet 3": [["O", "P", "Q"], [3.0, 2.0, 1.0], [4.0, 3.0, 2.0]],
        }
        book = pe.Book(data)
        content = dedent(
            """
        Sheet 1:
        +-----+-----+-----+
        | 1.0 | 2.0 | 3.0 |
        +-----+-----+-----+
        | 4.0 | 5.0 | 6.0 |
        +-----+-----+-----+
        | 7.0 | 8.0 | 9.0 |
        +-----+-----+-----+
        Sheet 2:
        +---+---+---+
        | X | Y | Z |
        +---+---+---+
        | 1 | 2 | 3 |
        +---+---+---+
        | 4 | 5 | 6 |
        +---+---+---+
        Sheet 3:
        +-----+-----+-----+
        | O   | P   | Q   |
        +-----+-----+-----+
        | 3.0 | 2.0 | 1.0 |
        +-----+-----+-----+
        | 4.0 | 3.0 | 2.0 |
        +-----+-----+-----+"""
        ).strip("\n")
        self.assertEqual(str(book), content)
