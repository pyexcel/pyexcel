"""
    pyexcel.sources.file
    ~~~~~~~~~~~~~~~~~~~

    Representation of file sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel import params
import pyexcel.renderers as renderers
from .factory import FileSource


class IOSource(FileSource):
    """
    Get excel data from file source
    """
    attributes = renderers.renderer_factories.keys()

    @classmethod
    def can_i_handle(cls, action, file_type):
        if action == params.WRITE_ACTION:
            status = file_type in tuple(
                renderers.renderer_factories.keys())
        else:
            status = False
        return status


class SheetSource(IOSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [params.FILE_NAME]
    targets = (params.SHEET,)
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        self.file_type = file_name.split(".")[-1]
        self.renderer = renderers.get_renderer(self.file_type)

    def write_data(self, sheet):
        self.renderer.render_sheet_to_file(self.file_name,
                                           sheet, **self.keywords)


class BookSource(SheetSource):
    """Pick up 'file_name' field and do multiple sheet based read and write
    """
    targets = (params.BOOK,)

    def write_data(self, book):
        self.renderer.render_book_to_file(self.file_name, book,
                                          **self.keywords)


class WriteOnlySheetSource(IOSource):
    fields = [params.FILE_TYPE]
    targets = (params.SHEET,)
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_type=None, file_stream=None, **keywords):
        self.renderer = renderers.get_renderer(file_type)
        if file_stream:
            self.content = file_stream
        else:
            self.content = self.renderer.get_io()
        self.file_type = file_type
        self.keywords = keywords

    def write_data(self, sheet):
        self.renderer.render_sheet_to_stream(self.content,
                                             sheet, **self.keywords)


class WriteOnlyBookSource(WriteOnlySheetSource):
    """
    Multiple sheet data source for writting back to memory
    """
    targets = (params.BOOK,)

    def write_data(self, book):
        self.renderer.render_book_to_stream(self.content, book,
                                            **self.keywords)


sources = (
    WriteOnlySheetSource,
    WriteOnlyBookSource,
    SheetSource,
    BookSource
)
