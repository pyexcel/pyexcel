from .._compact import StringIO

from .base import FileSource
from . import params
from . import _texttable as texttable
from .renderer import RendererFactory


RendererFactory.register_renderers(texttable.renderer)

try:
    import pyexcel_text as text
    RendererFactory.register_renderers(text.renderers)
except ImportError:
    pass


file_types = tuple(RendererFactory.renderer_factories.keys())


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
        self.renderer = RendererFactory.get_renderer(self.file_type)
        self.renderer.set_write_title(self.write_title)

    def write_data(self, sheet):
        self.renderer.set_output_stream(self.content)
        self.write_sheet(self.content, sheet)
            
    def write_sheet(self, stream, sheet):
        self.renderer.render_sheet(sheet)


class SheetSource(SheetSourceInMemory):
    fields = [params.FILE_NAME]
    targets = (params.SHEET, )

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.write_title = write_title
        self.file_type = file_name.split(".")[-1]
        self.renderer = RendererFactory.get_renderer(self.file_type)
        self.renderer.set_write_title(self.write_title)

    def write_data(self, sheet):
        with open(self.file_name, 'w') as output_file:
            self.renderer.set_output_stream(output_file)
            self.write_sheet(output_file, sheet)


class BookSourceInMemory(SheetSourceInMemory):
    targets = (params.BOOK, )

    def write_data(self, book):
        self.renderer.set_output_stream(self.content)
        self.write_book(book)

    def write_book(self, book):
        self.renderer.render_book(book)


class BookSource(BookSourceInMemory):
    fields = [params.FILE_NAME]

    def __init__(self, file_name=None, write_title=True, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.write_title = write_title
        self.file_type = file_name.split(".")[-1]
        self.renderer = RendererFactory.get_renderer(self.file_type)
        self.renderer.set_write_title(self.write_title)

    def write_data(self, book):
        with open(self.file_name, 'w') as output_file:
            self.renderer.set_output_stream(output_file)
            self.renderer.render_book(book)


sources = (SheetSource, SheetSourceInMemory, BookSource, BookSourceInMemory)