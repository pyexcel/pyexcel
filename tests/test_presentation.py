from textwrap import dedent
import pyexcel as pe

class TestPresentation:
    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content)
        content = dedent("""
           Sheet Name: pyexcel
           +---+-----+-----+
           | 1 | 2   | 3   |
           +---+-----+-----+
           | 4 | 588 | 6   |
           +---+-----+-----+
           | 7 | 8   | 999 |
           +---+-----+-----+""").strip('\n')
        assert str(s) == content
        
    def test_irregular_usage(self):
        """textable doesn't like empty string """
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8] # one empty string
        ]
        s = pe.Sheet(content)
        content = dedent("""
           Sheet Name: pyexcel
           +---+-----+---+
           | 1 | 2   | 3 |
           +---+-----+---+
           | 4 | 588 | 6 |
           +---+-----+---+
           | 7 | 8   |   |
           +---+-----+---+""").strip('\n')
        assert str(s) == content
    

    def test_column_series(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        s = pe.Sheet(content, name_columns_by_row=0)
        print(s)
        content = dedent("""
           Sheet Name: pyexcel
           +----------+----------+----------+
           | Column 1 | Column 2 | Column 3 |
           +==========+==========+==========+
           | 1        | 2        | 3        |
           +----------+----------+----------+
           | 4        | 5        | 6        |
           +----------+----------+----------+
           | 7        | 8        | 9        |
           +----------+----------+----------+""").strip('\n')
        assert str(s) == content

    def test_data_frame(self):
        content = [
            ["", "Column 1", "Column 2", "Column 3"],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]
        s = pe.Sheet(content, name_rows_by_column=0, name_columns_by_row=0)
        print(str(s))
        content = dedent("""
            Sheet Name: pyexcel
            +-------+----------+----------+----------+
            |       | Column 1 | Column 2 | Column 3 |
            +=======+==========+==========+==========+
            | Row 1 | 1        | 2        | 3        |
            +-------+----------+----------+----------+
            | Row 2 | 4        | 5        | 6        |
            +-------+----------+----------+----------+
            | Row 3 | 7        | 8        | 9        |
            +-------+----------+----------+----------+""").strip('\n')
        assert str(s) == content

    def test_row_series(self):
        content = [
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]
        s = pe.Sheet(content, name_rows_by_column=0)
        print("X"+str(s)+"X")
        content = dedent("""
            Sheet Name: pyexcel
            +-------+---+---+---+
            | Row 1 | 1 | 2 | 3 |
            +-------+---+---+---+
            | Row 2 | 4 | 5 | 6 |
            +-------+---+---+---+
            | Row 3 | 7 | 8 | 9 |
            +-------+---+---+---+""").strip('\n')
        assert str(s) == content

    def test_book_presentation(self):
        data = {
            'Sheet 1':
            [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]
            ],
            'Sheet 2':
            [
                ['X', 'Y', 'Z'],
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]
            ],
            'Sheet 3':
            [
                ['O', 'P', 'Q'],
                [3.0, 2.0, 1.0],
                [4.0, 3.0, 2.0]
            ]
        }
        book = pe.Book(data)
        content = dedent("""
            Sheet Name: Sheet 1
            +---+---+---+
            | 1 | 2 | 3 |
            +---+---+---+
            | 4 | 5 | 6 |
            +---+---+---+
            | 7 | 8 | 9 |
            +---+---+---+
            Sheet Name: Sheet 2
            +---+---+---+
            | X | Y | Z |
            +---+---+---+
            | 1 | 2 | 3 |
            +---+---+---+
            | 4 | 5 | 6 |
            +---+---+---+
            Sheet Name: Sheet 3
            +---+---+---+
            | O | P | Q |
            +---+---+---+
            | 3 | 2 | 1 |
            +---+---+---+
            | 4 | 3 | 2 |
            +---+---+---+
            """).strip("\n")
        assert str(book) == content