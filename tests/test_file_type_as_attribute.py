import os
from pyexcel.sources import Source
from pyexcel.plugins.sources import params
from pyexcel import Sheet, Book
from pyexcel import get_book, save_as
from _compact import StringIO, OrderedDict
from nose.tools import eq_, raises
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

    def get_internal_stream(self):
        return self.content


def test_sheet_register_presentation():
    Sheet.register_presentation(FIXTURE)
    s = Sheet([[1, 2]])
    assert s.dummy == FIXTURE


def test_book_register_presentation():
    Book.register_presentation(FIXTURE)
    b = Book({"sheet": [[1, 2]]})
    assert b.dummy == FIXTURE


@raises(NotImplementedError)
def test_invalid_url_getter():
    sheet = Sheet()
    sheet.csv = "a,b,c"
    sheet.url


@raises(NotImplementedError)
def test_invalid_json_stter():
    sheet = Sheet()
    sheet.json = "a,b,c"


def test_set_csv_attribute():
    sheet = Sheet()
    sheet.csv = "a,b,c"
    expected = dedent("""
    csv:
    +---+---+---+
    | a | b | c |
    +---+---+---+""").strip('\n')
    eq_(str(sheet), expected)


def test_set_csv_attribute2():
    sheet = Sheet()
    content = "a,b,c"
    sheet.set_csv(content, name_columns_by_row=0)
    expected = dedent("""
    csv:
    +---+---+---+
    | a | b | c |
    +===+===+===+
    +---+---+---+""").strip('\n')
    eq_(str(sheet), expected)


def test_get_csv_stream():
    sheet = Sheet()
    sheet.csv = "a,b,c"
    stream = sheet.stream.csv
    expected = 'a,b,c\r\n'
    eq_(stream.getvalue(), expected)


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
    # hei, please note the following test
    # get csv stream
    stream = book.stream.csv
    eq_(stream.getvalue(), expected)


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


def test_save_handsontable_html():
    test_file = '1.handsontable.html'
    save_as(array=[[1]], dest_file_name=test_file)

    with open(test_file, 'r') as f:
        content = f.read()
        assert 'handsontable.full.min.js' in content

    os.unlink(test_file)
