"""
    pyexcel.constants
    ~~~~~~~~~~~~~~~~~~~

    Constants appeared in pyexcel

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
# flake8: noqa
DEFAULT_NAME = 'pyexcel sheet'
DEFAULT_SHEET_NAME = 'pyexcel_sheet1'

MESSAGE_WARNING = "We do not overwrite files"
MESSAGE_WRITE_ERROR = "Cannot write sheet"
MESSAGE_ERROR_02 = "No valid parameters found!"
MESSAGE_DATA_ERROR_NO_SERIES = "No column names or row names found"
MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST = "Column list is empty. Do not waste resource"
MESSAGE_DATA_ERROR_COLUMN_LIST_INTEGER_TYPE = "Column list should be a list of integers"
MESSAGE_DATA_ERROR_COLUMN_LIST_STRING_TYPE = "Column list should be a list of integers"
MESSAGE_INDEX_OUT_OF_RANGE = "Index out of range"
MESSAGE_DATA_ERROR_EMPTY_CONTENT = "Nothing to be pasted!"
MESSAGE_DATA_ERROR_DATA_TYPE_MISMATCH = "Data type mismatch"
MESSAGE_DATA_ERROR_ORDEREDDICT_IS_EXPECTED = "Please give a ordered list"

MESSAGE_DEPRECATED_ROW_COLUMN = "Deprecated usage. Please use [row, column]"
MESSAGE_DEPRECATED_OUT_FILE = "Depreciated usage of 'out_file'. please use dest_file_name"
MESSAGE_DEPRECATED_CONTENT = "Depreciated usage of 'content'. please use file_content"

MESSAGE_NOT_IMPLEMENTED_01 = "Please use attribute row or column to extend sheet"
MESSAGE_NOT_IMPLEMENTED_02 = "Confused! What do you want to put as column names"
MESSAGE_READONLY = "This attribute is readonly"
MESSAGE_ERROR_NO_HANDLER = "No suitable plugins imported or installed"
MESSAGE_UNKNOWN_IO_OPERATION = "Internal error: an illegal source action"
_IMPLEMENTATION_REMOVED = "Deprecated since 0.3.0! Implementation removed"