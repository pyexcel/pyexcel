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

from lml.plugin import PluginManager
from lml.registry import PluginInfo, PluginList

import pyexcel.constants as constants
import pyexcel.exceptions as exceptions
from pyexcel._compact import PY2


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


class PyexcelPluginManager(PluginManager):
    """pyexcel specific method for load_me_later"""
    def validate_plugin_info(self, plugin_info):
        if not isinstance(plugin_info, PluginInfo):
            plugin = plugin_info.module_name.replace('_', '-')
            raise exceptions.UpgradePlugin(constants.MESSAGE_UPGRADE % plugin)


class SourceInfo(PluginInfo):

    def keywords(self):
        target_action_list = product(
            self.targets, self.actions)
        for target, action in target_action_list:
            yield "%s-%s" % (target, action)


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
