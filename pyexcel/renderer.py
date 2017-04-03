"""
    pyexcel.renderer
    ~~~~~~~~~~~~~~~~~~~

    Renders pyexcel.Book and pyexcel.Sheet to any format

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel._compact import StringIO, with_metaclass
from pyexcel.internal.renderer_meta import MetaForRendererRegistryOnly


class Renderer(with_metaclass(MetaForRendererRegistryOnly, object)):
    """
    Render pyexcel sheet or book into excel format as any other formats
    """
    file_types = ()
    WRITE_FLAG = 'w'

    def __init__(self, file_type):
        self._file_type = file_type
        self._stream = None
        self._write_title = True

    def get_io(self):
        """
        If your renderer's output is binary, please override it and
        return BytesIO instead
        """
        return StringIO()

    def render_sheet_to_file(self, file_name, sheet,
                             write_title=True, **keywords):
        """Render a sheet to a physical file

        :param file_name: the output file name
        :param sheet: pyexcel sheet instance to be rendered
        :param write_title: to write sheet name
        :param keywords: any other keywords to the renderer
        """
        self.set_write_title(write_title)
        with open(file_name, self.WRITE_FLAG) as outfile:
            self.set_output_stream(outfile)
            self.render_sheet(sheet, **keywords)

    def render_sheet_to_stream(self, file_stream, sheet,
                               write_title=True, **keywords):
        """Render a sheet to a file stream

        :param file_stream: the output file stream
        :param sheet: pyexcel sheet instance to be rendered
        :param write_title: to write sheet name
        :param keywords: any other keywords to the renderer
        """
        self.set_write_title(write_title)
        self.set_output_stream(file_stream)
        self.render_sheet(sheet, **keywords)

    def render_book_to_file(self, file_name, book,
                            write_title=True, **keywords):
        """Render a book to a physical file

        :param file_name: the output file name
        :param book: pyexcel book instance to be rendered
        :param write_title: to write sheet names
        :param keywords: any other keywords to the renderer
        """
        self.set_write_title(write_title)
        with open(file_name, self.WRITE_FLAG) as outfile:
            self.set_output_stream(outfile)
            self.render_book(book, **keywords)

    def render_book_to_stream(self, file_stream, book,
                              write_title=True, **keywords):
        """Render a book to a file stream

        :param file_stream: the output file stream
        :param book: pyexcel book instance to be rendered
        :param write_title: to write sheet names
        :param keywords: any other keywords to the renderer
        """
        self.set_write_title(write_title)
        self.set_output_stream(file_stream)
        self.render_book(book, **keywords)

    def render_sheet(self, sheet, **keywords):
        """
        If your renderer is kind of text format, you just
        need to implement this function.

        :param sheet: pyexcel sheet instance to be rendered
        :param keywords: any other keywords to the renderer
        """
        raise NotImplementedError("Please render sheet")

    def render_book(self, book, **keywords):
        """
        Implementation of book rendering

        :param book: pyexcel book instance to be rendered
        :param keywords: any other keywords to the renderer
        """
        number_of_sheets = book.number_of_sheets() - 1
        for index, sheet in enumerate(book):
            self.render_sheet(sheet)
            if index < number_of_sheets:
                self._stream.write('\n')

    def set_output_stream(self, stream):
        self._stream = stream

    def set_write_title(self, flag):
        self._write_title = flag
