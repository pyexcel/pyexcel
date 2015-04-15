"""
    pyexcel.constants
    ~~~~~~~~~~~~~~~~~~~

    Constants appeared in pyexcel

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
DEFAULT_NAME = 'pyexcel'
DEFAULT_SHEET_NAME = 'pyexcel_sheet1'

MESSAGE_WARNING = "We do not overwrite files"
MESSAGE_WRITE_ERROR = "Cannot write sheet"
MESSAGE_ERROR_02 = "No valid parameters found!"
MESSAGE_ERROR_03 = "cannot handle unknown content"
MESSAGE_DATA_ERROR_NO_SERIES = "No column names or row names found"
MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST = "Column list is empty. Do not waste resource"
MESSAGE_DATA_ERROR_COLUMN_LIST_INTEGER_TYPE = "Column list should be a list of integers"
MESSAGE_DATA_ERROR_COLUMN_LIST_STRING_TYPE = "Column list should be a list of integers"
MESSAGE_INDEX_OUT_OF_RANGE = "Index out of range"
MESSAGE_DATA_ERROR_EMPTY_CONTENT = "Nothing to be pasted!"
MESSAGE_DATA_ERROR_DATA_TYPE_MISMATCH = "Data type mismatch"
MESSAGE_DATA_ERROR_ORDEREDDICT_IS_EXPECTED = "Please give a ordered list"

MESSAGE_DEPRECATED_ROW_COLUMN = "Deprecated usage. Please use [row, column]"
MESSAGE_DEPRECATED_02 = "Depreciated usage. please use dest_file_name"

MESSAGE_NOT_IMPLEMENTED_01 = "Please .row or .column to extendsheet"
MESSAGE_NOT_IMPLEMENTED_02 = "Confused! What do you want to put as column names"
MESSAGE_CANNOT_WRITE_STREAM_FORMATTER = "Cannot write content of file type %s to stream"
MESSAGE_CANNOT_READ_STREAM_FORMATTER = "Cannot read content of file type %s from stream"
MESSAGE_CANNOT_WRITE_FILE_TYPE_FORMATTER = "Cannot write content of file type %s to file %s"
MESSAGE_CANNOT_READ_FILE_TYPE_FORMATTER = "Cannot read content of file type %s from file %s"
MESSAGE_LOADING_FORMATTER = "The plugin for file type %s is not installed. Please install %s"