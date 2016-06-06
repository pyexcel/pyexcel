"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Core functionality of pyexcel, data model

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .sheet import (
    Sheet, SheetStream, NominableSheet
)
from .nominablesheet import NamedRow, NamedColumn, VALID_SHEET_PARAMETERS
from .matrix import Matrix, transpose, Row, Column
