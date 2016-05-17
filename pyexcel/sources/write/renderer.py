from pyexcel._compact import StringIO
from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel_io import save_data, RWManager
from pyexcel_io.utils import AVAILABLE_WRITERS


class RendererFactory:
    renderer_factories = {}

    @classmethod
    def get_renderer(self, file_type):
        renderer_class = self.renderer_factories.get(file_type)
        return renderer_class(file_type)

    @classmethod
    def register_renderers(self, renderers):
        for renderer in renderers:
            for file_type in renderer.file_types:
                self.renderer_factories[file_type] = renderer


class BaseRenderer(object):
    file_types = tuple(AVAILABLE_WRITERS) + tuple(RWManager.writer_factories.keys())

    def __init__(self, file_type):
        self.file_type = file_type
        self.stream = None

    def get_io(self):
        return RWManager.get_io(self.file_type)

    def render_sheet_to_file(self, file_name, sheet, **keywords):
        sheet_name = DEFAULT_SHEET_NAME
        if sheet.name:
            sheet_name = sheet.name
        data = {sheet_name: sheet.to_array()}
        save_data(file_name,
                  data,
                  **keywords)

    def render_book_to_file(self, file_name, book, **keywords):
        save_data(file_name, book.to_dict(), **keywords)


    def render_sheet_to_stream(self, file_stream, sheet, **keywords):
        sheet_name = DEFAULT_SHEET_NAME
        if sheet.name:
            sheet_name = sheet.name
        data = {sheet_name: sheet.to_array()}
        save_data(file_stream,
                  data,
                  file_type=self.file_type,
                  **keywords)
        
    def render_book_to_stream(self, file_stream, book, **keywords):
        save_data(file_stream, book.to_dict(),
                  file_type=self.file_type, **keywords)


RendererFactory.register_renderers((BaseRenderer,))


class Renderer(BaseRenderer):
    def get_io(self):
        return StringIO()

    def render_sheet_to_file(self, file_name, sheet, write_title=True, **keywords):
        self.set_write_title(write_title)
        with open(file_name, 'w') as outfile:
            self.set_output_stream(outfile)
            self.render_sheet(sheet)

    def render_sheet_to_stream(self, file_stream, sheet, write_title=True, **keywords):
        self.set_write_title(write_title)
        self.set_output_stream(file_stream)
        self.render_sheet(sheet)

    def render_book_to_file(self, file_name, book, write_title=True, **keywords):
        self.set_write_title(write_title)
        with open(file_name, 'w') as outfile:
            self.set_output_stream(outfile)
            self.render_book(book)

    def render_book_to_stream(self, file_stream, book, write_title=True, **keywords):
        self.set_write_title(write_title)
        self.set_output_stream(file_stream)
        self.render_book(book)

    def set_output_stream(self, stream):
        self.stream = stream

    def set_write_title(self, flag):
        self.write_title = flag

    def render_sheet(self, sheet):
        self.stream.write(sheet.name)

    def render_book(self, book):
        number_of_sheets = book.number_of_sheets() - 1
        for index, sheet in enumerate(book):
            self.render_sheet(sheet)
            if index < number_of_sheets:
                self.stream.write('\n')
