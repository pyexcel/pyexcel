"""
    pyexcel.internal.common
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Defintion for the shared objects

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import sys
import types
from itertools import product

from lml.plugin import PluginInfo, PluginInfoChain

from pyexcel._compact import PY2
from pyexcel._compact import is_string
from pyexcel.internal.plugins import PARSER, RENDERER
import pyexcel.constants as constants
from pyexcel.exceptions import FileTypeNotSupported


class StreamAttribute(object):
    """Provide access to get_*_stream methods"""
    def __init__(self, cls):
        self.cls = cls

    def __getattr__(self, name):
        getter = getattr(self.cls, 'save_to_memory')
        return getter(file_type=name)


class PyexcelObject(object):
    """parent class for pyexcel.Sheet and pyexcel.Book"""
    @property
    def stream(self):
        """Return a stream in which the content is properly encoded

        Example::

            >>> import pyexcel as p
            >>> b = p.get_book(bookdict={"A": [[1]]})
            >>> csv_stream = b.stream.texttable
            >>> print(csv_stream.getvalue())
            A:
            +---+
            | 1 |
            +---+

        Where b.stream.xls.getvalue() is equivalent to b.xls. In some situation
        b.stream.xls is prefered than b.xls.

        Sheet examples::

            >>> import pyexcel as p
            >>> s = p.Sheet([[1]], 'A')
            >>> csv_stream = s.stream.texttable
            >>> print(csv_stream.getvalue())
            A:
            +---+
            | 1 |
            +---+

        Where s.stream.xls.getvalue() is equivalent to s.xls. In some situation
        s.stream.xls is prefered than s.xls.

        It is similar to :meth:`~pyexcel.Book.save_to_memory`.
        """
        return StreamAttribute(self)

    def __repr__(self):
        if PY2:
            default_encoding = sys.getdefaultencoding()
            if default_encoding == "ascii":
                result = self.texttable
                return result.encode('utf-8')

        return self.texttable

    def __str__(self):
        return self.__repr__()


class SourceInfo(PluginInfo):
    """Plugin description for a source"""
    def __init__(self, absolute_import_path, **keywords):
        PluginInfo.__init__(self, "source",
                            absolute_import_path, **keywords)

    def tags(self):
        target_action_list = product(
            self.targets, self.actions)
        for target, action in target_action_list:
            yield "%s-%s" % (target, action)

    def is_my_business(self, action, **keywords):
        statuses = [_has_field(field, keywords) for field in self.fields]
        results = [status for status in statuses if status is False]
        return len(results) == 0


class FileSourceInfo(SourceInfo):
    """Plugin description for a file source"""
    def is_my_business(self, action, **keywords):
        status = SourceInfo.is_my_business(self, action, **keywords)
        if status:
            file_name = keywords.get("file_name", None)
            if file_name:
                if is_string(type(file_name)):
                    file_type = _find_file_type_from_file_name(file_name,
                                                               action)
                else:
                    raise IOError("Wrong file name")
            else:
                file_type = keywords.get("file_type")

            status = self.can_i_handle(action, file_type)
        return status

    def can_i_handle(self, action, file_type):
        raise NotImplementedError("")


class InputSourceInfo(FileSourceInfo):
    """Plugin description for an input source"""
    def can_i_handle(self, action, file_type):
        __file_type = None
        if file_type:
            __file_type = file_type.lower()
        if action == constants.READ_ACTION:
            status = __file_type in PARSER.get_all_file_types()
        else:
            status = False
        return status


class OutputSourceInfo(FileSourceInfo):
    """Plugin description for a output file source"""
    def can_i_handle(self, action, file_type):
        if action == constants.WRITE_ACTION:
            status = file_type.lower() in tuple(
                RENDERER.get_all_file_types())
        else:
            status = False
        return status


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None


def _find_file_type_from_file_name(file_name, action):
    if action == 'read':
        list_of_file_types = PARSER.get_all_file_types()
    else:
        list_of_file_types = RENDERER.get_all_file_types()
    file_types = []
    lowercase_file_name = file_name.lower()
    for a_supported_type in list_of_file_types:
        if lowercase_file_name.endswith(a_supported_type):
            file_types.append(a_supported_type)
    if len(file_types) > 1:
        file_types = sorted(file_types, key=len)
        file_type = file_types[-1]
    elif len(file_types) == 1:
        file_type = file_types[0]
    else:
        file_type = lowercase_file_name.split('.')[-1]
        raise FileTypeNotSupported(
            constants.FILE_TYPE_NOT_SUPPORTED_FMT % (file_type, action))

    return file_type


class IOPluginInfo(PluginInfo):
    """Plugin description for a parser or a renderer"""
    def tags(self):
        file_types = self.file_types
        if isinstance(file_types, types.FunctionType):
            file_types = file_types()
        for file_type in file_types:
            yield file_type


class PyexcelPluginChain(PluginInfoChain):
    """A list for pyexcel plugins"""
    def add_a_source(self, relative_plugin_class_path=None, **keywords):
        default = {
            'key': None,
            'attributes': []
        }
        default.update(keywords)
        self.add_a_plugin_instance(SourceInfo(
            self._get_abs_path(relative_plugin_class_path), **default))
        return self

    def add_an_input_source(self, relative_plugin_class_path=None, **keywords):
        default = {
            'key': None,
            'attributes': []
        }
        default.update(keywords)
        self.add_a_plugin_instance(InputSourceInfo(
            self._get_abs_path(relative_plugin_class_path), **default))
        return self

    def add_a_output_source(self, relative_plugin_class_path=None, **keywords):
        default = {
            'key': None,
            'attributes': []
        }
        default.update(keywords)
        self.add_a_plugin_instance(OutputSourceInfo(
            self._get_abs_path(relative_plugin_class_path), **default))
        return self

    def add_a_parser(self, relative_plugin_class_path=None, file_types=None):
        self.add_a_plugin_instance(IOPluginInfo(
            "parser", self._get_abs_path(relative_plugin_class_path),
            file_types=file_types))
        return self

    def add_a_renderer(self, relative_plugin_class_path=None,
                       file_types=None, stream_type=None):
        default = dict(file_types=file_types,
                       stream_type=stream_type)
        self.add_a_plugin_instance(IOPluginInfo(
            "renderer", self._get_abs_path(relative_plugin_class_path),
            **default))
        return self


class SheetIterator(object):
    """
    Sheet Iterator
    """
    def __init__(self, bookreader):
        self.book_reader_ref = bookreader
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        """get next sheet"""
        if self.current < self.book_reader_ref.number_of_sheets():
            self.current += 1
            return self.book_reader_ref[self.current-1]
        else:
            raise StopIteration
