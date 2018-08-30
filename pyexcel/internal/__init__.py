"""
    pyexcel.internal
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Pyexcel internals that subjected to change

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from lml.loader import scan_plugins
from pyexcel.internal.plugins import PARSER, RENDERER  # noqa
from pyexcel.internal.source_plugin import SOURCE  # noqa
from pyexcel.internal.generators import SheetStream, BookStream  # noqa


BLACK_LIST = [
    "pyexcel_io",
    "pyexcel_webio",
    "pyexcel_xlsx",
    "pyexcel_xls",
    "pyexcel_ods3",
    "pyexcel_ods",
    "pyexcel_odsr",
    "pyexcel_xlsxw",
]
WHITE_LIST = [
    "pyexcel.plugins.parsers",
    "pyexcel.plugins.renderers",
    "pyexcel.plugins.sources",
]


scan_plugins("pyexcel_", "pyexcel", BLACK_LIST, WHITE_LIST)
