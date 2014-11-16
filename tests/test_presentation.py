import pyexcel as pe

class TestPresentation:
    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content)
        content = """+---+-----+-----+
| 1 | 2   | 3   |
+---+-----+-----+
| 4 | 588 | 6   |
+---+-----+-----+
| 7 | 8   | 999 |
+---+-----+-----+"""
        assert str(s) == content

    def test_column_series(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        s = pe.Sheet(content, name_columns_by_row=0)
        content = """+----------+----------+----------+
| Column 1 | Column 2 | Column 3 |
+==========+==========+==========+
| 1        | 2        | 3        |
+----------+----------+----------+
| 4        | 5        | 6        |
+----------+----------+----------+
| 7        | 8        | 9        |
+----------+----------+----------+"""
        assert str(s) == content