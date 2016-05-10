from .._compact import StringIO

from .base import FileSource
from . import params
from .factory import RendererFactory
from . import txttable

RendererFactory.register_renderers(txttable.file_types, txttable.renderer)

file_types = set(RendererFactory.render_factories.keys())


class TextTableSource(FileSource):
    fields = [params.FILE_NAME]
    actions = (params.WRITE_ACTION,)

    @classmethod
    def can_i_handle(cls, action, file_type):
        status = False
        if action == params.WRITE_ACTION and file_type in RendererFactory.render_factories.keys():
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
        renderer = RendererFactory.get_renderer(self.file_type)
        texts = renderer(sheet)
        if self.write_title:
            stream.write("%s:\n" % sheet.name)
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


sources = (SheetSource, SheetSourceInMemory, BookSource, BookSourceInMemory)