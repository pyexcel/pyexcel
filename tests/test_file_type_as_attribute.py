from pyexcel.sources.file_source_output import WriteOnlySheetSource
from pyexcel import params
from pyexcel.factory import SourceFactory
from pyexcel import Sheet, Book
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

SourceFactory.register_sources([DummySource])


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
