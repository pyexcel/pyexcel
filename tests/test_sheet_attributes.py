# since v0.2.2
import copy
from textwrap import dedent

from pyexcel.sheet import Sheet, make_names_unique
from pyexcel.internal.meta import PyexcelObject

from nose.tools import eq_, raises


def test_sheet_content():
    array = [[1, 2]]
    sheet = Sheet(array)
    expected = dedent(
        """
    +---+---+
    | 1 | 2 |
    +---+---+""",
    ).strip("\n")
    eq_(str(sheet.content), expected)


def test_random_access():
    test_content = [[1, 2]]
    sheet = Sheet(test_content)
    eq_(sheet.to_array(), test_content)
    expected = dedent(
        """
    pyexcel sheet:
    +---+-----+
    | 1 | 100 |
    +---+-----+""",
    ).strip("\n")
    sheet[0, 1] = 100
    eq_(str(sheet), expected)


def test_random_access_to_unknown_area():
    test_content = [[1, 2]]
    sheet = Sheet(copy.deepcopy(test_content))
    eq_(sheet.to_array(), test_content)
    expected = [[1, 2, ""], ["", "", ""], ["", "", 100]]
    sheet[2, 2] = 100
    eq_(sheet.array, expected)


def test_named_sheet_access():
    test_content = [["A", "B"], [1, 2]]
    sheet = Sheet(copy.deepcopy(test_content), name_columns_by_row=0)
    eq_(sheet.to_array(), test_content)
    expected = dedent(
        """
    pyexcel sheet:
    +-----+---+
    |  A  | B |
    +=====+===+
    | 100 | 2 |
    +-----+---+""",
    ).strip("\n")
    sheet[0, "A"] = 100
    print(str(sheet))
    eq_(str(sheet), expected)


def test_named_sheet_access_to_unknown_area():
    test_content = [["A", "B"], [1, 2]]
    sheet = Sheet(copy.deepcopy(test_content), name_columns_by_row=0)
    eq_(sheet.to_array(), test_content)
    expected = dedent(
        """
    pyexcel sheet:
    +-----+---+
    |  A  | B |
    +=====+===+
    | 1   | 2 |
    +-----+---+
    | 100 |   |
    +-----+---+""",
    ).strip("\n")
    sheet[1, "A"] = 100
    print(str(sheet))
    eq_(str(sheet), expected)


def test_data_frame_access():
    test_content = [["", "A", "B"], ["R", 1, 2]]
    sheet = Sheet(
        copy.deepcopy(test_content),
        name_columns_by_row=0,
        name_rows_by_column=0,
    )
    eq_(sheet.to_array(), test_content)
    expected = dedent(
        """
    pyexcel sheet:
    +---+-----+---+
    |   |  A  | B |
    +===+=====+===+
    | R | 100 | 2 |
    +---+-----+---+""",
    ).strip("\n")
    sheet["R", "A"] = 100
    print(str(sheet))
    eq_(str(sheet), expected)


def test_html_representation():
    array = [[1, 2]]
    sheet = Sheet(array)
    expected = dedent(
        """
    pyexcel sheet:
    <table>
    <tbody>
    <tr>
    <td style="text-align: right;">1</td>
    <td style="text-align: right;">2</td>
    </tr>
    </tbody>
    </table>""",
    ).strip("\n")
    eq_(str(sheet._repr_html_()), expected)


def test_svg_representation():
    array = [["a", "b"], [1, 2]]
    sheet = Sheet(array)
    io = sheet.plot()
    assert io._repr_svg_() is not None


@raises(NotImplementedError)
def test_pyexcel_object():
    obj = PyexcelObject()
    obj.save_to_memory("csv")


def test_make_names_unique():
    alist = ["a", "a"]
    new_names = make_names_unique(alist)
    expected = ["a", "a-1"]
    eq_(new_names, expected)


def test_make_names_unique_includes_leading_whitespace():
    alist = ["a", " a"]
    new_names = make_names_unique(alist)
    expected = ["a", "a-1"]
    eq_(new_names, expected)


def test_make_names_unique_includes_trailing_whitespace():
    alist = ["a", "a "]
    new_names = make_names_unique(alist)
    expected = ["a", "a-1"]
    eq_(new_names, expected)


def test_make_names_unique_includes_whitespace():
    alist = ["a", "   a   ", "   ", "   "]
    new_names = make_names_unique(alist)
    expected = ["a", "a-1", "", "-1"]
    eq_(new_names, expected)
