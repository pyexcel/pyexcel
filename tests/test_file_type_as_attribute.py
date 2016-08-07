import os
from pyexcel.sources.file_source_output import WriteOnlySheetSource
from pyexcel import params
from pyexcel import Sheet, Book
from pyexcel import get_book
from _compact import StringIO
from nose.tools import eq_
from textwrap import dedent

FIXTURE = "dummy"


class DummySource(WriteOnlySheetSource):
    """
    Write into json file
    """
    fields = [params.FILE_TYPE]
    targets = (params.BOOK, params.SHEET)
    actions = (params.WRITE_ACTION,)
    attirbutes = ['dummy']

    def __init__(self, file_type=None, file_stream=None, **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = StringIO()
        self.file_type = file_type
        self.keywords = keywords

    @classmethod
    def can_i_handle(cls, action, file_type):
        status = False
        if action == params.WRITE_ACTION and file_type == 'dummy':
            status = True
        return status

    def write_data(self, sheet):
        self.content.write(FIXTURE)


def test_sheet_register_presentation():
    Sheet.register_presentation('dummy')
    s = Sheet([[1, 2]])
    assert s.dummy == FIXTURE


def test_book_register_presentation():
    Book.register_presentation('dummy')
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
