# since v0.2.2
from textwrap import dedent
from pyexcel.sheets import Sheet
from nose.tools import eq_


def test_sheet_content():
    array = [[1, 2]]
    sheet = Sheet(array)
    expected = dedent("""
    +---+---+
    | 1 | 2 |
    +---+---+""").strip('\n')
    eq_(str(sheet.content), expected)


def test_random_access():
    test_content = [[1, 2]]
    sheet = Sheet(test_content)
    eq_(sheet.to_array(), test_content)
    expected = dedent("""
    pyexcel sheet:
    +---+-----+
    | 1 | 100 |
    +---+-----+""").strip('\n')
    sheet[0, 1] = 100
    eq_(str(sheet), expected)


def test_random_access_to_unknown_area():
    test_content = [[1, 2]]
    sheet = Sheet(test_content)
    eq_(sheet.to_array(), test_content)
    expected = dedent("""
    pyexcel sheet:
    +---+---+-----+
    | 1 | 2 |     |
    +---+---+-----+
    +---+---+-----+
    |   |   | 100 |
    +---+---+-----+""").strip('\n')
    sheet[2, 2] = 100
    eq_(str(sheet), expected)
