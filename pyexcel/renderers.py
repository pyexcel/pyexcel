import logging

from pyexcel._compact import StringIO, with_metaclass
from pyexcel.internal import soft_renderer_registry, preload_a_plugin
from pyexcel._compact import PY2


log = logging.getLogger(__name__)
renderer_registry = {}


def get_renderer(file_type):
    __file_type = None
    if file_type:
        __file_type = file_type.lower()
    preload_a_plugin(soft_renderer_registry, file_type)
    renderer_class = renderer_registry.get(__file_type)
    if renderer_class is None:
        raise Exception("No renderer found for %s" % file_type)
    return renderer_class(__file_type)


def get_all_file_types():
    if PY2:
        file_types = renderer_registry.keys() + soft_renderer_registry.keys()
    else:
        file_types = (list(renderer_registry.keys()) +
                      list(soft_renderer_registry.keys()))
    return file_types


def _register_renderer(renderer_cls):
    __file_types = []
    for file_type in set(renderer_cls.file_types):
        __file_types.append(file_type)
        renderer_registry[file_type] = renderer_cls
    log.debug("%s: %s" % (",".join(__file_types), renderer_cls))


class MetaForRendererRegistryOnly(type):
    """sole class registry"""
    def __init__(cls, name, bases, nmspc):
        super(MetaForRendererRegistryOnly, cls).__init__(
            name, bases, nmspc)
        _register_renderer(cls)


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
