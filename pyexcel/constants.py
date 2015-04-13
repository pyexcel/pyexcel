"""
    pyexcel.constants
    ~~~~~~~~~~~~~~~~~~~

    Constants appeared in pyexcel

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""

DEFAULT_SHEET_NAME = 'pyexcel_sheet1'

MESSAGE_WRITE_ERROR = "Cannot write sheet"
MESSAGE_DATA_ERROR_NO_SERIES = "No column names or row names found"
MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST = "Column list is empty. Do not waste resource"
MESSAGE_DATA_ERROR_COLUMN_LIST_INTEGER_TYPE = "Column list should be a list of integers"
MESSAGE_DATA_ERROR_COLUMN_LIST_STRING_TYPE = "Column list should be a list of integers"
MESSAGE_INDEX_OUT_OF_RANGE = "Index out of range"
MESSAGE_DATA_ERROR_EMPTY_CONTENT = "Nothing to be pasted!"
MESSAGE_DATA_ERROR_DATA_TYPE_MISMATCH = "Data type mismatch"
MESSAGE_DATA_ERROR_ORDEREDDICT_IS_EXPECTED = "Please give a ordered list"

MESSAGE_DEPRECATED_ROW_COLUMN = "Deprecated usage. Please use [row, column]"

MESSAGE_NOT_IMPLEMENTED_01 = "Please .row or .column to extendsheet"
MESSAGE_NOT_IMPLEMENTED_02 = "Confused! What do you want to put as column names"