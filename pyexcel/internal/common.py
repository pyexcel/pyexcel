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

from lml.registry import PluginInfo, PluginList

from pyexcel._compact import PY2
from pyexcel._compact import is_string
from pyexcel.internal.plugins import PARSER, RENDERER
import pyexcel.constants as constants
from pyexcel.exceptions import FileTypeNotSupported


class PyexcelObject(object):
    """parent class for pyexcel.Sheet and pyexcel.Book"""
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

    def keywords(self):
        target_action_list = product(
            self.targets, self.actions)
        for target, action in target_action_list:
            yield "%s-%s" % (target, action)

    def is_my_business(self, action, **keywords):
        statuses = [_has_field(field, keywords) for field in self.fields]
        results = [status for status in statuses if status is False]
        return len(results) == 0


class FileSourceInfo(SourceInfo):

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
        file_types = sorted(file_types, key=lambda x: len(x))
        file_type = file_types[-1]
    elif len(file_types) == 1:
        file_type = file_types[0]
    else:
        file_type = lowercase_file_name.split('.')[-1]
        raise FileTypeNotSupported(
            constants.FILE_TYPE_NOT_SUPPORTED_FMT % (file_type, action))

    return file_type


class IOPluginInfo(PluginInfo):

    def keywords(self):
        file_types = self.file_types
        if isinstance(file_types, types.FunctionType):
            file_types = file_types()
        for file_type in file_types:
            yield file_type


class PyexcelPluginList(PluginList):
    def add_a_source(self, submodule=None, **keywords):
        default = {
            'key': None,
            'attributes': []
        }
        default.update(keywords)
        self._add_a_plugin(SourceInfo("source",
                                      self._get_abs_path(submodule),
                                      **default))
        return self

    def add_an_input_source(self, submodule=None, **keywords):
        default = {
            'key': None,
            'attributes': []
        }
        default.update(keywords)
        self._add_a_plugin(InputSourceInfo("source",
                                           self._get_abs_path(submodule),
                                           **default))
        return self

    def add_a_output_source(self, submodule=None, **keywords):
        default = {
            'key': None,
            'attributes': []
        }
        default.update(keywords)
        self._add_a_plugin(OutputSourceInfo("source",
                                            self._get_abs_path(submodule),
                                            **default))
        return self

    def add_a_parser(self, submodule=None, file_types=None):
        self._add_a_plugin(IOPluginInfo(
            "parser", self._get_abs_path(submodule), file_types=file_types))
        return self

    def add_a_renderer(self, submodule=None,
                       file_types=None, stream_type=None):
        default = dict(file_types=file_types,
                       stream_type=stream_type)
        self._add_a_plugin(IOPluginInfo(
            "renderer", self._get_abs_path(submodule), **default))
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
