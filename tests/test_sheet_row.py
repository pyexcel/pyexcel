from nose.tools import eq_, raises, assert_not_in
from pyexcel import Sheet

from ._compact import OrderedDict


class TestSheetRow:
    def setUp(self):
        self.data = [
            ["Row 0", -1, -2, -3],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9],
        ]

    def test_negative_row_index(self):
        s = Sheet(self.data, "test")
        data = s.row[-1]
        eq_(data, self.data[-1])

    def test_formatter_by_named_row(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        s.row.format("Row 1", str)
        eq_(s.row["Row 1"], ["1", "2", "3"])

    def test_rownames(self):
        s = Sheet(self.data, "test", name_rows_by_column=0)
        eq_(s.rownames, ["Row 0", "Row 1", "Row 2", "Row 3"])
        custom_rows = ["R0", "R1", "R2", "R3"]
        s.rownames = custom_rows
        eq_(s.rownames, custom_rows)

    def test_rownames2(self):
        custom_rows = ["R0", "R1", "R2", "R3"]
        s = Sheet(self.data, "test", rownames=custom_rows)
        eq_(s.rownames, custom_rows)

    @raises(NotImplementedError)
    def test_rownames3(self):
        custom_rows = ["R0", "R1", "R2", "R3"]
        Sheet(self.data, "test", name_rows_by_column=0, rownames=custom_rows)

    def test_formatter_by_named_row_2(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        s.row.format("Row 1", str)
        eq_(s.row["Row 1"], ["1", "2", "3"])

    def test_row_series_to_dict(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        content = s.to_dict(True)
        keys = ["Row 0", "Row 1", "Row 2", "Row 3"]
        assert keys == list(content.keys())

    @raises(TypeError)
    def test_extend_rows_using_wrong_data_type(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        s.extend_rows([1, 2])

    def test_formatter_by_named_row2(self):
        """Test a list of string as index"""
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        s.row.format(["Row 1", "Row 2"], str)
        assert s.row["Row 1"] == ["1", "2", "3"]
        assert s.row["Row 2"] == ["4", "5", "6"]

    def test_add(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        data = OrderedDict({"Row 5": [10, 11, 12]})
        s1 = s.row + data
        assert s1.row["Row 5"] == [10, 11, 12]
        assert_not_in("Row 5", s.row)

    def test_iadd(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        data = OrderedDict({"Row 5": [10, 11, 12]})
        s.row += data
        assert s.row["Row 5"] == [10, 11, 12]

    def test_dot_notation(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        eq_(s.row.Row_3, [7, 8, 9])

    @raises(TypeError)
    def test_add_wrong_type(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        s = s.row + "string type"  # bang

    @raises(ValueError)
    def test_delete_named_row(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        del s.row["Row 2"]
        assert s.number_of_rows() == 3
        s.row["Row 2"]  # already deleted

    @raises(ValueError)
    def test_delete_indexed_row1(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        del s.row[2]
        assert s.number_of_rows() == 3
        s.row["Row 2"]  # already deleted

    @raises(ValueError)
    def test_delete_indexed_row2(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        s.delete_named_row_at(2)
        assert s.number_of_rows() == 3
        s.row["Row 2"]  # already deleted

    @raises(ValueError)
    def test_delete_indexed_row3(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        del s.row["Row 0", "Row 1"]
        assert s.number_of_rows() == 2
        s.row["Row 1"]  # already deleted

    @raises(ValueError)
    def test_delete_row(self):
        s = Sheet(self.data, "test")
        del s.row[1, 2]
        assert s.number_of_rows() == 2
        s.row["Row 1"]  # already deleted

    def test_column_locator2(self):
        """
        Remove odd columns
        """
        sheet = Sheet(self.data)

        def locator(index, _):
            return index % 2 == 0

        del sheet.row[locator]
        assert sheet.number_of_rows() == 2

    def test_set_named_row(self):
        s = Sheet(self.data, "test")
        s.name_rows_by_column(0)
        s.row["Row 2"] = [11, 11, 11]
        assert s.row["Row 2"] == [11, 11, 11]

    def test_set_indexed_column(self):
        s = Sheet(self.data, "test", name_rows_by_column=0)
        s.column[0] = [12, 3, 4, 5]
        assert s.column[0] == [12, 3, 4, 5]
