import os
from pyexcel.sources.factory import Source
from pyexcel.sources import params
from pyexcel import Sheet, Book
from pyexcel import get_book
from _compact import StringIO, OrderedDict
from nose.tools import eq_
from textwrap import dedent

FIXTURE = "dummy"


class DummySource(Source):
    """
    Write into json file
    """
    fields = [FIXTURE]
    targets = (params.BOOK, params.SHEET)
    actions = (params.WRITE_ACTION,)
    attributes = [FIXTURE]
    key = FIXTURE

    def __init__(self, file_type=None, file_stream=None, **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = StringIO()
        self.file_type = file_type
        self.keywords = keywords

    def write_data(self, sheet):
        self.content.write(FIXTURE)


def test_sheet_register_presentation():
    Sheet.register_presentation(FIXTURE)
    s = Sheet([[1, 2]])
    assert s.dummy == FIXTURE


def test_book_register_presentation():
    Book.register_presentation(FIXTURE)
    b = Book({"sheet": [[1, 2]]})
    assert b.dummy == FIXTURE


def test_set_csv_attribute():
    sheet = Sheet()
    sheet.csv = "a,b,c"
    expected = dedent("""
    csv:
    +---+---+---+
    | a | b | c |
    +---+---+---+""").strip('\n')
    eq_(str(sheet), expected)


def test_book_attribute():
    book = get_book(file_name=os.path.join("tests",
                                           "fixtures",
                                           "test-multiple.csvz"))
    expected = ("---pyexcel:sheet1---\r\n" +
                "1,4,9\r\n" +
                "2,5,8\r\n" +
                "3,6,7\r\n" +
                "---pyexcel---\r\n" +
                "---pyexcel:sheet2---\r\n" +
                "1,4,9\r\n" +
                "2,5,8\r\n" +
                "3,6,7\r\n" +
                "---pyexcel---\r\n" +
                "---pyexcel:sheet3---\r\n" +
                "1,4,9\r\n" +
                "2,5,8\r\n" +
                "3,6,7\r\n" +
                "---pyexcel---\r\n")
    eq_(book.csv, expected)


def test_set_book_attribute():
    file_name = os.path.join("tests",
                             "fixtures",
                             "test-multiple.csvz")
    with open(file_name, 'rb') as f:
        csvz_content = f.read()
        book = Book()
        book.csvz = csvz_content
        expected = ("---pyexcel:sheet1---\r\n" +
                    "1,4,9\r\n" +
                    "2,5,8\r\n" +
                    "3,6,7\r\n" +
                    "---pyexcel---\r\n" +
                    "---pyexcel:sheet2---\r\n" +
                    "1,4,9\r\n" +
                    "2,5,8\r\n" +
                    "3,6,7\r\n" +
                    "---pyexcel---\r\n" +
                    "---pyexcel:sheet3---\r\n" +
                    "1,4,9\r\n" +
                    "2,5,8\r\n" +
                    "3,6,7\r\n" +
                    "---pyexcel---\r\n")
        eq_(book.csv, expected)


def test_set_array():
    c = Sheet()
    test_array = [[1, 2]]
    c.array = test_array
    expected = dedent("""
    pyexcel_sheet1:
    +---+---+
    | 1 | 2 |
    +---+---+""").strip()
    eq_(str(c), expected)
    eq_(c.array, test_array)


def test_set_records():
    s = Sheet()
    test_records = [{"name": "a", "age": 11}, {"name": "b", "age": 12}]
    s.records = test_records
    expected = dedent("""
    pyexcel_sheet1:
    +-----+------+
    | age | name |
    +-----+------+
    | 11  | a    |
    +-----+------+
    | 12  | b    |
    +-----+------+""").strip()
    eq_(str(s), expected)
    s.name_columns_by_row(0)
    eq_(s.records, test_records)


def test_set_dict():
    s = Sheet()
    test_dict = {"a": [1, 2, 3], "b": [2, 3, 4]}
    s.dict = test_dict
    expected = dedent("""
    pyexcel_sheet1:
    +---+---+
    | a | b |
    +---+---+
    | 1 | 2 |
    +---+---+
    | 2 | 3 |
    +---+---+
    | 3 | 4 |
    +---+---+""").strip()
    eq_(expected, str(s))
    s.name_columns_by_row(0)
    eq_(s.dict, test_dict)


def test_set_bookdict():
    b = Book()
    b.bookdict = {"sheet1": [[1]], "sheet2": [[2]]}
    expected = dedent("""
    sheet1:
    +---+
    | 1 |
    +---+
    sheet2:
    +---+
    | 2 |
    +---+""").strip()
    eq_(str(b), expected)
    expected = OrderedDict([('sheet1', [[1]]), ('sheet2', [[2]])])
    eq_(b.bookdict, expected)