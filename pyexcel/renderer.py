from pyexcel._compact import StringIO, with_metaclass
from pyexcel.internal.renderer_meta import MetaForRendererRegistryOnly


class Renderer(with_metaclass(MetaForRendererRegistryOnly, object)):
    file_types = ()
    WRITE_FLAG = 'w'

    def __init__(self, file_type):
        self._file_type = file_type
        self._stream = None
        self._write_title = True

    def get_io(self):
        return StringIO()

    def render_sheet_to_file(self, file_name, sheet,
                             write_title=True, **keywords):
        self.set_write_title(write_title)
        with open(file_name, self.WRITE_FLAG) as outfile:
            self.set_output_stream(outfile)
            self.render_sheet(sheet, **keywords)

    def render_sheet_to_stream(self, file_stream, sheet,
                               write_title=True, **keywords):
        self.set_write_title(write_title)
        self.set_output_stream(file_stream)
        self.render_sheet(sheet, **keywords)

    def render_book_to_file(self, file_name, book,
                            write_title=True, **keywords):
        self.set_write_title(write_title)
        with open(file_name, self.WRITE_FLAG) as outfile:
            self.set_output_stream(outfile)
            self.render_book(book, **keywords)

    def render_book_to_stream(self, file_stream, book,
                              write_title=True, **keywords):
        self.set_write_title(write_title)
        self.set_output_stream(file_stream)
        self.render_book(book, **keywords)

    def set_output_stream(self, stream):
        self._stream = stream

    def set_write_title(self, flag):
        self._write_title = flag

    def render_sheet(self, sheet, **keywords):
        raise NotImplementedError("Please render sheet")

    def render_book(self, book, **keywords):
        number_of_sheets = book.number_of_sheets() - 1
        for index, sheet in enumerate(book):
            self.render_sheet(sheet)
            if index < number_of_sheets:
                self._stream.write('\n')
