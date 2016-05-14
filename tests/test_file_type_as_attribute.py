from pyexcel.sources.base import FileSource
from pyexcel.sources.excel import WriteOnlyMemorySourceMixin
from pyexcel.sources import params
from pyexcel.factory import SourceFactory
from pyexcel import Sheet, Book
from _compact import StringIO

FIXTURE = "dummy"


class DummySource(FileSource, WriteOnlyMemorySourceMixin):
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
    s = Sheet([[1,2]])
    assert s.dummy == FIXTURE


def test_book_register_presentation():
    Book.register_presentation('dummy')
    b = Book({"sheet":[[1,2]]})
    assert b.dummy == FIXTURE

