"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Core functionality of pyexcel, data model

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
# flake8: noqa
from .sheet import Sheet
from .nominablesheet import NamedRow, NamedColumn
from .nominablesheet import NominableSheet
from .matrix import Matrix, transpose, Row, Column
