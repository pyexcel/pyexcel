from six import with_metaclass
from pyexcel._compact import StringIO


renderer_registry = {}


def _register_renderer(renderer_cls):
    for file_type in renderer_cls.file_types:
        renderer_registry[file_type] = renderer_cls


class MetaForRendererRegistryOnly(type):
    """sole class registry"""
    def __init__(cls, name, bases, nmspc):
        super(MetaForRendererRegistryOnly, cls).__init__(
            name, bases, nmspc)
        _register_renderer(cls)


class Renderer(with_metaclass(MetaForRendererRegistryOnly, object)):
    file_types = ()

    def __init__(self, file_type):
        self.file_type = file_type
        self.stream = None

    def get_io(self):
        return StringIO()

    def render_sheet_to_file(self, file_name, sheet,
                             write_title=True, **keywords):
        self.set_write_title(write_title)
        with open(file_name, 'w') as outfile:
            self.set_output_stream(outfile)
            self.render_sheet(sheet)

    def render_sheet_to_stream(self, file_stream, sheet,
                               write_title=True, **keywords):
        self.set_write_title(write_title)
        self.set_output_stream(file_stream)
        self.render_sheet(sheet)

    def render_book_to_file(self, file_name, book,
                            write_title=True, **keywords):
        self.set_write_title(write_title)
        with open(file_name, 'w') as outfile:
            self.set_output_stream(outfile)
            self.render_book(book)

    def render_book_to_stream(self, file_stream, book,
                              write_title=True, **keywords):
        self.set_write_title(write_title)
        self.set_output_stream(file_stream)
        self.render_book(book)

    def set_output_stream(self, stream):
        self.stream = stream

    def set_write_title(self, flag):
        self.write_title = flag

    def render_sheet(self, sheet):
        raise NotImplementedError("Please render sheet")

    def render_book(self, book):
        number_of_sheets = book.number_of_sheets() - 1
        for index, sheet in enumerate(book):
            self.render_sheet(sheet)
            if index < number_of_sheets:
                self.stream.write('\n')
