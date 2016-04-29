from texttable import Texttable

from ..formatters import to_format
from .._compact import StringIO

from .base import FileSource
from . import params


file_types = ('texttable',)


class TextTableSource(FileSource):
    fields = [params.FILE_NAME]
    actions = (params.WRITE_ACTION,)

    @classmethod
    def can_i_handle(cls, action, file_type):
        status = False
        if action == params.WRITE_ACTION and file_type in file_types:
            status = True
        return status


class SheetSourceInMemory(TextTableSource):
    fields = [params.FILE_TYPE]
    targets = (params.SHEET, )

    def __init__(self, file_type=None, file_stream=None, write_title=True,
                 **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = StringIO()
        self.file_type = file_type
        self.keywords = keywords
        self.write_title = write_title

    def write_data(self, sheet):
        self.write_sheet(self.content, sheet)
            
    def write_sheet(self, stream, sheet):
        texts = render_text_table(sheet)
        if self.write_title:
            stream.write("Sheet Name: %s\n" % sheet.name)
        stream.write(texts)


class SheetSource(SheetSourceInMemory):
    fields = [params.FILE_NAME]
    targets = (params.SHEET, )

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.write_title = write_title
        self.file_type = file_name.split(".")[-1]

    def write_data(self, sheet):
        with open(self.file_name, 'w') as output_file:
            self.write_sheet(output_file, sheet)


class BookSourceInMemory(SheetSourceInMemory):
    targets = (params.BOOK, )

    def write_data(self, book):
        self.write_book(self.content, book)

    def write_book(self, stream, book):
        number_of_sheets = book.number_of_sheets() - 1
        for index, sheet in enumerate(book):
            self.write_sheet(stream, sheet)
            if index < number_of_sheets:
                stream.write('\n')


class BookSource(BookSourceInMemory):
    fields = [params.FILE_NAME]

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.write_title = write_title
        self.file_type = file_name.split(".")[-1]

    def write_data(self, sheet):
        with open(self.file_name, 'w') as output_file:
            self.write_book(output_file, sheet)


def render_text_table(sheet):
    table = Texttable(max_width=0)
    data = sheet.to_array()
    table.set_cols_dtype(['t'] * len(data[0]))
    if len(sheet.colnames) > 0:
        table.set_chars(['-', '|', '+', '='])
        table.header(list(_cleanse_a_row(data[0])))
    else:
        table.add_row(list(_cleanse_a_row(data[0])))
    for sub_array in data[1:]:
        new_array = _cleanse_a_row(sub_array)
        table.add_row(list(new_array))
    return table.draw()


def _cleanse_a_row(row):
    for item in row:
        if item == "":
            yield(" ")
        else:
            yield(to_format(str, item))


sources = (SheetSource, SheetSourceInMemory, BookSource, BookSourceInMemory)