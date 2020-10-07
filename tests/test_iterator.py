import os
import copy
import datetime

from base import PyexcelIteratorBase, create_sample_file2
from pyexcel import Reader, SeriesReader, save_as, get_sheet
from pyexcel.internal.sheets import Matrix, _shared

from nose.tools import eq_, raises


class TestMatrixColumn:
    def setUp(self):
        self.data = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4], [1]]
        self.data3 = [[1, 1], [2, 2]]
        self.result = [
            [1, 2, 3, 4, 5, 6, 1, 2],
            [1, 2, 3, 4, "", "", 1, 2],
            [1, "", "", "", "", "", "", ""],
        ]

    def test_to_array(self):
        m = Matrix(self.data)
        result = [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, "", ""],
            [1, "", "", "", "", ""],
        ]
        eq_(result, m.get_internal_array())

    def test_get_slice_of_columns(self):
        m = Matrix(self.data)
        data = m.column[:2]
        assert data == [[1, 1, 1], [2, 2, ""]]

    @raises(IndexError)
    def test_get_with_a_wrong_column_index(self):
        """Get with a wrong index"""
        m = Matrix(self.data)
        m.column[1.11]  # bang, string type index

    @raises(IndexError)
    def test_delete_with_a_wrong_column_index(self):
        """Get with a wrong index"""
        m = Matrix(self.data)
        del m.column[1.11]  # bang, string type index

    @raises(IndexError)
    def test_set_column_with_a_wrong_column_index(self):
        """Get with a wrong index"""
        m = Matrix(self.data)
        m.column[1.11] = 1  # bang, string type index

    @raises(IndexError)
    def test_get_with_a_wrong_index(self):
        """Get with a wrong index"""
        m = Matrix(self.data)
        m[1.1]  # bang,

    @raises(IndexError)
    def test_set_with_a_wrong_index(self):
        """Get with a wrong index"""
        m = Matrix(self.data)
        m[1.1] = 1  # bang,

    def test_extend_columns(self):
        """Test extend columns"""
        m = Matrix(self.data)
        m.extend_columns(self.data3)
        eq_(self.result, m.get_internal_array())

    def test_extend_column(self):
        """test extend just one column"""
        m = Matrix(self.data)
        m.extend_columns([1, 1])
        assert m.row[0] == self.result[0][:7]

    @raises(TypeError)
    def test_extend_columns2(self):
        """Test extend columns"""
        m = Matrix(self.data)
        m.extend_columns(1.1)

    def test_iadd_list(self):
        """Test in place add a list"""
        m2 = Matrix(self.data)
        m2.column += self.data3
        eq_(self.result, m2.get_internal_array())

    def test_add(self):
        """Test operator add overload"""
        # +
        m3 = Matrix(self.data)
        m4 = m3.column + self.data3
        eq_(self.result, m4.get_internal_array())

    def test_iadd_matrix(self):
        """Test in place add a matrix"""
        m5 = Matrix(copy.deepcopy(self.data))
        m6 = Matrix(copy.deepcopy(self.data))
        m7 = m5.column + m6
        result2 = [
            [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, "", "", 1, 2, 3, 4, "", ""],
            [1, "", "", "", "", "", 1, "", "", "", "", ""],
        ]
        eq_(result2, m7.get_internal_array())

    @raises(TypeError)
    def test_type_error(self):
        m = Matrix(self.data)
        m.column += 12  # bang, cannot add integers

    def test_delete_columns(self):
        r = Matrix(self.data)
        # delete a list of indices
        r.delete_columns([0, 2])
        assert r.row[0] == [2, 4, 5, 6]

    @raises(TypeError)
    def test_delete_wrong_type(self):
        r = Matrix(self.data)
        r.delete_columns("hi")  # bang, cannot delete columns named as string

    def test_delete_one_index(self):
        m = Matrix(self.data)
        del m.column[0]
        assert m.row[0] == [2, 3, 4, 5, 6]
        del m.column["A"]
        assert m.row[0] == [3, 4, 5, 6]

    def test_delete_a_slice(self):
        m = Matrix(self.data)
        del m.column[0:2]
        assert m.row[0] == [3, 4, 5, 6]

    def test_set_columns(self):
        matrix = Matrix(self.data)
        content = ["r", "s", "t", "o"]
        matrix.column[1] = content
        assert matrix.column[1] == content
        assert matrix.column[0] == [1, 1, 1, ""]
        matrix.column["B"] = ["p", "q", "r"]
        eq_(matrix.column["B"], ["p", "q", "r", "o"])

    def test_set_a_slice_of_column(self):
        r = Matrix(self.data)
        content2 = [1, 2, 3, 4]
        r.column[1:] = content2
        assert r.column[2] == content2

    def test_set_a_special_slice(self):
        r = Matrix(self.data)
        content3 = [True, False, True, False]
        r.column[0:0] = content3
        assert r.column[0] == content3

    def test_a_stepper_in_a_slice(self):
        r = Matrix(self.data)
        r.column[0:2:1] = [1, 1, 1, 1]
        assert r.column[0] == [1, 1, 1, 1]
        assert r.column[1] == [1, 1, 1, 1]
        assert r.column[2] == [3, 3, "", ""]

    def test_set_an_invalid_slice(self):
        m = Matrix(self.data)
        try:
            m.column[2:1] = ["e", "r", "r", "o"]
            assert 1 == 2
        except ValueError:
            assert 1 == 1


class TestMatrixRow:
    def setUp(self):
        self.data = [
            ["a", "b", "c", "d"],
            ["e", "f", "g", "h"],
            ["i", "j", 1.1, 1],
        ]
        self.content = [
            ["r", "s", "t", "o"],
            [1, 2, 3, 4],
            [True],
            [1.1, 2.2, 3.3, 4.4, 5.5],
        ]

    def test_extend_rows(self):
        r = Matrix(self.data)
        r.extend_rows(self.content)
        assert r.row[3] == ["r", "s", "t", "o", ""]
        assert r.row[4] == [1, 2, 3, 4, ""]
        assert r.row[5] == [True, "", "", "", ""]
        assert r.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]

    @raises(TypeError)
    def test_extend_rows_error_input(self):
        r = Matrix(self.data)
        r.extend_rows(102)

    def test_iadd(self):
        """Test in place add"""
        r2 = Matrix(self.data)
        r2.row += self.content
        assert r2.row[3] == ["r", "s", "t", "o", ""]
        assert r2.row[4] == [1, 2, 3, 4, ""]
        assert r2.row[5] == [True, "", "", "", ""]
        assert r2.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]

    def test_iadd_matrix(self):
        """Test in place add"""
        r2 = Matrix(self.data)
        r3 = Matrix(self.content)
        r2.row += r3
        assert r2.row[3] == ["r", "s", "t", "o", ""]
        assert r2.row[4] == [1, 2, 3, 4, ""]
        assert r2.row[5] == [True, "", "", "", ""]
        assert r2.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]

    def test_add(self):
        r3 = Matrix(self.data)
        r3 = r3.row + self.content
        assert r3.row[3] == ["r", "s", "t", "o", ""]
        assert r3.row[4] == [1, 2, 3, 4, ""]
        assert r3.row[5] == [True, "", "", "", ""]
        assert r3.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]

    @raises(TypeError)
    def test_type_error(self):
        m = Matrix(self.data)
        m.row += 12  # bang, cannot add integer

    def test_delete_a_index(self):
        """Delete a index"""
        r = Matrix(self.data)
        content = ["i", "j", 1.1, 1]
        assert r.row[2] == content
        del r.row[0]
        assert r.row[1] == content

    def test_delete_a_slice(self):
        """Delete a slice"""
        r2 = Matrix(self.data)
        del r2.row[1:]
        assert r2.number_of_rows() == 1

    def test_delete_special_slice(self):
        r3 = Matrix(self.data)
        content = ["i", "j", 1.1, 1]
        del r3.row[0:0]
        assert r3.row[1] == content
        assert r3.number_of_rows() == 2

    def test_delete_an_invalid_slice(self):
        m = Matrix(self.data)
        try:
            del m.row[2:1]
            assert 1 == 2
        except ValueError:
            assert 1 == 1

    def test_set_a_row(self):
        r = Matrix(self.data)
        content = ["r", "s", "t", "o"]
        r.row[1] = content
        assert r.row[1] == content

    def test_set_using_a_slice(self):
        """Set a list of rows"""
        r = Matrix(self.data)
        content2 = [1, 2, 3, 4]
        r.row[1:] = content2
        assert r.row[2] == [1, 2, 3, 4]

    def test_a_special_slice(self):
        r = Matrix(self.data)
        content3 = [True, False, True, False]
        r.row[0:0] = content3
        assert r.row[0] == [True, False, True, False]

    def test_a_stepper_in_a_slice(self):
        r = Matrix(self.data)
        r.row[0:2:1] = [1, 1, 1, 1]
        assert r.row[0] == [1, 1, 1, 1]
        assert r.row[1] == [1, 1, 1, 1]
        assert r.row[2] == ["i", "j", 1.1, 1]

    def test_a_wrong_slice(self):
        r = Matrix(self.data)
        try:
            r.row[2:1] = ["e", "r", "r", "o"]
            assert 1 == 2
        except ValueError:
            assert 1 == 1


class TestMatrix:
    def setUp(self):
        self.data = [
            ["a", "b", "c", "d"],
            ["e", "f", "g", "h"],
            ["i", "j", 1.1, 1],
        ]

    def test_empty_array_input(self):
        """Test empty array as input to Matrix"""
        m = Matrix([])
        assert m.number_of_columns() == 0
        assert m.number_of_rows() == 0

    def test_update_a_cell(self):
        r = Matrix(self.data)
        r[0, 0] = "k"
        assert r[0, 0] == "k"
        d = datetime.date(2014, 10, 1)
        r.cell_value(0, 1, d)
        assert isinstance(r[0, 1], datetime.date) is True
        assert r[0, 1].strftime("%d/%m/%y") == "01/10/14"
        r["A1"] = "p"
        assert r[0, 0] == "p"
        r[0, 1] = 16
        assert r["B1"] == 16

    def test_old_style_access(self):
        r = Matrix(self.data)
        r[0, 0] = "k"
        assert r[0][0] == "k"

    @raises(IndexError)
    def test_wrong_index_type(self):
        r = Matrix(self.data)
        r["string"][0]  # bang, cannot get

    @raises(IndexError)
    def test_wrong_index_type2(self):
        r = Matrix(self.data)
        r["string"] = "k"  # bang, cannot set

    def test_transpose(self):
        data = [[1, 2, 3], [4, 5, 6]]
        result = [[1, 4], [2, 5], [3, 6]]
        m = Matrix(data)
        m.transpose()
        eq_(result, m.get_internal_array())

    def test_set_column_at(self):
        r = Matrix(self.data)
        try:
            r.set_column_at(1, [11, 1], 1000)
            assert 1 == 2
        except IndexError:
            assert 1 == 1

    @raises(IndexError)
    def test_delete_rows_with_invalid_list(self):
        m = Matrix([])
        m.delete_rows("ab")  # bang, cannot delete


class TestIteratableArray(PyexcelIteratorBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.array = []
        for i in [0, 4, 8]:
            array = [i + 1, i + 2, i + 3, i + 4]
            self.array.append(array)
        self.iteratable = Matrix(self.array)


class TestIterator(PyexcelIteratorBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.xlsx"
        create_sample_file2(self.testfile)
        self.iteratable = Reader(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestHatIterators:
    def setUp(self):
        self.testfile = "test.xlsm"
        self.content = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
        ]
        save_as(dest_file_name=self.testfile, array=self.content)

    def test_hat_column_iterator(self):
        r = SeriesReader(self.testfile)
        actual = {
            "X": [1, 1, 1, 1, 1],
            "Y": [2, 2, 2, 2, 2],
            "Z": [3, 3, 3, 3, 3],
        }
        eq_(r.dict, actual)

    def test_named_row_iterator(self):
        sheet = get_sheet(file_name=self.testfile, name_columns_by_row=0)
        for row in sheet.named_rows():
            assert row == {"Y": 2, "Z": 3, "X": 1}

    def test_named_column_iterator(self):
        sheet = get_sheet(file_name=self.testfile, transpose_after=True)
        sheet.name_rows_by_column(0)
        for row in sheet.named_columns():
            assert row == {"Y": 2, "Z": 3, "X": 1}

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestUtilityFunctions:
    def test_excel_column_index(self):
        chars = ""
        index = _shared.excel_column_index(chars)
        assert index == -1
        chars = "Z"
        index = _shared.excel_column_index(chars)
        assert index == 25
        chars = "AB"
        index = _shared.excel_column_index(chars)
        assert index == 27
        chars = "AAB"
        index = _shared.excel_column_index(chars)
        eq_(index, 703)

    def test_excel_cell_position(self):
        pos_chars = "A"
        row, column = _shared.excel_cell_position(pos_chars)
        assert row == -1
        assert column == -1
        pos_chars = "A1"
        row, column = _shared.excel_cell_position(pos_chars)
        assert row == 0
        assert column == 0
        pos_chars = "AAB111"
        row, column = _shared.excel_cell_position(pos_chars)
        assert row == 110
        eq_(column, 703)

    @raises(ValueError)
    def test_analyse_slice(self):
        a = slice(None, 3)
        bound = 4
        expected = [0, 1, 2]
        result = _shared.analyse_slice(a, bound)
        assert expected == result
        a = slice(1, None)
        bound = 4
        expected = [1, 2, 3]
        result = _shared.analyse_slice(a, bound)
        assert expected == result
        a = slice(2, 1)  # invalid series
        bound = 4
        result = _shared.analyse_slice(a, bound)  # bang
