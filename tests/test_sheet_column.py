from _compact import OrderedDict

from pyexcel import Sheet
from nose.tools import eq_, raises


class TestSheetColumn:
    def setUp(self):
        self.data = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

    def test_negative_row_index(self):
        s = Sheet(self.data, "test")
        data = s.column[-1]
        eq_(data, ["Column 3", 3, 6, 9])

    def test_formatter_by_named_column(self):
        """Test one named column"""
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        s.column.format("Column 1", str)
        eq_(s.column["Column 1"], ["1", "4", "7"])

    def test_formatter_by_named_columns(self):
        """Test multiple named columns"""
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        s.column.format(["Column 1", "Column 3"], str)
        eq_(s.column["Column 1"], ["1", "4", "7"])
        eq_(s.column["Column 3"], ["3", "6", "9"])

    def test_add(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        data = OrderedDict({"Column 4": [10, 11, 12]})
        s = s.column + data
        eq_(s.column.Column_4, [10, 11, 12])

    @raises(TypeError)
    def test_add_wrong_type(self):
        """Add string type"""
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        s = s.column + "string type"  # bang

    @raises(ValueError)
    def test_delete_named_column(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # bang

    @raises(ValueError)
    def test_delete_indexed_column1(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column[1]
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # access it after deletion, bang

    @raises(ValueError)
    def test_delete_indexed_column2(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # access it after deletion, bang

    @raises(ValueError)
    def test_delete_indexed_column(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        s.delete_named_column_at(1)
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # access it after deletion, bang

    @raises(ValueError)
    def test_delete_column(self):
        s = Sheet(self.data, "test")
        del s.column[1, 2]
        assert s.number_of_columns() == 1
        s.column["Column 2"]  # access it after deletion, bang


class TestSheetColumn2:
    def setUp(self):
        self.data = [
            [1, 2, 3],
            [4, 5, 6],
            ["Column 1", "Column 2", "Column 3"],
            [7, 8, 9],
        ]

    def test_series(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        eq_(s.colnames, ["Column 1", "Column 2", "Column 3"])
        custom_columns = ["C1", "C2", "C3"]
        s.colnames = custom_columns
        eq_(s.colnames, custom_columns)

    def test_series2(self):
        custom_columns = ["C1", "C2", "C3"]
        s = Sheet(self.data, "test", colnames=custom_columns)
        assert s.colnames == custom_columns

    @raises(NotImplementedError)
    def test_series3(self):
        custom_columns = ["C1", "C2", "C3"]
        Sheet(
            self.data, "test", colnames=custom_columns, name_columns_by_row=0
        )

    def test_formatter_by_named_column(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        s.column.format("Column 1", str)
        assert s.column["Column 1"] == ["1", "4", "7"]

    def test_formatter_by_named_column_2(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        s.column.format("Column 1", str)
        assert s.column["Column 1"] == ["1", "4", "7"]

    def test_add(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        data = OrderedDict({"Column 4": [10, 11, 12]})
        s = s.column + data
        assert s.column["Column 4"] == [10, 11, 12]

    def test_dot_notation(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        eq_(s.column.Column_3, [3, 6, 9])

    @raises(ValueError)
    def test_delete_named_column(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        s.column["Column 2"]  # bang

    def test_set_indexed_row(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        s.row[0] = [10000, 1, 11]
        assert s.row[0] == [10000, 1, 11]
