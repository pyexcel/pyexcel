import copy
from nose.tools import eq_, raises
from pyexcel import Sheet, load_from_dict, load_from_records

@raises(TypeError)
def test_non_filter():
    data = []
    s = Sheet(data)
    s.filter("abc")  # bang


def test_invalid_array_in_sheet():
    test_array = [[1, 2]]
    sheet = Sheet(test_array)
    sheet2 = Sheet(sheet)
    eq_(sheet2.array, test_array)


def test_sheet_len():
    sheet = Sheet([[1, 2]])
    eq_(len(sheet), 1)


class TestNegativeIndices:
    def setUp(self):
        self.data = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            ["1", "2", "3", "4", "5", "6", "7", "8"],
            [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            [2, 3, 4, 5, 6, 7, 8, 9],
            ["2", "3", "4", "5", "6", "7", "8", "9"],
        ]

    def test_apply_row_form(self):
        s = Sheet(self.data)
        data = s.row_at(-2)
        eq_(data, self.data[-2])


class TestFormatter:
    def setUp(self):
        self.data = [
            [1, 2, 3, 4, 5, 6, 7, 8],
            ["1", "2", "3", "4", "5", "6", "7", "8"],
            [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            [2, 3, 4, 5, 6, 7, 8, 9],
            ["2", "3", "4", "5", "6", "7", "8", "9"],
        ]

    def test_apply_row_formatter(self):
        s = Sheet(self.data)
        s.row.format(0, str)
        assert s.row[0] == s.row[1]

    def test_apply_column_formatter(self):
        s = Sheet(self.data)
        s.column.format(0, float)
        assert s.column[0] == [1, 1, 1.1, 1.1, 2, 2]

    def test_apply_sheet_formatter(self):
        s = Sheet(self.data)
        s.format(float)
        assert s.row[0] == s.row[1]
        assert s.column[0] == [1, 1, 1.1, 1.1, 2, 2]

    def test_column_locator(self):
        """
        Remove odd columns
        """
        sheet = Sheet(self.data)
        del sheet.column[lambda column_index, _: column_index % 2 == 0]
        expected = [
            [2, 4, 6, 8],
            ["2", "4", "6", "8"],
            [2.2, 4.4, 6.6, 8.8],
            ["2.2", "4.4", "6.6", "8.8"],
            [3, 5, 7, 9],
            ["3", "5", "7", "9"],
        ]
        eq_(sheet.array, expected)

    def test_column_locator2(self):
        """
        Remove odd columns
        """
        sheet = Sheet(self.data)

        def locator(index, _):
            return index % 2 == 0

        del sheet.column[locator]
        expected = [
            [2, 4, 6, 8],
            ["2", "4", "6", "8"],
            [2.2, 4.4, 6.6, 8.8],
            ["2.2", "4.4", "6.6", "8.8"],
            [3, 5, 7, 9],
            ["3", "5", "7", "9"],
        ]
        eq_(sheet.array, expected)

    @raises(IndexError)
    def test_set_row_at(self):
        s = Sheet(self.data)
        s.set_row_at(1000, [1])

    def test_set_row_at2(self):
        s = Sheet(self.data)
        s.set_row_at(1, [1])
        eq_(s[1], [1, "", "", "", "", "", "", ""])

    @raises(IndexError)
    def test_set_row_at3(self):
        s = Sheet(self.data)
        s._set_row_at(10000, 100000, [1])

    @raises(ValueError)
    def test_empty_paste(self):
        s = Sheet(self.data)
        s.paste((1, 2))


class TestUniquenessOfNames:
    def test_column_names(self):
        data = [
            [1, 2, 3],
            [4, 5, 6],
            ["Column", "Column", "Column"],
            [7, 8, 9],
        ]
        sheet = Sheet(data, name_columns_by_row=2)
        assert sheet.colnames == ["Column", "Column-1", "Column-2"]

    def test_column_names2(self):
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        sheet = Sheet(data)
        sheet.colnames = ["Column", "Column", "Column"]
        assert sheet.colnames == ["Column", "Column-1", "Column-2"]

    def test_row_names(self):
        data = [
            ["Row", -1, -2, -3],
            ["Row", 1, 2, 3],
            ["Row", 4, 5, 6],
            ["Row", 7, 8, 9],
        ]
        sheet = Sheet(data, name_rows_by_column=0)
        assert sheet.rownames == ["Row", "Row-1", "Row-2", "Row-3"]

    def test_row_names2(self):
        data = [[-1, -2, -3], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
        sheet = Sheet(data)
        sheet.rownames = ["Row"] * 4
        assert sheet.rownames == ["Row", "Row-1", "Row-2", "Row-3"]


class TestSheetRegion:
    def test_region(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57],  # 4
        ]
        s = Sheet(data)
        data = s.region([1, 1], [4, 5])
        expected = [[22, 23, 24, 25], [32, 33, 34, 35], [42, 43, 44, 45]]
        assert data == expected

    def test_cut_region(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57],  # 4
        ]
        s = Sheet(data)
        data = s.cut([1, 1], [4, 5])
        expected = [[22, 23, 24, 25], [32, 33, 34, 35], [42, 43, 44, 45]]
        expected2 = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, "", "", "", "", 26, 27],
            [31, "", "", "", "", 36, 37],
            [41, "", "", "", "", 46, 47],
            [51, 52, 53, 54, 55, 56, 57],  # 4
        ]
        assert data == expected
        assert s.to_array() == expected2

    def test_cut_and_paste_region(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57],  # 4
        ]
        s = Sheet(data)
        data = s.cut([1, 1], [4, 5])
        s.paste([0, 0], rows=data)
        expected = [
            [22, 23, 24, 25, 5, 6, 7],
            [32, 33, 34, 35, "", 26, 27],
            [42, 43, 44, 45, "", 36, 37],
            [41, "", "", "", "", 46, 47],
            [51, 52, 53, 54, 55, 56, 57],
        ]
        assert expected == s.to_array()

    def test_cut_and_paste_region_within_limits_at_edge(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57],  # 4
        ]
        s = Sheet(data)
        data = s.cut([1, 1], [4, 5])
        s.paste([0, 0], rows=data)
        expected = [
            [22, 23, 24, 25, 5, 6, 7],
            [32, 33, 34, 35, "", 26, 27],
            [42, 43, 44, 45, "", 36, 37],
            [41, "", "", "", "", 46, 47],
            [51, 52, 53, 54, 55, 56, 57],
        ]
        assert expected == s.to_array()


class TestLoadingFunction:
    def test_load_from_dict(self):
        content = {"a": [1, 2, 3, 5], "b": [4, 5, 6, 7, 8]}
        sheet = load_from_dict(content, name_columns_by_row=0)
        assert sorted(sheet.colnames) == sorted(content.keys())

    def test_load_from_records(self):
        content = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        sheet = load_from_records(content, name_columns_by_row=0)
        expected = {"a": [1, 3], "b": [2, 4]}
        assert sheet.to_dict() == expected


class TestSheetTops:
    def test_top(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57],  # 4
        ]
        s = Sheet(data)
        data = s.top(1)
        expected = [[1, 2, 3, 4, 5, 6, 7]]
        assert data.array == expected

    def test_top_with_colnames(self):
        data = [["column 1", "column 2"], [1, 2]]
        s = Sheet(copy.deepcopy(data))
        s.name_columns_by_row(0)
        top_sheet = s.top()
        assert top_sheet.array == data

    def test_top_left(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57],  # 4
        ]
        s = Sheet(data)
        data = s.top_left(rows=1, columns=1)
        expected = [[1]]
        assert data.array == expected

    def test_top_left_with_colnames(self):
        data = [
            ["col 1", "col 2", "col 3", "col 4", "col 5", "col 6"],
            [1, 2, 3, 4, 5, 6],
            [11, 2, 3, 4, 5, 6],
            [21, 2, 3, 4, 5, 6],
            [31, 2, 3, 4, 5, 6],
            [41, 2, 3, 4, 5, 6],
            [51, 2, 3, 4, 5, 6],
        ]
        s = Sheet(data)
        s.name_columns_by_row(0)
        top_sheet = s.top_left()
        expected = [
            ["col 1", "col 2", "col 3", "col 4", "col 5"],
            [1, 2, 3, 4, 5],
            [11, 2, 3, 4, 5],
            [21, 2, 3, 4, 5],
            [31, 2, 3, 4, 5],
            [41, 2, 3, 4, 5],
        ]
        eq_(top_sheet.array, expected)

    def test_top_left_with_colnames_and_rownames(self):
        data = [
            ["", "col 1", "col 2", "col 3", "col 4", "col 5", "col 6"],
            ["row 1", 1, 2, 3, 4, 5, 6],
            ["row 2", 11, 2, 3, 4, 5, 6],
            ["row 3", 21, 2, 3, 4, 5, 6],
            ["row 4", 31, 2, 3, 4, 5, 6],
            ["row 5", 41, 2, 3, 4, 5, 6],
            ["row 6", 51, 2, 3, 4, 5, 6],
        ]
        s = Sheet(data)
        s.name_columns_by_row(0)
        s.name_rows_by_column(0)
        top_sheet = s.top_left()
        expected = [
            ["", "col 1", "col 2", "col 3", "col 4", "col 5"],
            ["row 1", 1, 2, 3, 4, 5],
            ["row 2", 11, 2, 3, 4, 5],
            ["row 3", 21, 2, 3, 4, 5],
            ["row 4", 31, 2, 3, 4, 5],
            ["row 5", 41, 2, 3, 4, 5],
        ]
        eq_(top_sheet.array, expected)
