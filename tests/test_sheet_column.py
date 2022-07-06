import unittest

from pyexcel import Sheet

from ._compact import OrderedDict


class TestSheetColumn(unittest.TestCase):
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
        self.assertEqual(data, ["Column 3", 3, 6, 9])

    def test_formatter_by_named_column(self):
        """Test one named column"""
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        s.column.format("Column 1", str)
        self.assertEqual(s.column["Column 1"], ["1", "4", "7"])

    def test_formatter_by_named_columns(self):
        """Test multiple named columns"""
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        s.column.format(["Column 1", "Column 3"], str)
        self.assertEqual(s.column["Column 1"], ["1", "4", "7"])
        self.assertEqual(s.column["Column 3"], ["3", "6", "9"])

    def test_add(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        data = OrderedDict({"Column 4": [10, 11, 12]})
        s1 = s.column + data

        self.assertEqual(s1.column.Column_4, [10, 11, 12])

        # check that we don't have the column in the original sheet
        with self.assertRaises((AttributeError)):
            self.assertEqual(s.column.Column_4, [10, 11, 12])

    def test_iadd(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        data = OrderedDict({"Column 4": [10, 11, 12]})
        s.column += data
        self.assertEqual(s.column.Column_4, [10, 11, 12])

    def test_add_wrong_type(self):
        """Add string type"""
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        with self.assertRaises((TypeError)):
            s = s.column + "string type"  # bang

    def test_delete_named_column(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        with self.assertRaises((ValueError)):
            s.column["Column 2"]  # bang

    def test_delete_indexed_column1(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column[1]
        assert s.number_of_columns() == 2
        with self.assertRaises((ValueError)):
            s.column["Column 2"]  # access it after deletion, bang

    def test_delete_indexed_column2(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        with self.assertRaises((ValueError)):
            s.column["Column 2"]  # access it after deletion, bang

    def test_delete_indexed_column(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(0)
        s.delete_named_column_at(1)
        assert s.number_of_columns() == 2
        with self.assertRaises((ValueError)):
            s.column["Column 2"]  # access it after deletion, bang

    def test_delete_column(self):
        s = Sheet(self.data, "test")
        del s.column[1, 2]
        assert s.number_of_columns() == 1
        with self.assertRaises((ValueError)):
            s.column["Column 2"]  # access it after deletion, bang


class TestSheetColumn2(unittest.TestCase):
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
        self.assertEqual(s.colnames, ["Column 1", "Column 2", "Column 3"])
        custom_columns = ["C1", "C2", "C3"]
        s.colnames = custom_columns
        self.assertEqual(s.colnames, custom_columns)

    def test_series2(self):
        custom_columns = ["C1", "C2", "C3"]
        s = Sheet(self.data, "test", colnames=custom_columns)

        self.assertEqual(s.colnames, custom_columns)

    def test_series3(self):
        custom_columns = ["C1", "C2", "C3"]
        with self.assertRaises((NotImplementedError)):
            Sheet(
                self.data,
                "test",
                colnames=custom_columns,
                name_columns_by_row=0,
            )

    def test_formatter_by_named_column(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        s.column.format("Column 1", str)
        self.assertEqual(s.column["Column 1"], ["1", "4", "7"])

    def test_add(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        data = OrderedDict({"Column 4": [10, 11, 12]})
        s1 = s.column + data
        self.assertEqual(s1.column["Column 4"], [10, 11, 12])

        self.assertNotIn("Column 4", s.column)

    def test_iadd(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        data = OrderedDict({"Column 4": [10, 11, 12]})
        s.column += data

        self.assertEqual(s.column["Column 4"], [10, 11, 12])

    def test_dot_notation(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        self.assertEqual(s.column.Column_3, [3, 6, 9])

    def test_delete_named_column(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        del s.column["Column 2"]
        assert s.number_of_columns() == 2
        with self.assertRaises((ValueError)):
            s.column["Column 2"]  # bang

    def test_set_indexed_row(self):
        s = Sheet(self.data, "test")
        s.name_columns_by_row(2)
        s.row[0] = [10000, 1, 11]

        self.assertEqual(s.row[0], [10000, 1, 11])
