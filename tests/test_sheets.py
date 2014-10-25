import pyexcel as pe

class TestPlainSheet:
    def setUp(self):
        self.data = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            ["1", "2", "3", "4", "5", "6", "7", "8"],
            [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            [2, 3, 4, 5, 6, 7, 8, 9],
            ["2", "3", "4", "5", "6", "7", "8", "9"]            
        ]

    def test_apply_row_formatter(self):
        s = pe.sheets.PlainSheet(self.data)
        s.apply_formatter(pe.formatters.RowFormatter(0, str))
        assert s.row[0] == s.row[1]

    def test_apply_column_formatter(self):
        s = pe.sheets.PlainSheet(self.data)
        s.apply_formatter(pe.formatters.ColumnFormatter(0, float))
        assert s.column[0] == [1, 1, 1.1, 1.1, 2, 2]

    def test_apply_sheet_formatter(self):
        s = pe.sheets.PlainSheet(self.data)
        s.format(pe.formatters.SheetFormatter(float))
        assert s.row[0] == s.row[1]
        assert s.column[0] == [1, 1, 1.1, 1.1, 2, 2]

    def test_freeze_formatter(self):
        s = pe.sheets.PlainSheet(self.data)
        s.freeze_formatters()

        
class TestFilterSheet:
    def test_freeze_filters(self):
        data = [
            [1, 2, 3],
            [2, 3, 4]
        ]
        s = pe.sheets.MultipleFilterableSheet(data)
        s.add_filter(pe.filters.EvenRowFilter())
        s.freeze_filters()
        assert s.row[0] == [1, 2, 3]
        assert s.column[0] == [1]


class TestSheetNamedColumn:
    def setUp(self):
        self.data = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

    def test_add(self):
        s = pe.sheets.Sheet(self.data, "test")
        data = [
            ["Column 4"],
            [10],
            [11],
            [12]
        ]
        m = pe.iterators.Matrix(data)
        s = s.column + m
        assert s.column["Column 4"] == [10, 11, 12]

    def test_add_wrong_type(self):
        s = pe.sheets.Sheet(self.data, "test")
        try:
            s = s.column + "string type"
            assert 1==2
        except TypeError:
            assert 1==1

        