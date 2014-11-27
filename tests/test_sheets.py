import pyexcel as pe
from _compact import OrderedDict
from nose.tools import raises

    
class TestFormattableSheet:
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
        s = pe.sheets.FormattableSheet(self.data)
        s.apply_formatter(pe.formatters.RowFormatter(0, str))
        assert s.row[0] == s.row[1]

    def test_apply_column_formatter(self):
        s = pe.sheets.FormattableSheet(self.data)
        s.apply_formatter(pe.formatters.ColumnFormatter(0, float))
        assert s.column[0] == [1, 1, 1.1, 1.1, 2, 2]

    def test_apply_sheet_formatter(self):
        s = pe.sheets.FormattableSheet(self.data)
        s.apply_formatter(pe.formatters.SheetFormatter(float))
        assert s.row[0] == s.row[1]
        assert s.column[0] == [1, 1, 1.1, 1.1, 2, 2]

    def test_freeze_formatter(self):
        s = pe.sheets.FormattableSheet(self.data)
        s.freeze_formatters()

    def test_empty_sheet(self):
        s = pe.sheets.FormattableSheet([])
        ret = s.cell_value(100, 100)
        assert ret is None
        ret = s._cell_value(100, 100)
        assert ret == ""
        
class TestFilterSheet:
    def test_freeze_filters(self):
        data = [
            [1, 2, 3],
            [2, 3, 4]
        ]
        s = pe.sheets.FilterableSheet(data)
        s.add_filter(pe.filters.EvenRowFilter())
        s.freeze_filters()
        assert s.row[0] == [1, 2, 3]
        assert s.column[0] == [1]

    @raises(NotImplementedError)
    def test_non_filter(self):
        data = []
        s = pe.sheets.FilterableSheet(data)
        s.filter("abc")  # bang


class TestSheetNamedColumn:
    def setUp(self):
        self.data = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

    def test_formatter_by_named_column(self):
        """Test one named column"""
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(0)
        f = pe.formatters.NamedColumnFormatter("Column 1", str)
        s.apply_formatter(f)
        assert s.column["Column 1"] == ["1", "4", "7"]
        
    def test_formatter_by_named_columns(self):
        """Test multiple named columns"""
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(0)
        f = pe.formatters.NamedColumnFormatter(["Column 1", "Column 3"], str)
        s.apply_formatter(f)
        assert s.column["Column 1"] == ["1", "4", "7"]
        assert s.column["Column 3"] == ["3", "6", "9"]

    @raises(IndexError)
    def test_formatter_by_named_column3(self):
        """Test multiple named columns with wrong type"""
        pe.formatters.NamedColumnFormatter(["Column 1", 1], str)

    @raises(IndexError)
    def test_empty_list_in_named_column_formatter(self):
        pe.formatters.NamedColumnFormatter([], str)

    @raises(NotImplementedError)
    def test_float_in_list_for_named_column_formatter(self):
        pe.formatters.NamedColumnFormatter(1.22, str)
        
    def test_add(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(0)
        data = OrderedDict({
            "Column 4":[10, 11,12]
        })
        s = s.column + data
        assert s.column["Column 4"] == [10, 11, 12]

    @raises(TypeError)
    def test_add_wrong_type(self):
        """Add string type"""
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(0)
        s = s.column + "string type"  # bang

    @raises(ValueError)
    def test_delete_named_column(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # bang

    @raises(ValueError)
    def test_delete_indexed_column1(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column[1]
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # access it after deletion, bang

    @raises(ValueError)
    def test_delete_indexed_column2(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # access it after deletion, bang

    @raises(ValueError)
    def test_delete_indexed_column(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(0)
        s.delete_named_column_at(1)
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # access it after deletion, bang


class TestSheetNamedColumn2:
    def setUp(self):
        self.data = [
            [1, 2, 3],
            [4, 5, 6],
            ["Column 1", "Column 2", "Column 3"],
            [7, 8, 9]
        ]

    def test_series(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(2)
        assert s.colnames == ["Column 1", "Column 2", "Column 3"]
        custom_columns = ["C1", "C2", "C3"]
        s.colnames = custom_columns
        assert s.colnames == custom_columns

    def test_series2(self):
        custom_columns = ["C1", "C2", "C3"]
        s = pe.sheets.NominableSheet(self.data, "test", colnames=custom_columns)
        assert s.colnames == custom_columns

    @raises(NotImplementedError)
    def test_series3(self):
        custom_columns = ["C1", "C2", "C3"]
        pe.sheets.NominableSheet(self.data, "test", colnames=custom_columns,
                                     name_columns_by_row=0)
        
    def test_formatter_by_named_column(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(2)
        f = pe.formatters.NamedColumnFormatter("Column 1", str)
        s.apply_formatter(f)
        assert s.column["Column 1"] == ["1", "4", "7"]

    def test_formatter_by_named_column_2(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(2)
        s.column.format("Column 1", str)
        assert s.column["Column 1"] == ["1", "4", "7"]

    def test_add(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(2)
        data = OrderedDict({
            "Column 4": [10, 11, 12]
            }
        )
        s = s.column + data
        assert s.column["Column 4"] == [10, 11, 12]

    @raises(ValueError)
    def test_delete_named_column(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(2)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # bang

    def test_set_indexed_row(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_columns_by_row(2)
        s.row[0] = [10000, 1, 11]
        assert s.row[0] == [10000, 1, 11]


class TestSheetNamedRow:
    def setUp(self):
        self.data = [
            ["Row 0", -1, -2, -3],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]

    def test_formatter_by_named_row(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        f = pe.formatters.NamedRowFormatter("Row 1", str)
        s.apply_formatter(f)
        assert s.row["Row 1"] == ["1", "2", "3"]
        
    def test_rownames(self):
        s = pe.sheets.NominableSheet(self.data, "test", name_rows_by_column=0)
        assert s.rownames == ["Row 0", "Row 1", "Row 2", "Row 3"]
        custom_rows = ["R0", "R1", "R2", "R3"]
        s.rownames = custom_rows
        assert s.rownames == custom_rows
        
    def test_rownames2(self):
        custom_rows = ["R0", "R1", "R2", "R3"]
        s = pe.sheets.NominableSheet(self.data, "test", rownames=custom_rows)
        assert s.rownames == custom_rows

    @raises(NotImplementedError)
    def test_rownames3(self):
        custom_rows = ["R0", "R1", "R2", "R3"]
        pe.sheets.NominableSheet(self.data, "test", name_rows_by_column=0,
                                 rownames=custom_rows)

    def test_formatter_by_named_row_2(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        s.row.format("Row 1", str)
        assert s.row["Row 1"] == ["1", "2", "3"]

    def test_row_series_to_dict(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        content = s.to_dict(True)
        keys = ["Row 0", "Row 1", "Row 2", "Row 3"]
        assert keys == list(content.keys())

    @raises(TypeError)
    def test_extend_rows_using_wrong_data_type(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        s.extend_rows([1,2])

    def test_formatter_by_named_row2(self):
        """Test a list of string as index"""
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        f = pe.formatters.NamedRowFormatter(["Row 1", "Row 2"], str)
        s.apply_formatter(f)
        assert s.row["Row 1"] == ["1", "2", "3"]
        assert s.row["Row 2"] == ["4", "5", "6"]

    @raises(IndexError)
    def test_formatter_by_named_column3(self):
        """Test multiple named columns with wrong type"""
        pe.formatters.NamedRowFormatter(["Row 1", 1], str)

    @raises(IndexError)
    def test_empty_list_in_named_row_column(self):
        pe.formatters.NamedRowFormatter([], str)

    @raises(NotImplementedError)
    def test_float_in_list_in_named_formatter(self):
        pe.formatters.NamedRowFormatter(1.22, str)

    def test_add(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        data = OrderedDict({
            "Row 5": [10, 11, 12]
            }
        )
        s = s.row + data
        assert s.row["Row 5"] == [10, 11, 12]

    @raises(TypeError)
    def test_add_wrong_type(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        s = s.row + "string type"  # bang

    @raises(ValueError)
    def test_delete_named_row(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        del s.row["Row 2"]
        assert s.number_of_rows() == 3
        s.row["Row 2"]  # already deleted

    @raises(ValueError)
    def test_delete_indexed_row1(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        del s.row[2]
        assert s.number_of_rows() == 3
        s.row["Row 2"]  # already deleted

    @raises(ValueError)
    def test_delete_indexed_row2(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        s.delete_named_row_at(2)
        assert s.number_of_rows() == 3
        s.row["Row 2"]  # already deleted

    def test_set_named_row(self):
        s = pe.sheets.NominableSheet(self.data, "test")
        s.name_rows_by_column(0)
        s.row["Row 2"] = [11, 11, 11]
        assert s.row["Row 2"] == [11, 11, 11]

    def test_set_indexed_column(self):
        s = pe.sheets.NominableSheet(self.data, "test", name_rows_by_column=0)
        s.column[0] = [12, 3, 4, 5]
        assert s.column[0] == [12, 3, 4, 5]


class TestUniquenessOfNames:
    def test_column_names(self):
        data = [
            [1, 2, 3],
            [4, 5, 6],
            ["Column", "Column", "Column"],
            [7, 8, 9]
        ]
        sheet = pe.Sheet(data, name_columns_by_row=2)
        assert sheet.colnames == ["Column", "Column-1", "Column-2"]

    def test_column_names2(self):
        data = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        sheet = pe.Sheet(data)
        sheet.colnames = ["Column", "Column", "Column"]
        assert sheet.colnames == ["Column", "Column-1", "Column-2"]

    def test_row_names(self):
        data = [
            ["Row", -1, -2, -3],
            ["Row", 1, 2, 3],
            ["Row", 4, 5, 6],
            ["Row", 7, 8, 9]
        ]
        sheet = pe.Sheet(data, name_rows_by_column=0)
        assert sheet.rownames == ["Row", "Row-1", "Row-2", "Row-3"]

    def test_row_names2(self):
        data = [
            [-1, -2, -3],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        sheet = pe.Sheet(data)
        sheet.rownames = ["Row"] * 4
        assert sheet.rownames == ["Row", "Row-1", "Row-2", "Row-3"]


class TestSheetRegion:
    def test_region(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7], #  0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57]  # 4
        ]
        s = pe.Sheet(data)
        data = s.region([1, 1], [4, 5])
        expected = [
            [22, 23, 24, 25],
            [32, 33, 34, 35],
            [42, 43, 44, 45]
        ]
        assert data == expected

    def test_cut_region(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7], #  0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57]  # 4
        ]
        s = pe.Sheet(data)
        data = s.cut([1, 1], [4, 5])
        expected = [
            [22, 23, 24, 25],
            [32, 33, 34, 35],
            [42, 43, 44, 45]
        ]
        expected2 = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7], #  0
            [21, '', '', '', '', 26, 27],
            [31, '', '', '', '', 36, 37],
            [41, '', '', '', '', 46, 47],
            [51, 52, 53, 54, 55, 56, 57]  # 4
        ]
        assert data == expected
        assert s.to_array() == expected2
