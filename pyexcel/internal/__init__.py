"""
    pyexcel.internal
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Pyexcel internals that subjected to change

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from lml.loader import scan_plugins
from pyexcel.internal.plugins import IOPluginManager
from pyexcel.internal.source_plugin import SourcePluginManager
from pyexcel.internal.generators import SheetStream, BookStream  # noqa


RENDERER = IOPluginManager('renderer')
PARSER = IOPluginManager('parser')
SOURCE = SourcePluginManager()

BLACK_LIST = ['pyexcel_io', 'pyexcel_webio',
              'pyexcel_xlsx', 'pyexcel_xls',
              'pyexcel_ods3', 'pyexcel_ods',
              'pyexcel_odsr', 'pyexcel_xlsxw']
WHITE_LIST = [
    'pyexcel.plugins.parsers',
    'pyexcel.plugins.renderers',
    'pyexcel.plugins.sources',
]


scan_plugins('pyexcel_', 'pyexcel', BLACK_LIST, WHITE_LIST)
