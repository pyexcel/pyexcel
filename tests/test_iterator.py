import os
import copy
import datetime
import unittest

import pytest
from pyexcel import Reader, SeriesReader, save_as, get_sheet
from pyexcel.internal.sheets import Matrix, _shared

from .base import PyexcelIteratorBase, create_sample_file2
from .nose_tools import eq_, raises


def get_data():
    return [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4], [1]]


DATA3 = [[1, 1], [2, 2]]
RESULT = [
    [1, 2, 3, 4, 5, 6, 1, 2],
    [1, 2, 3, 4, "", "", 1, 2],
    [1, "", "", "", "", "", "", ""],
]


def test_to_array():
    m = Matrix(get_data())
    result = [
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, "", ""],
        [1, "", "", "", "", ""],
    ]
    eq_(result, m.get_internal_array())


def test_get_slice_of_columns():
    m = Matrix(get_data())
    data = m.column[:2]
    assert data == [[1, 1, 1], [2, 2, ""]]


@raises(IndexError)
def test_get_with_a_wrong_column_index():
    """Get with a wrong index"""
    m = Matrix(get_data())
    m.column[1.11]  # bang, string type index


@raises(IndexError)
def test_delete_with_a_wrong_column_index():
    """Get with a wrong index"""
    m = Matrix(get_data())
    del m.column[1.11]  # bang, string type index


@raises(IndexError)
def test_set_column_with_a_wrong_column_index():
    """Get with a wrong index"""
    m = Matrix(get_data())
    m.column[1.11] = 1  # bang, string type index


@raises(IndexError)
def test_get_with_a_wrong_index():
    """Get with a wrong index"""
    m = Matrix(get_data())
    m[1.1]  # bang,


@raises(IndexError)
def test_set_with_a_wrong_index():
    """Get with a wrong index"""
    m = Matrix(get_data())
    m[1.1] = 1  # bang,


def test_extend_columns():
    """Test extend columns"""
    m = Matrix(get_data())
    m.extend_columns(DATA3)
    eq_(RESULT, m.get_internal_array())


def test_extend_column():
    """test extend just one column"""
    m = Matrix(get_data())
    m.extend_columns([1, 1])
    assert m.row[0] == RESULT[0][:7]


@raises(TypeError)
def test_extend_columns2():
    """Test extend columns"""
    m = Matrix(get_data())
    m.extend_columns(1.1)


def test_iadd_list():
    """Test in place add a list"""
    m2 = Matrix(get_data())
    m2.column += DATA3
    eq_(RESULT, m2.get_internal_array())


def test_add():
    """Test operator add overload"""
    # +
    m3 = Matrix(get_data())
    m4 = m3.column + DATA3
    eq_(RESULT, m4.get_internal_array())


def test_iadd_matrix():
    """Test in place add a matrix"""
    m5 = Matrix(copy.deepcopy(get_data()))
    m6 = Matrix(copy.deepcopy(get_data()))
    m7 = m5.column + m6
    result2 = [
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, "", "", 1, 2, 3, 4, "", ""],
        [1, "", "", "", "", "", 1, "", "", "", "", ""],
    ]
    eq_(result2, m7.get_internal_array())


@raises(TypeError)
def test_type_error():
    m = Matrix(get_data())
    m.column += 12  # bang, cannot add integers


def test_delete_columns():
    r = Matrix(get_data())
    # delete a list of indices
    r.delete_columns([0, 2])
    assert r.row[0] == [2, 4, 5, 6]


@raises(TypeError)
def test_delete_wrong_type():
    r = Matrix(get_data())
    r.delete_columns("hi")  # bang, cannot delete columns named as string


def test_delete_one_index():
    m = Matrix(get_data())
    del m.column[0]
    assert m.row[0] == [2, 3, 4, 5, 6]
    del m.column["A"]
    assert m.row[0] == [3, 4, 5, 6]


def test_delete_a_slice():
    m = Matrix(get_data())
    del m.column[0:2]
    assert m.row[0] == [3, 4, 5, 6]


def test_set_columns():
    matrix = Matrix(get_data())
    content = ["r", "s", "t", "o"]
    matrix.column[1] = content
    assert matrix.column[1] == content
    assert matrix.column[0] == [1, 1, 1, ""]
    matrix.column["B"] = ["p", "q", "r"]
    eq_(matrix.column["B"], ["p", "q", "r", "o"])


def test_set_a_slice_of_column():
    r = Matrix(get_data())
    content2 = [1, 2, 3, 4]
    r.column[1:] = content2
    assert r.column[2] == content2


def test_set_a_special_slice():
    r = Matrix(get_data())
    content3 = [True, False, True, False]
    r.column[0:0] = content3
    assert r.column[0] == content3


def test_a_stepper_in_a_slice():
    r = Matrix(get_data())
    r.column[0:2:1] = [1, 1, 1, 1]
    assert r.column[0] == [1, 1, 1, 1]
    assert r.column[1] == [1, 1, 1, 1]
    assert r.column[2] == [3, 3, "", ""]


def test_set_an_invalid_slice():
    m = Matrix(get_data())
    try:
        m.column[2:1] = ["e", "r", "r", "o"]
        assert 1 == 2
    except ValueError:
        assert 1 == 1


def get_data_2():
    return [
        ["a", "b", "c", "d"],
        ["e", "f", "g", "h"],
        ["i", "j", 1.1, 1],
    ]


CONTENT2 = [
    ["r", "s", "t", "o"],
    [1, 2, 3, 4],
    [True],
    [1.1, 2.2, 3.3, 4.4, 5.5],
]


def test_extend_rows():
    r = Matrix(get_data_2())
    r.extend_rows(CONTENT2)
    assert r.row[3] == ["r", "s", "t", "o", ""]
    assert r.row[4] == [1, 2, 3, 4, ""]
    assert r.row[5] == [True, "", "", "", ""]
    assert r.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]


@raises(TypeError)
def test_extend_rows_error_input():
    r = Matrix(get_data_2())
    r.extend_rows(102)


def test_iadd():
    """Test in place add"""
    r2 = Matrix(get_data_2())
    r2.row += CONTENT2
    assert r2.row[3] == ["r", "s", "t", "o", ""]
    assert r2.row[4] == [1, 2, 3, 4, ""]
    assert r2.row[5] == [True, "", "", "", ""]
    assert r2.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]


def test_iadd_matrix():
    """Test in place add"""
    r2 = Matrix(get_data_2())
    r3 = Matrix(CONTENT2)
    r2.row += r3
    assert r2.row[3] == ["r", "s", "t", "o", ""]
    assert r2.row[4] == [1, 2, 3, 4, ""]
    assert r2.row[5] == [True, "", "", "", ""]
    assert r2.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]


def test_add():
    r3 = Matrix(get_data_2())
    r3 = r3.row + CONTENT2
    assert r3.row[3] == ["r", "s", "t", "o", ""]
    assert r3.row[4] == [1, 2, 3, 4, ""]
    assert r3.row[5] == [True, "", "", "", ""]
    assert r3.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]


@raises(TypeError)
def test_type_error():
    m = Matrix(get_data_2())
    m.row += 12  # bang, cannot add integer


def test_delete_a_index():
    """Delete a index"""
    r = Matrix(get_data_2())
    content = ["i", "j", 1.1, 1]
    assert r.row[2] == content
    del r.row[0]
    assert r.row[1] == content


def test_delete_a_slice():
    """Delete a slice"""
    r2 = Matrix(get_data_2())
    del r2.row[1:]
    assert r2.number_of_rows() == 1


def test_delete_special_slice():
    r3 = Matrix(get_data_2())
    content = ["i", "j", 1.1, 1]
    del r3.row[0:0]
    assert r3.row[1] == content
    assert r3.number_of_rows() == 2


def test_delete_an_invalid_slice():
    m = Matrix(get_data_2())
    try:
        del m.row[2:1]
        assert 1 == 2
    except ValueError:
        assert 1 == 1


def test_set_a_row():
    r = Matrix(get_data_2())
    content = ["r", "s", "t", "o"]
    r.row[1] = content
    assert r.row[1] == content


def test_set_using_a_slice():
    """Set a list of rows"""
    r = Matrix(get_data_2())
    content2 = [1, 2, 3, 4]
    r.row[1:] = content2
    assert r.row[2] == [1, 2, 3, 4]


def test_a_special_slice():
    r = Matrix(get_data_2())
    content3 = [True, False, True, False]
    r.row[0:0] = content3
    assert r.row[0] == [True, False, True, False]


def test_a_stepper_in_a_slice():
    r = Matrix(get_data_2())
    r.row[0:2:1] = [1, 1, 1, 1]
    assert r.row[0] == [1, 1, 1, 1]
    assert r.row[1] == [1, 1, 1, 1]
    assert r.row[2] == ["i", "j", 1.1, 1]


def test_a_wrong_slice():
    r = Matrix(get_data_2())
    try:
        r.row[2:1] = ["e", "r", "r", "o"]
        assert 1 == 2
    except ValueError:
        assert 1 == 1


DATA_1 = [
    ["a", "b", "c", "d"],
    ["e", "f", "g", "h"],
    ["i", "j", 1.1, 1],
]


def test_empty_array_input():
    """Test empty array as input to Matrix"""
    m = Matrix([])
    eq_(m.number_of_columns(), 0)
    eq_(m.number_of_rows(), 0)


def test_update_a_cell():
    r = Matrix(DATA_1)
    r[0, 0] = "k"
    eq_(r[0, 0], "k")

    d = datetime.date(2014, 10, 1)
    r.cell_value(0, 1, d)
    eq_(isinstance(r[0, 1], datetime.date), True)
    eq_(r[0, 1].strftime("%d/%m/%y"), "01/10/14")
    r["A1"] = "p"
    eq_(r[0, 0], "p")
    r[0, 1] = 16
    eq_(r["B1"], 16)


def test_old_style_access():
    r = Matrix(DATA_1)
    r[0, 0] = "k"
    eq_(r[0][0], "k")


def test_wrong_index_type():
    r = Matrix(DATA_1)
    with pytest.raises(KeyError):
        r["string"][0]  # bang, cannot get


def test_wrong_index_type_set():
    r = Matrix(DATA_1)
    with pytest.raises(KeyError):
        r["string"] = "k"  # bang, cannot set


def test_transpose():
    data = [[1, 2, 3], [4, 5, 6]]
    result = [[1, 4], [2, 5], [3, 6]]
    m = Matrix(data)
    m.transpose()
    eq_(result, m.get_internal_array())


def test_set_column_at():
    r = Matrix(DATA_1)
    try:
        r.set_column_at(1, [11, 1], 1000)
        assert 1 == 2
    except IndexError:
        assert 1 == 1


def test_delete_rows_with_invalid_list():
    m = Matrix([])
    with pytest.raises(IndexError):
        m.delete_rows("ab")  # bang, cannot delete


def test_excel_column_index():
    chars = ""
    index = _shared.excel_column_index(chars)

    eq_(index, -1)

    chars = "Z"
    index = _shared.excel_column_index(chars)
    eq_(index, 25)

    chars = "AB"
    index = _shared.excel_column_index(chars)
    eq_(index, 27)

    chars = "AAB"
    index = _shared.excel_column_index(chars)
    eq_(index, 703)


def test_excel_cell_position():
    with pytest.raises(KeyError):
        row, column = _shared.excel_cell_position("A")

    eq_(_shared.excel_cell_position("A1"), (0, 0))
    eq_(_shared.excel_cell_position("Z1"), (0, 25))
    eq_(_shared.excel_cell_position("AA1"), (0, 26))
    eq_(_shared.excel_cell_position("AAB111"), (110, 703))


def test_analyse_slice():
    a = slice(None, 3)
    bound = 4

    eq_(_shared.analyse_slice(a, bound), [0, 1, 2])

    a = slice(1, None)
    bound = 4
    expected = [1, 2, 3]
    eq_(_shared.analyse_slice(a, bound), expected)

    a = slice(2, 1)  # invalid series
    bound = 4

    with pytest.raises(ValueError):
        _shared.analyse_slice(a, bound)  # bang
