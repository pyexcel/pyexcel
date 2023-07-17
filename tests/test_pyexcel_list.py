from pyexcel.internal.sheets.extended_list import PyexcelList

from nose.tools import eq_


def test_pyexcel_list():
    words = "pyexcel is so cool".split()
    result_sheet = PyexcelList(words).value_counts()
    result = list(result_sheet.to_array())
    expected = [
        ["names", "cool", "is", "pyexcel", "so"],
        ["counts", 1, 1, 1, 1],
    ]
    eq_(expected, result)
