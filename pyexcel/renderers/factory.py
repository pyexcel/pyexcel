import logging

from pyexcel._compact import StringIO, with_metaclass
from collections import defaultdict


UPGRADE_MESSAGE = "Please upgrade the plugin '%s' according to \
plugin compactibility table."


log = logging.getLogger(__name__)
renderer_registry = {}
soft_renderer_registry = defaultdict(list)


def _register_renderer(renderer_cls):
    __file_types = []
    for file_type in set(renderer_cls.file_types):
        __file_types.append(file_type)
        renderer_registry[file_type] = renderer_cls
    log.debug("%s: %s" % (",".join(__file_types), renderer_cls))


class UpgradePlugin(Exception):
    pass


def pre_register(library_meta, module_name):
    if not isinstance(library_meta, dict):
        plugin = module_name.replace('_', '-')
        raise UpgradePlugin(UPGRADE_MESSAGE % plugin)
    library_import_path = "%s.%s" % (module_name, library_meta['submodule'])
    for file_type in library_meta['file_types']:
        soft_renderer_registry[file_type].append(
            (library_import_path, library_meta['submodule']))
    log.debug("pre-register :" + ','.join(library_meta['file_types']))


def dynamic_load_library(library_import_path):
    __import__(library_import_path[0])


def preload_a_renderer(file_type):
    __file_type = file_type.lower()
    if __file_type in soft_renderer_registry:
        debug_path = []
        for path in soft_renderer_registry[__file_type]:
            dynamic_load_library(path)
            debug_path.append(path)
        log.debug("preload :" + __file_type + ":" + ','.join(path))
        # once loaded, forgot it
        soft_renderer_registry.pop(__file_type)


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
