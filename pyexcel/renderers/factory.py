from pyexcel._compact import StringIO


class RendererManager(type):
    def __init__(cls, name, bases, nmspc):
        super(RendererManager, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        for file_type in cls.file_types:
            cls.registry[file_type] = cls


class Renderer(object):
    file_types = ()
    __metaclass__ = RendererManager

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
