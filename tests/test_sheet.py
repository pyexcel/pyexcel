from textwrap import dedent

from pyexcel import Sheet

from nose.tools import eq_


def test_project():
    sheet = Sheet(
        [["A", "B", "C"], [1, 2, 3], [11, 22, 33], [111, 222, 333]],
        name_columns_by_row=0,
    )
    expected = dedent(
        """
    pyexcel sheet:
    +-----+-----+-----+
    |  B  |  A  |  C  |
    +=====+=====+=====+
    | 2   | 1   | 3   |
    +-----+-----+-----+
    | 22  | 11  | 33  |
    +-----+-----+-----+
    | 222 | 111 | 333 |
    +-----+-----+-----+""",
    ).strip()
    sheet = sheet.project(["B", "A", "C"])
    eq_(expected, str(sheet))


def test_project_for_less():
    sheet = Sheet(
        [["A", "B", "C"], [1, 2, 3], [11, 22, 33], [111, 222, 333]],
        name_columns_by_row=0,
    )
    expected = dedent(
        """
    pyexcel sheet:
    +-----+-----+
    |  B  |  C  |
    +=====+=====+
    | 2   | 3   |
    +-----+-----+
    | 22  | 33  |
    +-----+-----+
    | 222 | 333 |
    +-----+-----+""",
    ).strip()
    sheet = sheet.project(["B", "C"])
    eq_(expected, str(sheet))


def test_project_for_exclusion():
    sheet = Sheet(
        [["A", "B", "C"], [1, 2, 3], [11, 22, 33], [111, 222, 333]],
        name_columns_by_row=0,
    )
    expected = dedent(
        """
    pyexcel sheet:
    +-----+
    |  A  |
    +=====+
    | 1   |
    +-----+
    | 11  |
    +-----+
    | 111 |
    +-----+""",
    ).strip()
    sheet = sheet.project(["B", "C"], exclusion=True)
    eq_(expected, str(sheet))
